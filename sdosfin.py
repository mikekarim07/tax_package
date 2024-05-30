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
    page_title="Tax Package - Financial Statements",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)


st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=120)
# st.header('Machine Learnig Model')
st.subheader('Tax Package - Saldos Financieros')

# st.divider()

@st.cache_data
def get_sheet_names(file):
    # Leer todas las hojas del archivo y devolver sus nombres
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    return excel_file.sheet_names

@st.cache_data
def load_sheet(file, sheet_name, dtype):
    # Leer una hoja específica del archivo de Excel
    return pd.read_excel(file, engine='openpyxl', sheet_name=sheet_name, dtype=dtype)



uploaded_GIMX = st.sidebar.file_uploader("Upload GIMX Financial Statements", type=["xlsx"])
if uploaded_GIMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_GIMX = get_sheet_names(uploaded_GIMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_GIMX.insert(0, "Select")
    sheet_GIMX = st.sidebar.selectbox("Select the sheet which contains GIMX P&L", sheet_names_GIMX)
st.sidebar.divider()

uploaded_GSMX = st.sidebar.file_uploader("Upload GSMX Financial Statements", type=["xlsx"])
if uploaded_GSMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_GSMX = get_sheet_names(uploaded_GSMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_GSMX.insert(0, "Select")
    sheet_GSMX = st.sidebar.selectbox("Select the sheet which contains GSMX P&L", sheet_names_GSMX)
st.sidebar.divider()

uploaded_KCMX = st.sidebar.file_uploader("Upload KCMX Financial Statements", type=["xlsx"])
if uploaded_RepPagos is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_KCMX = get_sheet_names(uploaded_KCMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_KCMX.insert(0, "Select")
    sheet_KCMX = st.sidebar.selectbox("Select the sheet which contains KCMX P&L", sheet_names_KCMX)
st.sidebar.divider()

uploaded_KLMX = st.sidebar.file_uploader("Upload KLMX Financial Statements", type=["xlsx"])
if uploaded_RepPagos is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_KLMX = get_sheet_names(uploaded_KLMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_KLMX.insert(0, "Select")
    sheet_KLMX = st.sidebar.selectbox("Select the sheet which contains KLMX P&L", sheet_names_KLMX)
st.sidebar.divider()

uploaded_PRMX = st.sidebar.file_uploader("Upload PRMX Financial Statements", type=["xlsx"])
if uploaded_RepPagos is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_PRMX = get_sheet_names(uploaded_PRMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_PRMX.insert(0, "Select")
    sheet_PRMX = st.sidebar.selectbox("Select the sheet which contains PRMX P&L", sheet_names_PRMX)
st.sidebar.divider()













# tab1, tab2, tab3, tab4, tab5 = = st.tabs(["GIMX", "GSMX", "KCMX", "KLMX", "PRMX"])

# with tab1:
#     col1_gimx, col2_gimx, col3_gimx, col4_gimx, col5_gimx = st.columns(5)
#         with col1_gimx:
#             uploaded_GIMX = st.file_uploader("Upload Balances Reporte de Pagos", type=["xlsx"])
#             st.divider()
            
    
    
    
#     uploaded_GIMX = st.sidebar.file_uploader("Carga el Reporte de Pagos", type=["xlsx"])
#     if uploaded_RepPagos is not None:
#         # Obtener nombres de las hojas del archivo
#         sheet_names_pagos = get_sheet_names(uploaded_RepPagos)
        
#         # Seleccionar la hoja de Excel
#         sheet_Rep_pagos = st.sidebar.selectbox("Seleccionar hoja del reporte de pagos que contiene los datos para procesar", sheet_names_pagos)
#     st.sidebar.divider()
