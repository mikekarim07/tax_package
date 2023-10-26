import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os
import datetime
import io
from io import StringIO
import base64
import xlsxwriter
import time


st.set_page_config(
    page_title="Modelo de Machine Learning para la clasificación de las partidas intercompañía.",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)


st.header('Machine Learnig Model')
st.subheader('Modelo de aprendizaje automatico de clasificación de categorías y subcategorías de operaciones con partes relacionadas')

st.divider()

start_time01 = time.time()
uploaded_FBL3N_train = st.file_uploader("Carga el archivo que contenga la clasificación para el entrenamiento del modelo de ML", type=["xlsx"], accept_multiple_files=False)
if uploaded_FBL3N_train:
    FBL3N_full = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})

    

    # Paso 2: Rellenar las celdas "NaN" como celdas vacías ('') en las columnas especificadas
    columnas_rellenar = ['Company Code', 'Document Type', 'Account', 'Text', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_full[columnas_rellenar] = FBL3N_full[columnas_rellenar].fillna('')
    # FBL3N_full.dropna(subset=columnas_rellenar, how='any', inplace=True)


    # FBL3N_full
    # Paso 3: Crear una nueva columna 'ML' con el contenido de las columnas especificadas
    FBL3N_full['ML'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + FBL3N_full['Account'] + ' ' + FBL3N_full['Text'] + ' ' + FBL3N_full['Document Header Text'] + ' ' + FBL3N_full['User Name'] + ' ' + FBL3N_full['Tax Code']
    st.divider()
    st.caption('Archivo FBL3N que se va a usar para entrenamiento del modelo')
    # Revisión de los subcodigos asignados para poder mostrar el texto no estandarizado
    # subcodes_unique = FBL3N_full['Subcode'].unique()
    # subcodes_options = st.multiselect('Selecciona la clasificación para filtar el dataframe', subcodes_unique, subcodes_unique)
    # FBL3N_filtered = FBL3N_full[FBL3N_full['Subcode'].isin(subcodes_options)]
    # st.dataframe(FBL3N_filtered)
    # Mostrar el dataframe sin filtrar
    st.dataframe(FBL3N_full)
    st.divider()

    

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
    accuracy = "{:.4%}".format(accuracy)
    # print(accuracy)
    st.caption('El modelo de aprendizaje finalizó y una vez que el modelo fue probado, dio un porcentaje de accuracy del:')
    st.metric(label="Accuracy", value=accuracy, delta=accuracy)
    
    end_time01 = time.time()
    processing_time01 = end_time01 - start_time01
    processing_time_formatted01 = "{:.4f}".format(processing_time01)
    st.info(f'Tiempo total de entrenamiento del Modelo de Aprendizaje de clasificación de las operaciones con partes relacionadas: {processing_time_formatted01} segundos')

st.divider()
st.subheader('Una vez entrenado el modelo de ML, se realizará la clasificación en el nuevo conjunto de datos')

start_time02 = time.time()
uploaded_new_FBL3N = st.file_uploader("Cargar el archivo que contiene el conjunto de datos para su clasificación", key="new_FBL3N", type=["xlsx"], accept_multiple_files=False)
uploaded_masters = st.file_uploader("Cargar el maestros de datos que incluye el catálogo de cuentas y subcategorías", key="masters", type=["xlsx"], accept_multiple_files=False)

if uploaded_new_FBL3N and uploaded_masters:
    FBL3N_real = pd.read_excel(uploaded_new_FBL3N, engine='openpyxl', sheet_name='FBL3N',
                dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str,
                        'Text': str, 'Document Header Text': str, 'User Name': str,
                        'Tax Code': str,})
    accounts = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='GL_Accounts',
                dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})
    subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
                  dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
                         'Code_RP': str, 'Code_Desc_RP': str,})
    
    

    # Paso 2: Rellenar las celdas "NaN" como celdas vacías ('') en las columnas especificadas
    columnas_rellenar_real = ['Company Code', 'Document Type', 'Account', 'Text', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_real[columnas_rellenar_real] = FBL3N_real[columnas_rellenar_real].fillna('')
    FBL3N_real['ML'] = FBL3N_real['Company Code'] + ' ' + FBL3N_real['Document Type'] + ' ' + FBL3N_real['Account'] + ' ' + FBL3N_real['Text'] + ' ' + FBL3N_real['Document Header Text'] + ' ' + FBL3N_real['User Name'] + ' ' + FBL3N_real['Tax Code']
    
    X_new_data_tfidf = tfidf_vectorizer.transform(FBL3N_real['ML'])
    # Realizar predicciones con el modelo entrenado en el conjunto de datos real
    FBL3N_real['Subcode_ML'] = modelo.predict(X_new_data_tfidf)

    # y_test_pred = modelo.predict(X_test_tfidf)
    # accuracy_test = accuracy_score(y_test, y_test_pred)

    FBL3N_real = FBL3N_real.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
    FBL3N_real = FBL3N_real.merge(subcodes, left_on="Subcode_ML", right_on='Code', how='left')

    FBL3N_summary = FBL3N_real.copy()
    FBL3N_summary['K1'] = FBL3N_summary['Company Code'] + FBL3N_summary['CoCd'] + (FBL3N_summary['Subcode_ML'].astype(str))
    FBL3N_summary['K2'] = FBL3N_summary['CoCd'] + FBL3N_summary['Company Code'] + (FBL3N_summary['Code_RP'].astype(str))
    FBL3N_summary = FBL3N_summary.groupby(by=['Company Code', 'CoCd', 'Subcode_ML', 'Code_Type', 'Code_Desc', 'Code_RP', 'Document currency', 'K1', 'K2'], as_index=False)['Amount in doc. curr.'].sum()
   
    FBL3N_summary2 = FBL3N_summary.copy()
    FBL3N_summary2.columns = [col_name + '_k2' for col_name in FBL3N_summary2]
    FBL3N_summary = FBL3N_summary.merge(FBL3N_summary2, left_on="K1", right_on='K2_k2', how='left')
    FBL3N_summary = FBL3N_summary.drop(columns=['K1', 'K2','Company Code_k2','CoCd_k2','Subcode_ML_k2','Code_Type_k2','Code_Desc_k2','Code_RP_k2','K1_k2','K2_k2'])
    FBL3N_summary = FBL3N_summary['Document currency', 'Amount in doc. curr.', 'Document currency_k2', 'Amount in doc. curr._k2'].fillna(0)
    FBL3N_summary['Diferencia'] = FBL3N_summary['Amount in doc. curr.'] + FBL3N_summary['Amount in doc. curr._k2']
    

    
    tab1, tab2 = st.tabs(["Resumen", "Detalle"])
    
    with tab1:
        st.subheader(f'Resumen')
        st.dataframe(FBL3N_summary)

    with tab2:
    
        FBL3N_real['Key1'] = FBL3N_real['Company Code'] + FBL3N_real['CoCd'] + (FBL3N_real['Document Date'].astype(str)) + (FBL3N_real['Amount in doc. curr.'].astype(str))
        FBL3N_real['Key2'] = FBL3N_real['CoCd'] + FBL3N_real['Company Code'] + (FBL3N_real['Document Date'].astype(str)) + (-FBL3N_real['Amount in doc. curr.']).astype(str)
        
        FBL3N_real['Counter1'] = FBL3N_real.groupby('Key1').cumcount()
        FBL3N_real['Counter1'] += 0 # Sumar 1 al contador para que comience desde 1 en lugar de 0
        FBL3N_real['Key_1'] = FBL3N_real['Key1'] + FBL3N_real['Counter1'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        FBL3N_real['Counter2'] = FBL3N_real.groupby('Key2').cumcount()
        FBL3N_real['Counter2'] += 0 # Contador para que comience desde 0
        FBL3N_real['Key_2'] = FBL3N_real['Key2'] + FBL3N_real['Counter2'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        
        FBL3N_real2 = FBL3N_real.copy()
        FBL3N_real2.columns = [col_name + '_k2' for col_name in FBL3N_real2]
        # FBL3N_real = FBL3N_real.merge(FBL3N_real2, left_on="Key1", right_on='Key2_k2', how='left')
        st.dataframe(FBL3N_real)
    
    end_time02 = time.time()
    processing_time02 = end_time02 - start_time02
    processing_time_formatted02 = "{:.4f}".format(processing_time02)
    st.info(f'Una vez generado el modelo, este fue aplicado en el nuevo conjunto de datos, asignando las categorías correspondientes en un tiempo total de: {processing_time_formatted02} segundos')

    if st.checkbox("Generar Archivo de Excel"):
        start_time03 = time.time()
        fecha_actual = datetime.datetime.now()
        formato = "%Y%m%d %H%M%S"  # Formato: Año-Mes-Día Hora-Minuto-Segundo
        fecha_formateada = fecha_actual.strftime(formato)
        
        # Crear un objeto de Pandas ExcelWriter y un buffer
        buffer = pd.ExcelWriter("output.xlsx", engine='openpyxl')
    
        # Escribir el DataFrame en la hoja de Excel
        FBL3N_real.to_excel(buffer, sheet_name='FBL3N', index=False)
        FBL3N_real2.to_excel(buffer, sheet_name='FBL3N_2', index=False)
        # Cerrar el Pandas Excel writer
        buffer.close()
    
        # Cargar el archivo Excel en un búfer base64 y crear un enlace de descarga
        with open("output.xlsx", "rb") as excel_file:
            b64 = base64.b64encode(excel_file.read()).decode()
    
        # Crear un enlace de descarga para el archivo Excel
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="FBL3N_{fecha_formateada}.xlsx">Download Excel File</a>'
    
        # Mostrar el enlace en Streamlit
        st.markdown(href, unsafe_allow_html=True)
        end_time03 = time.time()
        processing_time03 = end_time03 - start_time03
        processing_time_formatted03 = "{:.4f}".format(processing_time03)
        st.success(f'Archivo de Excel generado en un tiempo total de: {processing_time_formatted03} segundos')
