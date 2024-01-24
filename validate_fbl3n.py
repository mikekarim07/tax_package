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

# Función para cargar el DataFrame desde el archivo Excel
@st.cache
def load_data(file):
    FBL3N_classified = pd.read_excel(file, sheet_name='FBL3N')
    return FBL3N_classified

# Función para aplicar filtros
@st.cache
def apply_filters(FBL3N_classified, company_codes, related_parties):
    if company_codes:
        FBL3N_classified = FBL3N_classified[FBL3N_classified['Company Code'].isin(company_codes)]
    if related_parties:
        FBL3N_classified = FBL3N_classified[FBL3N_classified['Related Party'].isin(related_parties)]
    return FBL3N_classified

# Cargar el archivo Excel
file = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if file is not None:
    # Cargar el DataFrame desde el archivo Excel
    FBL3N_classified = load_data(file)

    # Obtener los valores únicos de las columnas "Company Code" y "Related Party"
    unique_company_codes = FBL3N_classified['Company Code'].unique()
    unique_related_parties = FBL3N_classified['Related Party'].unique()

    # Filtros
    company_code_filter = st.sidebar.multiselect("Seleccionar Company Code:", unique_company_codes)
    related_party_filter = st.sidebar.multiselect("Seleccionar Related Party:", unique_related_parties)

    # Aplicar filtros
    filtered_FBL3N_classified = apply_filters(FBL3N_classified, company_code_filter, related_party_filter)
    merged_FBL3N_classified = filtered_FBL3N_classified.merge(filtered_FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer')
    # merged_FBL3N_classified = pd.merge(filtered_FBL3N_classified, filtered_FBL3N_classified, left_on=Key_1, right_on=Key_2, suffixes=('_1', '_2'))
    # Mostrar el DataFrame filtrado
    st.dataframe(filtered_FBL3N_classified)
    st.dataframe(merged_FBL3N_classified)

