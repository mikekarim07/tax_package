import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
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
    page_title="Tax Package Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)



st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=120)
# st.header('Tax Package Model')
st.subheader('Related Party Operations validations')

# Definir una función para cargar el archivo y preprocesarlo
def load_FBL3N(uploaded_file):
    FBL3N_classified = pd.read_excel(uploaded_file, engine='openpyxl', sheet_name='FBL3N', dtype={'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str})
    return FBL3N_classified

# Definir una función para filtrar el DataFrame en función de las selecciones
def filter_dataframe(FBL3N_full, selected_company_code, selected_related_party, selected_document_date):
    filtered_df = FBL3N_full[(FBL3N_full['Company Code'] == selected_company_code) & (FBL3N_full['Related Party'] == selected_related_party) & (FBL3N_full['Document Date'] == selected_document_date)]
    return filtered_df


uploaded_FBL3N_classified = st.file_uploader("Carga el archivo FBL3N mas actualizado que contenga la clasificación de los movimientos para poder entrenar el modelo de ML", type=["xlsx"], accept_multiple_files=False)

# Inicializar o cargar el DataFrame en st.session_state
if 'FBL3N_classified' not in st.session_state:
    st.session_state.FBL3N_classified = None

if st.session_state.FBL3N_classified is None and uploaded_FBL3N_classified is not None:
    st.session_state.FBL3N_classified = load_FBL3N(uploaded_FBL3N_classified)

if st.session_state.FBL3N_full is not None:
    col1, col2, col3 = st.columns(3)

    # Agregar un st.selectbox para seleccionar 'Company Code'
    with col1:
        selected_company_code = st.selectbox("Selecciona el Company Code", st.session_state.FBL3N_classified['Company Code'].unique())
        # selected_company_code = st.multiselect("Selecciona los Company Codes", options=st.session_state.FBL3N_classified['Company Code'].unique(),)

    # Agregar un st.selectbox para seleccionar 'Related Party'
    with col2:
        selected_related_party = st.selectbox("Selecciona el Related Party", options=st.session_state.FBL3N_classified['Related Party'].unique(),)

    filtered_df = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Company Code'] == selected_company_code]
    filtered_df = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Related Party'] == selected_related_party]

    # Obtener las fechas únicas que cumplen con los filtros
    # unique_dates = filtered_df['Document Date'].unique()

    # Agregar un st.selectbox para seleccionar 'Document Date' basado en las fechas únicas
    # with col3:
    #     selected_document_date = st.selectbox("Selecciona la Document Date", unique_dates)

    # # filtered_df = filtered_df[filtered_df['Document Date'] == selected_document_date]
    # filtered_df['Checkbox'] = [False] * len(filtered_df)
    # filtered_df = st.data_editor(filtered_df)
    # # Mostrar el DataFrame filtrado
    st.dataframe(filtered_df)

    
    # # Calcular la suma de las filas seleccionadas
    # selected_rows = filtered_df[filtered_df['Checkbox']]
    # total_sum = selected_rows['Amount in doc. curr.'].sum()  # Reemplaza 'TuColumnaNumerica' con el nombre real de la columna que deseas sumar

    # # Mostrar el DataFrame filtrado
    
    # st.write(f"Suma de las filas seleccionadas: {total_sum}")
