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

import streamlit as st
import pandas as pd

# Función para cargar el DataFrame desde el archivo Excel
@st.cache
def load_data(file):
    df = pd.read_excel(file, sheet_name='FBL3N')
    return df

# Función para aplicar filtros
@st.cache
def apply_filters(df, company_code, related_party):
    if company_code:
        df = df[df['Company Code'] == company_code]
    if related_party:
        df = df[df['Related Party'] == related_party]
    return df

# Cargar el archivo Excel
file = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if file is not None:
    # Cargar el DataFrame desde el archivo Excel
    df = load_data(file)

    # Obtener los valores únicos de las columnas "Company Code" y "Related Party"
    unique_company_codes = df['Company Code'].unique()
    unique_related_parties = df['Related Party'].unique()

    # Filtros
    company_code_filter = st.multiselect("Seleccionar Company Code:", unique_company_codes)
    related_party_filter = st.multiselect("Seleccionar Related Party:", unique_related_parties)

    # Aplicar filtros
    filtered_df = apply_filters(df, company_code_filter, related_party_filter)

    # Mostrar el DataFrame filtrado
    st.dataframe(filtered_df)











# #------------------ OLD CODE ---------------------#
# # Definir una función para cargar el archivo y preprocesarlo
# def load_FBL3N(uploaded_file):
#     FBL3N_classified = pd.read_excel(uploaded_file, engine='openpyxl', sheet_name='FBL3N', dtype={'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str})
#     return FBL3N_classified

# # Definir una función para filtrar el DataFrame en función de las selecciones
# # def filter_dataframe(FBL3N_full, selected_company_code, selected_related_party, selected_document_date):
# #     filtered_df = FBL3N_full[(FBL3N_full['Company Code'] == selected_company_code) & (FBL3N_full['Related Party'] == selected_related_party) & (FBL3N_full['Document Date'] == selected_document_date)]
# #     return filtered_df


# uploaded_FBL3N_classified = st.file_uploader("Carga el archivo FBL3N mas actualizado que contenga la clasificación de los movimientos para poder entrenar el modelo de ML", type=["xlsx"], accept_multiple_files=False)

# # Inicializar o cargar el DataFrame en st.session_state
# if 'FBL3N_classified' not in st.session_state:
#     st.session_state.FBL3N_classified = None

# if st.session_state.FBL3N_classified is None and uploaded_FBL3N_classified is not None:
#     st.session_state.FBL3N_classified = load_FBL3N(uploaded_FBL3N_classified)

# if st.session_state.FBL3N_classified is not None:

#     selected_company_code = st.selectbox("Selecciona el Company Code", options=st.session_state.FBL3N_classified['Company Code'].unique())
#     # selected_related_party = st.selectbox("Selecciona el Related Party", options=FBL3N_classified['Related Party'].unique(),)
#     # filtered_df = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Related Party'] == selected_related_party]
#     st.session_state.FBL3N_classified = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Company Code'] == selected_company_code]
#     st.dataframe(st.session_state.FBL3N_classified)

    
#     # # Calcular la suma de las filas seleccionadas
#     # selected_rows = filtered_df[filtered_df['Checkbox']]
#     # total_sum = selected_rows['Amount in doc. curr.'].sum()  # Reemplaza 'TuColumnaNumerica' con el nombre real de la columna que deseas sumar

#     # # Mostrar el DataFrame filtrado
    
#     # st.write(f"Suma de las filas seleccionadas: {total_sum}")
