import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os
import datetime
from datetime import datetime
from io import BytesIO
import io
from io import StringIO
import base64
import xlsxwriter
from xlsxwriter import Workbook
import time

#


st.set_page_config(
    page_title="Tax Package ML Classification Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)



st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=120)
# st.header('Machine Learnig Model')
st.subheader('Tax Package - Related Party Operations Category Classification Machine Learning Model')

# st.divider()


start_time01 = time.time()
uploaded_FBL3N_train = st.sidebar.file_uploader("Upload FBL3N file which contains historical data classified to train the Machine Learning Model", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()
uploaded_new_FBL3N = st.sidebar.file_uploader("Upload the file which contains the new dataset to be classified", key="new_FBL3N", type=["xlsx"], accept_multiple_files=False)
uploaded_ZLAAUDIT = st.sidebar.file_uploader("Upload the file which contains the ZLAAUDIT dataset", key="ZLAAUDIT", type=["xlsx"], accept_multiple_files=False)
uploaded_SdosFin = st.sidebar.file_uploader("Upload the file which contains the SALDOS FINANCIEROS dataset", key="SaldosFinancieros", type=["xlsx"], accept_multiple_files=False)
uploaded_masters = st.sidebar.file_uploader("Upload masterdata file which contains the Chart of Accounts and Subcodes", key="masters", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()
if uploaded_FBL3N_train and uploaded_new_FBL3N and uploaded_masters: #and uploaded_ZLAAUDIT:
    FBL3N_full = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', 
                               dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str,
                                        'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    FBL3N_new = pd.read_excel(uploaded_new_FBL3N, engine='openpyxl', sheet_name='FBL3N',
                dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Document Number': str,
                        'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})

    # ZLAAUDIT = pd.read_excel(uploaded_ZLAAUDIT, engine='openpyxl', sheet_name='ZLAAUDIT',
    #             dtype = {'CONCAT': str, 'CONCAT_2': str, 'Company Code': str, 'Document Number': str, 'Business Area': str,
    #                     'Document type': str, 'Tax Code': str, 'Line item': str, 'Posting Key': str, 'Account': str, 'Assignment': str,
    #                     'User Name': str, 'Reference': str, 'Document Header Text': str, 'Currency': str, 'Local Currency': str,})

    accounts = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='GL_Accounts',
                dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})

    subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
                  dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
                         'Code_RP': str, 'Code_Desc_RP': str,})

    saldos_financieros = pd.read_excel(uploaded_SdosFin, engine='openpyxl', sheet_name='SaldosFin_MX',
                  dtype={'Concat': str, 'Co_Cd': str, 'Debit Account': str, 'Account Name': str,
                         'Type': str, 'Balance': str,})

    ######----------MACHINE LEARNING MODEL----------######
    #-----Stage 1: Clean dataset, to get unique records and avoid NA, to have a clean Dataset to run the Machine Learning Model
    #----- Step 1: Fill "NaN" cell as empty ('') at specified columns
    NA_Fill_Columns = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_full[NA_Fill_Columns] = FBL3N_full[NA_Fill_Columns].fillna('')
    # FBL3N_full.dropna(subset=NA_Fill_Columns, how='any', inplace=True)
    
    #----- Step 2: Delete rows with no Subcode (either NA or blank)
    FBL3N_full.dropna(subset=['Subcode'], how='any', inplace=True)

    #----- Step 3: Create a new column "ML"
    FBL3N_full['CONCAT'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str))
    FBL3N_full['ML'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + FBL3N_full['Account'] + ' ' + FBL3N_full['Text'] + ' ' + FBL3N_full['Reference'] + ' ' + FBL3N_full['Document Header Text'] + ' ' + FBL3N_full['User Name'] + ' ' + FBL3N_full['Tax Code']
    # FBL3N_full['Id'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + (FBL3N_full['Document Number'].astype(str)) + ' ' + (FBL3N_full['Amount in doc. curr.'].astype(str)) + ' ' + (FBL3N_full['Posting Date'].astype(str))

    #----- Step 4: Create a new column "Subcode_td", which contains the Subcode that has been assigned previously in order to use it later
    FBL3N_full['Subcode_td'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str)) + FBL3N_full['Document Type'] + (FBL3N_full['Posting period'].astype(str)) + (FBL3N_full['Amount in doc. curr.'].astype(str))

    #----- Step 4a: This code is for showing on screen the FBL3N dataset that is going to be used to train the model
    # st.divider()
    # st.caption('ML FBL3N train dataset')
    # # Revisión de los subcodigos asignados para poder mostrar el texto no estandarizado
    # # subcodes_unique = FBL3N_full['Subcode'].unique()
    # # subcodes_options = st.multiselect('Selecciona la clasificación para filtar el dataframe', subcodes_unique, subcodes_unique)
    # # FBL3N_filtered = FBL3N_full[FBL3N_full['Subcode'].isin(subcodes_options)]
    # # st.dataframe(FBL3N_filtered)
    # # Mostrar el dataframe sin filtrar
    # st.dataframe(FBL3N_full)
    # st.divider()

    #----- Step 5: Use FBL3N_full dataset to create a new one, with the Subcode previously assigned (this step applies in case that exists a FBL3N dataset already coded for previous periods and not to loose the work already done)
    FBL3N_previous_subcode = FBL3N_full[['Subcode_td', 'Subcode']].drop_duplicates()
    FBL3N_previous_subcode["conteo"] = FBL3N_previous_subcode.groupby('Subcode_td')['Subcode_td'].transform("size")
    FBL3N_previous_subcode.rename(columns={'Subcode': 'Subcode_assigned'}, inplace=True)
    #----- Step 5a: Shows unique records of previously assigned subcoded dataset
    # st.caption('Registros unicos')
    # st.dataframe(FBL3N_previous_subcode)
    
    #----- Step 6: Delete duplicated values of ML column in order to train the model (test dataset is setup to 20%, this can be adjusted)
    FBL3N_train = FBL3N_full[['ML', 'Subcode']].drop_duplicates()
    X = FBL3N_train['ML']
    y = FBL3N_train['Subcode']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #----- Step 7: Vectorize text data using TF-IDF (in previous versions max_features were set at 1,000, beacuse that provides the best accuracy when training the model, however this can be adjusted manually or with a streamlit widget, but re-runnings take time)
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    #----- Step 8: Train the classification model
    modelo = MultinomialNB()
    modelo.fit(X_train_tfidf, y_train)

    #----- Step 9: Make predictions to the test dataset
    y_pred = modelo.predict(X_test_tfidf)

    #----- Step 10: Calculate model accuracy
    accuracy = accuracy_score(y_test, y_pred)
    accuracy = "{:.2%}".format(accuracy)
    st.metric(label="Model Accuracy", value=accuracy, delta=accuracy)
    
    end_time01 = time.time()
    processing_time01 = end_time01 - start_time01
    processing_time_formatted01 = "{:.2f}".format(processing_time01)
    st.info(f'Machine Learning model training time: {processing_time_formatted01} seconds')

    st.divider()
    # st.subheader('Una vez entrenado el modelo de ML, se realizará la clasificación en el nuevo conjunto de datos')

    start_time02 = time.time()
    

    #----- Stage 2: Work with new FBL3N dataset, Masters (GL_Accounts and Subcodes), ZLAAUDIT and Saldos Financieros
    #----- Step 1: Fill "NaN" cell as empty ('') at specified columns
    columnas_rellenar_real = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_new[columnas_rellenar_real] = FBL3N_new[columnas_rellenar_real].fillna('')

    #----- Step 2: Create a new column "ML"
    FBL3N_new['CONCAT_01'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str))
    FBL3N_new['ML'] = FBL3N_new['Company Code'] + ' ' + FBL3N_new['Document Type'] + ' ' + FBL3N_new['Account'] + ' ' + FBL3N_new['Text'] + ' ' + FBL3N_new['Reference'] + ' ' + FBL3N_new['Document Header Text'] + ' ' + FBL3N_new['User Name'] + ' ' + FBL3N_new['Tax Code']
    # FBL3N_new['Id'] = FBL3N_new['Company Code'] + ' ' + FBL3N_new['Document Type'] + ' ' + (FBL3N_new['Document Number'].astype(str)) + ' ' + (FBL3N_new['Amount in doc. curr.'].astype(str)) + ' ' + (FBL3N_new['Posting Date'].astype(str))

    #----- Step 3: Create a new column for comparing FBL3N (Original and New) to get the previously assigned subcode
    FBL3N_new['Subcode_td_1'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str)) + FBL3N_new['Document Type'] + (FBL3N_new['Posting period'].astype(str)) + (FBL3N_new['Amount in doc. curr.'].astype(str))

    #----- Step 4: Assign the Subcode to the new FBL3N dataset uploades, according to the ML model
    X_new_data_tfidf = tfidf_vectorizer.transform(FBL3N_new['ML'])
    # Realizar predicciones con el modelo entrenado en el conjunto de datos real
    FBL3N_new['Subcode_ML'] = modelo.predict(X_new_data_tfidf)

    #### Testing
    #----- Codigo para crear una nueva columna que contenga el porcentaje de certeza en la prediccion, vamos a ver si funciona
    # Assuming 'modelo' is your trained model
    probability_matrix = modelo.predict_proba(X_new_data_tfidf)
    
    # Extract the probabilities for the predicted class
    certainty_percentages = [max(probabilities) * 100 for probabilities in probability_matrix]
    
    # Create a new column 'Certainty_Percentage' in your DataFrame
    FBL3N_new['Certainty_Percentage'] = certainty_percentages
    
    # Now, FBL3N_new contains a column with the certainty percentage for each prediction
    #### Testing ends

    FBL3N_new = FBL3N_new.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
    NA_Fill_CoCd = ['CoCd']
    FBL3N_new[NA_Fill_CoCd] = FBL3N_new[NA_Fill_CoCd].fillna('')
    #----- Evaluar si quitar el cruzar la tabla con Subcodes (creo que no la estoy usando para nada, y al final las elimino)
    # FBL3N_new = FBL3N_new.merge(subcodes, left_on="Subcode_ML", right_on='Code', how='left')
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

    #----- Contar el numero total de registros (evaluar si la dejo o no)
    # reg_clas = len(FBL3N_new[FBL3N_new['SC_concat'] != ''])
    # st.write(reg_clas)
    
    tab1, tab2 = st.tabs(["Resumen", "Detalle"])
    
    with tab1:
        st.subheader('Resumen')
        FBL3N_summary = FBL3N_new.copy()
        # FBL3N_summary['K1'] = FBL3N_summary['Company Code'] + FBL3N_summary['CoCd'] + FBL3N_summary['Document currency'] + (FBL3N_summary['Subcode_ML'].astype(str))
        # FBL3N_summary['K2'] = FBL3N_summary['CoCd'] + FBL3N_summary['Company Code'] + FBL3N_summary['Document currency'] + (FBL3N_summary['Code_RP'].astype(str))
        # FBL3N_summary = FBL3N_summary.groupby(by=['Company Code', 'CoCd', 'Subcode_ML', 'Code_Type', 'Code_Desc', 'Code_RP', 'Document currency', 'K1', 'K2'], as_index=False)['Amount in doc. curr.'].sum()
       
        # FBL3N_summary2 = FBL3N_summary.copy()
        # FBL3N_summary2.columns = [col_name + '_k2' for col_name in FBL3N_summary2]
        # FBL3N_summary = FBL3N_summary.merge(FBL3N_summary2, left_on="K1", right_on='K2_k2', how='left')
        # FBL3N_summary = FBL3N_summary.drop(columns=['K1', 'K2','Company Code_k2','CoCd_k2','Subcode_ML_k2','Code_Type_k2','Code_Desc_k2','Code_RP_k2','K1_k2','K2_k2'])
        # # FBL3N_summary = FBL3N_summary[['Document currency', 'Amount in doc. curr.', 'Document currency_k2', 'Amount in doc. curr._k2']].fillna(0)
        # # FBL3N_summary = FBL3N_summary[['Amount in doc. curr.', 'Amount in doc. curr._k2']].fillna(0)
        # FBL3N_summary['Diferencia'] = FBL3N_summary['Amount in doc. curr.'] + FBL3N_summary['Amount in doc. curr._k2']
    
        # st.dataframe(FBL3N_summary)
        # st.write(FBL3N_summary.columns)

    with tab2:
        def remove_CONCAT(FBL3N_new):
            if "CONCAT" in FBL3N_new.columns:
                FBL3N_new = FBL3N_new.drop("CONCAT", axis=1)
            return FBL3N_new
        FBL3N_new = remove_CONCAT(FBL3N_new)
        
        def remove_Subcode(FBL3N_new):
            if "Subcode" in FBL3N_new.columns:
                FBL3N_new = FBL3N_new.drop("Subcode", axis=1)
            return FBL3N_new
        FBL3N_new = remove_Subcode(FBL3N_new)

        def remove_RelatedParty(FBL3N_new):
            if "Related Party" in FBL3N_new.columns:
                FBL3N_new = FBL3N_new.drop("Related Party", axis=1)
            return FBL3N_new
        FBL3N_new = remove_RelatedParty(FBL3N_new)

        
        # FBL3N_new = FBL3N_new.drop(['CONCAT', 'Subcode', 'Subcode 2', 'Related Party'], axis=1)
        FBL3N_new = FBL3N_new.merge(FBL3N_previous_subcode, left_on="Subcode_td_1", right_on='Subcode_td', how='left')
        FBL3N_new['Subcode_assigned'] = FBL3N_new['Subcode_assigned'].fillna('')
        def Subcode(row):
        # Verificar las condiciones
            if row['Subcode_assigned'] != '':
                return row['Subcode_assigned']
            else:
                return row['SC_Fix']
        FBL3N_new['Subcode'] = FBL3N_new.apply(Subcode, axis=1)
        
            
        columns_to_eliminate = ['ML', 'Subcode_td_1', 'Subcode_ML', 'GL_Account', 'Description', 'Country', 
                                'SC_1', 'SC_2', 'SC_3', 'SC_4', 'SC_5', 'SC_6', 'SC_7', 'SC_8', 'SC_concat',
                               'SC_Fix', 'Subcode_td', 'Subcode_assigned', 'conteo']
        FBL3N_new = FBL3N_new.drop(columns=columns_to_eliminate)
        columns_to_rename = {'CoCd': 'Related Party', 'CONCAT_01': 'CONCAT'}
        FBL3N_new = FBL3N_new.rename(columns=columns_to_rename)
        
        def create_subcode2(FBL3N_new):
            if "Subcode 2" not in FBL3N_new.columns:
                FBL3N_new["Subcode 2"] = ""
            return FBL3N_new
        FBL3N_new = create_subcode2(FBL3N_new)
        
        
        
        # FBL3N_new['Subcode 2'] = ''
        st.write(FBL3N_new.columns)
        
        FBL3N_new = FBL3N_new[['CONCAT', 'Subcode',  'Subcode 2', 'Related Party', 'Company Code', 'Document Number', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 
                               'User Name', 'Posting period', 'Tax Code', 'Document Date', 'Amount in local currency', 'Local Currency', 'Amount in doc. curr.', 'Document currency', 'Posting Date', 'Status', 'V']]
        date_columns = ['Document Date', 'Posting Date']
        # Convert to datetime and then extract the date
        FBL3N_new[date_columns] = FBL3N_new[date_columns].apply(pd.to_datetime).apply(lambda x: x.dt.date)

        #-------- Para volver a cruzar el dataframe con el Subcode ajustado con el catalogo de cuentas y los subcodigos
        # FBL3N_new = FBL3N_new.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
        # FBL3N_new = FBL3N_new.merge(subcodes, left_on="Subcode", right_on='Code', how='left')

        
        # FBL3N_new['Key1'] = FBL3N_new['Company Code'] + FBL3N_new['CoCd'] + (FBL3N_new['Document Date'].astype(str)) + (FBL3N_new['Amount in doc. curr.'].astype(str))
        # FBL3N_new['Key2'] = FBL3N_new['CoCd'] + FBL3N_new['Company Code'] + (FBL3N_new['Document Date'].astype(str)) + (-FBL3N_new['Amount in doc. curr.']).astype(str)
        FBL3N_new['Key1'] = FBL3N_new['Company Code'] + FBL3N_new['Related Party'] + (FBL3N_new['Amount in doc. curr.'].astype(str))
        FBL3N_new['Key2'] = FBL3N_new['Related Party'] + FBL3N_new['Company Code'] + (-FBL3N_new['Amount in doc. curr.']).astype(str)
        
        FBL3N_new['Counter1'] = FBL3N_new.groupby('Key1').cumcount()
        FBL3N_new['Counter1'] += 0 # Sumar 1 al contador para que comience desde 1 en lugar de 0
        FBL3N_new['Key_1'] = FBL3N_new['Key1'] + FBL3N_new['Counter1'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        FBL3N_new['Counter2'] = FBL3N_new.groupby('Key2').cumcount()
        FBL3N_new['Counter2'] += 0 # Contador para que comience desde 0
        FBL3N_new['Key_2'] = FBL3N_new['Key2'] + FBL3N_new['Counter2'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        
        # FBL3N_real2 = FBL3N_new.copy()
        # FBL3N_real2.columns = [col_name + '_k2' for col_name in FBL3N_real2]
        # FBL3N_real = FBL3N_real.merge(FBL3N_real2, left_on="Key1", right_on='Key2_k2', how='left')
        # st.dataframe(FBL3N_tobe_class)
        # st.dataframe(FBL3N_classified)

        #----- eliminar las columnas Key1, Key2, Counter1, Counter2
        drop_keycols = ['Key1', 'Key2', 'Counter1', 'Counter2']
        FBL3N_new = FBL3N_new.drop(columns=drop_keycols)

        integer_cols = ['Subcode', 'Account', 'Document Number']
        FBL3N_new[integer_cols] = FBL3N_new[integer_cols].apply(pd.to_numeric, errors='coerce', downcast='integer')

        
        st.dataframe(FBL3N_new)
    
    end_time02 = time.time()
    processing_time02 = end_time02 - start_time02
    processing_time_formatted02 = "{:.4f}".format(processing_time02)
    st.info(f'Subcodes has been assigned to the new FBL3N dataset according to the Machine Learning Model in: {processing_time_formatted02} seconds')
#--------------

    current_datetime = datetime.now().strftime('%y%m%d_%H%M')
    file_name = f'FBL3N_{current_datetime}.xlsx'
    
    excel_buffer = BytesIO()
    FBL3N_new.to_excel(excel_buffer, index=False, sheet_name='FBL3N')
# Descargar el archivo Excel en Streamlit
    st.download_button(
        label="Download FBL3N Classified excel file",
        data=excel_buffer.getvalue(),
        file_name=file_name,  # Puedes cambiar el nombre del archivo según tus necesidades
        key='download_button'
    )
