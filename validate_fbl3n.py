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
# import pygwalker as pyg
# import streamlit.components.v1 as components
# from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html



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
@st.cache_data
def load_data(file):
    FBL3N_classified = pd.read_excel(file, sheet_name='FBL3N')
    return FBL3N_classified

# Función para aplicar filtros
@st.cache_data
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
    st.write(company_code_filter)
    # Aplicar filtros
    # filtered_FBL3N_classified = apply_filters(FBL3N_classified, company_code_filter, related_party_filter)
    # filtered_FBL3N_classified = FBL3N_classified[FBL3N_classified['Company Code'].isin(company_code_filter)]
    filtered_FBL3N_classified = FBL3N_classified[(FBL3N_classified['Company Code'].isin(company_code_filter)) & (FBL3N_classified['Related Party'].isin(related_party_filter))]
    merged_FBL3N_classified = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=(' sell', ' purchase'))
    st.write(merged_FBL3N_classified.columns)
    merged_FBL3N_classified = merged_FBL3N_classified[(merged_FBL3N_classified['Company Code sell'].isin(company_code_filter)) & (merged_FBL3N_classified['Company Code purchase'].isin(related_party_filter))]
    
    columns_to_eliminate = ['CONCAT sell', 'Subcode 2 sell', 'Document Date sell', 'Amount in local currency sell', 'Local Currency sell', 'Key_1 sell', 'Key_2 sell', 'CONCAT purchase', 'Document Date purchase', 'Amount in local currency purchase', 'Local Currency purchase', 'Key_1 purchase', 'Key_2 purchase', 'Subcode 2 purchase']
    merged_FBL3N_classified = merged_FBL3N_classified.drop(columns=columns_to_eliminate)
    
    # Mostrar el DataFrame filtrado
    st.dataframe(filtered_FBL3N_classified)
    st.dataframe(merged_FBL3N_classified)
    st.dataframe(
       merged_FBL3N_classified, 
       show_header=True,  
       show_index=True,
    
       header_cell_color= "blue",  
       header_font_color="white",
    
       rows_font_color="black",
       even_row_cell_color="white",
       odd_row_cell_color="lightblue",
    
       columns_with_header_style=[0],  # which rows must be shown using header style, [0] = df.index if show_index==True
       rows_with_header_style=[0],  # same for rows, [0] = header if show_index=True
    
       columns_with_bold_font=[],  # font text in bold for these rows and columns: 
       rows_with_bold_font=[],   # used to highlight special rows and cols such as "average", "median", etc.
    
       max_row_number=None,   # if set, create pagination
    
       format_decimals=2,   # more complex formats should be managed in df
       invalid_numbers_representation="-",  # if set, non-numbers like pd.NA, np.nan, None are visualized using this string
    
       ...
    )



    # pyg_html = pyg.walk(filtered_FBL3N_classified, return_html=True)
    # components.html = (pyg_html)
    
