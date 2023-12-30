import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import os
import datetime
from io import BytesIO
import io
from io import StringIO
import base64
import xlsxwriter
from xlsxwriter import Workbook
import time

st.set_page_config(
    page_title="Tax Package ML Classification Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)

def load_data():
    uploaded_FBL3N_train = st.sidebar.file_uploader("Upload FBL3N file...", type=["xlsx"], accept_multiple_files=False)
    uploaded_new_FBL3N = st.sidebar.file_uploader("Upload the file with new dataset...", key="new_FBL3N", type=["xlsx"], accept_multiple_files=False)
    uploaded_masters = st.sidebar.file_uploader("Upload masterdata file...", key="masters", type=["xlsx"], accept_multiple_files=False)

    if uploaded_FBL3N_train and uploaded_new_FBL3N and uploaded_masters:
        st.sidebar.info("Data is being loaded...")
        FBL3N_full = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', dtype={'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str})
        FBL3N_full = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', 
                                   dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str,
                                            'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
        FBL3N_new = pd.read_excel(uploaded_new_FBL3N, engine='openpyxl', sheet_name='FBL3N',
                    dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Document Number': str,
                            'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
        accounts = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='GL_Accounts',
                    dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})
        subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
                      dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
                             'Code_RP': str, 'Code_Desc_RP': str,})

        st.sidebar.success("Data loaded successfully!")
        # Paso 2: Rellenar las celdas "NaN" como celdas vacías ('') en las columnas especificadas
        columnas_rellenar = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
        FBL3N_full[columnas_rellenar] = FBL3N_full[columnas_rellenar].fillna('')
        # FBL3N_full.dropna(subset=columnas_rellenar, how='any', inplace=True)
    
    
        # FBL3N_full
        # Paso 3: Crear una nueva columna 'ML' con el contenido de las columnas especificadas
        FBL3N_full['CONCAT'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str))
        FBL3N_full['ML'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + FBL3N_full['Account'] + ' ' + FBL3N_full['Text'] + ' ' + FBL3N_full['Reference'] + ' ' + FBL3N_full['Document Header Text'] + ' ' + FBL3N_full['User Name'] + ' ' + FBL3N_full['Tax Code']
        FBL3N_full['Id'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + (FBL3N_full['Document Number'].astype(str)) + ' ' + (FBL3N_full['Amount in doc. curr.'].astype(str)) + ' ' + (FBL3N_full['Posting Date'].astype(str))
    
        #---------- Subcode_td: Columna que contiene el Subcode de train data para posteriormente cruzar con el dataset clasificado
        FBL3N_full['Subcode_td'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str)) + FBL3N_full['Document Type'] + (FBL3N_full['Posting period'].astype(str)) + (FBL3N_full['Amount in doc. curr.'].astype(str))
        # st.divider()
        st.caption('ML FBL3N train dataset')
        # Revisión de los subcodigos asignados para poder mostrar el texto no estandarizado
        # subcodes_unique = FBL3N_full['Subcode'].unique()
        # subcodes_options = st.multiselect('Selecciona la clasificación para filtar el dataframe', subcodes_unique, subcodes_unique)
        # FBL3N_filtered = FBL3N_full[FBL3N_full['Subcode'].isin(subcodes_options)]
        # st.dataframe(FBL3N_filtered)
        # Mostrar el dataframe sin filtrar
        st.dataframe(FBL3N_full)
        st.divider()
    
        
        FBL3N_previous_subcode = FBL3N_full[['Subcode_td', 'Subcode']].drop_duplicates()
        FBL3N_previous_subcode["conteo"] = FBL3N_previous_subcode.groupby('Subcode_td')['Subcode_td'].transform("size")
        FBL3N_previous_subcode.rename(columns={'Subcode': 'Subcode_assigned'}, inplace=True)
        st.caption('Registros unicos')
        st.dataframe(FBL3N_previous_subcode)
        FBL3N_train = FBL3N_full[['ML', 'Subcode']].drop_duplicates()
        # FBL3N_train
    
        X = FBL3N_train['ML']
        y = FBL3N_train['Subcode']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
        # Vectorizar los datos de texto utilizando TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
        X_test_tfidf = tfidf_vectorizer.transform(X_test)
    
        # Entrenar un modelo de clasificación
        modelo = MultinomialNB()
        modelo.fit(X_train_tfidf, y_train)
    
        # Realizar predicciones en el conjunto de prueba
        y_pred = modelo.predict(X_test_tfidf)
    
        # Calcular la precisión del modelo en el conjunto de prueba
        accuracy = accuracy_score(y_test, y_pred)
        accuracy = "{:.2%}".format(accuracy)
        # print(accuracy)
        # st.caption('El modelo de aprendizaje finalizó y una vez que el modelo fue probado, dio un porcentaje de accuracy del:')
        st.metric(label="Model Accuracy", value=accuracy, delta=accuracy)
        
        end_time01 = time.time()
        processing_time01 = end_time01 - start_time01
        processing_time_formatted01 = "{:.2f}".format(processing_time01)
        st.info(f'Machine Learning model training time: {processing_time_formatted01} seconds')
    
        st.divider()
    
    
        start_time02 = time.time()
    
        
    
        # Paso 2: Rellenar las celdas "NaN" como celdas vacías ('') en las columnas especificadas
        columnas_rellenar_real = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
        FBL3N_new[columnas_rellenar_real] = FBL3N_new[columnas_rellenar_real].fillna('')
        FBL3N_new['CONCAT'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str))
        FBL3N_new['ML'] = FBL3N_new['Company Code'] + ' ' + FBL3N_new['Document Type'] + ' ' + FBL3N_new['Account'] + ' ' + FBL3N_new['Text'] + ' ' + FBL3N_new['Reference'] + ' ' + FBL3N_new['Document Header Text'] + ' ' + FBL3N_new['User Name'] + ' ' + FBL3N_new['Tax Code']
        # FBL3N_new['Id'] = FBL3N_new['Company Code'] + ' ' + FBL3N_new['Document Type'] + ' ' + (FBL3N_new['Document Number'].astype(str)) + ' ' + (FBL3N_new['Amount in doc. curr.'].astype(str)) + ' ' + (FBL3N_new['Posting Date'].astype(str))
        # FBL3N_new['Subcode_td_1'] = FBL3N_new['Company Code'] + ' ' + (FBL3N_new['Document Number'].astype(str)) + ' ' + FBL3N_new['Document Type'] + ' ' + (FBL3N_new['Posting period'].astype(str)) + ' ' + (FBL3N_new['Amount in doc. curr.'].astype(str))
        FBL3N_new['Subcode_td_1'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str)) + FBL3N_new['Document Type'] + (FBL3N_new['Posting period'].astype(str)) + (FBL3N_new['Amount in doc. curr.'].astype(str))
        X_new_data_tfidf = tfidf_vectorizer.transform(FBL3N_new['ML'])
        # Realizar predicciones con el modelo entrenado en el conjunto de datos real
        FBL3N_new['Subcode_ML'] = modelo.predict(X_new_data_tfidf)
    
        # y_test_pred = modelo.predict(X_test_tfidf)
        # accuracy_test = accuracy_score(y_test, y_test_pred)
    
        FBL3N_new = FBL3N_new.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
        FBL3N_new = FBL3N_new.merge(subcodes, left_on="Subcode_ML", right_on='Code', how='left')
        #---------------Funciones para subcodes fijas-------------------
        def sc_121_1(row):
            if row['Reference'].startswith("00015-") and row['Document Header Text'].startswith("1176"):
                return "121"
            else:
                return ''
    
        def sc_121_2(row):
            if row['Reference'].startswith("00016-") and (row['Document Header Text'].startswith("1176") or row['Document Header Text'].startswith("8")):
                return "121"
            else:
                return ''
    
        def sc_121_3(row):
            if row['Reference'].startswith("1176") and row['Document Type'].startswith("RV"):
                return "121"
            else:
                return ''
    
        def sc_221_1(row):
            if row['Reference'].startswith("1176") and row['Document Type'].startswith("RN"):
                return "221"
            else:
                return ''
    
        def sc_221_2(row):
            if row['Reference'].startswith("CR"):
                return "221"
            else:
                return ''
    
        
        def sc_150(row):
        # Verificar las condiciones
            if "loan int" in str(row['Document Header Text']).lower() and row['Reference'].startswith(str(row['Company Code']) + str(row['CoCd'])):
                return "150"
            else:
                return ''
    
        def sc_250(row):
        # Verificar las condiciones
            if "loan int" in str(row['Document Header Text']).lower() and row['Reference'].startswith(str(row['CoCd']) + str(row['Company Code'])):
                return "250"
            else:
                return ''
    
        def sc_300_1(row):
        # Verificar las condiciones
            if "wf-batch" in str(row['User Name']).lower():
                return "300"
            else:
                return ''
    
        
        FBL3N_new['SC_1'] = FBL3N_new.apply(sc_121_1, axis=1)
        FBL3N_new['SC_2'] = FBL3N_new.apply(sc_121_2, axis=1)
        FBL3N_new['SC_3'] = FBL3N_new.apply(sc_121_3, axis=1)
        FBL3N_new['SC_4'] = FBL3N_new.apply(sc_221_1, axis=1)
        FBL3N_new['SC_5'] = FBL3N_new.apply(sc_221_2, axis=1)
        FBL3N_new['SC_6'] = FBL3N_new.apply(sc_150, axis=1)
        FBL3N_new['SC_7'] = FBL3N_new.apply(sc_250, axis=1)
        FBL3N_new['SC_8'] = FBL3N_new.apply(sc_300_1, axis=1)
        FBL3N_new['SC_concat'] = FBL3N_new['SC_1'] + FBL3N_new['SC_2'] + FBL3N_new['SC_3'] + FBL3N_new['SC_4'] + FBL3N_new['SC_5'] + FBL3N_new['SC_6'] + FBL3N_new['SC_7'] + FBL3N_new['SC_8']
    
        def Subcode_Correction(row):
        # Verificar las condiciones
            if row['SC_concat'] != '' and (row['SC_concat'] != row['Subcode_ML'] ):
                return row['SC_concat']
            else:
                return row['Subcode_ML']
        FBL3N_new['SC_Fix'] = FBL3N_new.apply(Subcode_Correction, axis=1)
        st.sidebar.success("Data loaded successfully!")

        return FBL3N_new

def page1():
    st.title("Machine Learning Classification Model")
    st.info("Please upload the required files.")
    FBL3N_full = load_data()

    if FBL3N_full is not None:
        st.dataframe(FBL3N_full)

def page2(fbl3n_full):
    st.title("Analysis")
    company_codes = fbl3n_full["Company Code"].unique()
    selected_company_code = st.selectbox("Select Company Code", company_codes)
    grouped_data = fbl3n_full[fbl3n_full["Company Code"] == selected_company_code].groupby("Company Code")["amount in doc. curr."].sum()
    st.write(f"Sum of amount in doc. curr. for {selected_company_code}:", grouped_data)

def main():
    # Page 1
    page1()

    # Page 2 (using cached result from Page 1)
    FBL3N_full = load_data()
    if FBL3N_full is not None:
        page2(FBL3N_full)

if __name__ == "__main__":
    main()





#--------mmmmmmmmmmmm-------------------mmmmmmmmmmmmmmmm------------
