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
st.subheader('Tax Package - Financial Statements Consolidation for Tax Package')

# st.divider()

@st.cache_data
def get_sheet_names(file):
    # Leer todas las hojas del archivo y devolver sus nombres
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    return excel_file.sheet_names

@st.cache_data
def load_sheet(file, sheet_name):
    # Leer una hoja específica del archivo de Excel
    return pd.read_excel(file, engine='openpyxl', sheet_name=sheet_name, header=None)



uploaded_GIMX = st.sidebar.file_uploader("Upload GIMX Financial Statements", type=["xlsx"])
if uploaded_GIMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_GIMX = get_sheet_names(uploaded_GIMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_GIMX.insert(0, "Select")
    sheet_PnL_GIMX = st.sidebar.selectbox("Select the sheet which contains GIMX P&L", sheet_names_GIMX)
    sheet_AccBal_GIMX = st.sidebar.selectbox("Select the sheet which contains GIMX Account Balances", sheet_names_GIMX)
st.sidebar.divider()

uploaded_GSMX = st.sidebar.file_uploader("Upload GSMX Financial Statements", type=["xlsx"])
if uploaded_GSMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_GSMX = get_sheet_names(uploaded_GSMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_GSMX.insert(0, "Select")
    sheet_PnL_GSMX = st.sidebar.selectbox("Select the sheet which contains GSMX P&L", sheet_names_GSMX)
    sheet_AccBal_GSMX = st.sidebar.selectbox("Select the sheet which contains GSMX Account Balances", sheet_names_GSMX)
st.sidebar.divider()

uploaded_KCMX = st.sidebar.file_uploader("Upload KCMX Financial Statements", type=["xlsx"])
if uploaded_KCMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_KCMX = get_sheet_names(uploaded_KCMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_KCMX.insert(0, "Select")
    sheet_KCMX = st.sidebar.selectbox("Select the sheet which contains KCMX P&L", sheet_names_KCMX)
    sheet_AccBal_KCMX = st.sidebar.selectbox("Select the sheet which contains KCMX Account Balances", sheet_names_KCMX)
st.sidebar.divider()

uploaded_KLMX = st.sidebar.file_uploader("Upload KLMX Financial Statements", type=["xlsx"])
if uploaded_KLMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_KLMX = get_sheet_names(uploaded_KLMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_KLMX.insert(0, "Select")
    sheet_KLMX = st.sidebar.selectbox("Select the sheet which contains KLMX P&L", sheet_names_KLMX)
    sheet_AccBal_KLMX = st.sidebar.selectbox("Select the sheet which contains KLMX Account Balances", sheet_names_KLMX)
st.sidebar.divider()

uploaded_PRMX = st.sidebar.file_uploader("Upload PRMX Financial Statements", type=["xlsx"])
if uploaded_PRMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_PRMX = get_sheet_names(uploaded_PRMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_PRMX.insert(0, "Select")
    sheet_PRMX = st.sidebar.selectbox("Select the sheet which contains PRMX P&L", sheet_names_PRMX)
    sheet_AccBal_PRMX = st.sidebar.selectbox("Select the sheet which contains PRMX Account Balances", sheet_names_PRMX)
st.sidebar.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["GIMX", "GSMX", "KCMX", "KLMX", "PRMX"])

with tab1:
    subtab1, subtab2 = st.tabs(['PnL','Accounts'])    
    with subtab1:
        if uploaded_GIMX and sheet_PnL_GIMX is not "Select" and sheet_AccBal_GIMX is not "Select":
            GIMX_PnL = load_sheet(uploaded_GIMX, sheet_PnL_GIMX)
            col_options_GIMX = GIMX_PnL.columns.tolist()
            col_options_GIMX.insert(0, "Select")
            col1, col2, col3 =st.columns([0.2, 0.2, 0.6])
            with col1:
                col_desc_GIMX = st.selectbox("Select columns which contains GIMX P&L Description", col_options_GIMX)
                               
            with col2:
                col_balance_GIMX = st.selectbox("Select columns which contains GIMX P&L Balance", col_options_GIMX)
                
            if col_desc_GIMX is not "Select" and col_balance_GIMX is not "Select":
                GIMX_PnL.rename(columns={col_desc_GIMX: "Description", col_balance_GIMX: "Balance"}, inplace=True)
                GIMX_PnL = GIMX_PnL[['Description', 'Balance']]
                GIMX_PnL["Income Rows"] = ''
                GIMX_PnL['Balance'] = pd.to_numeric(GIMX_PnL['Balance'], errors='coerce')
                GIMX_PnL['Balance'] = GIMX_PnL['Balance'].astype(float)
                edited_GIMX = st.data_editor(GIMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                GIMX_PnL = edited_GIMX
                GIMX_PnL = GIMX_PnL[GIMX_PnL['Income Rows'] == "True"]
                GIMX_Clasificacion = GIMX_PnL['Description'].unique()
    
                Total_Income = GIMX_PnL["Balance"].sum()
                Total_Income = "{:,.2f}".format(Total_Income)
                st.metric(label="Total Income", value=Total_Income)
        
                
                st.dataframe(GIMX_PnL)
            else:
                st.dataframe(GIMX_PnL)
            

    with subtab2:
        if uploaded_GIMX and sheet_PnL_GIMX is not "Select":
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                
                GIMX_Balances = load_sheet(uploaded_GIMX, sheet_AccBal_GIMX)
            with col2:
                col_cuenta_GIMX = st.number_input("Ingresa el numero de columna que contiene la Cuenta de GIMX", step=1)
            with col3:
                col_clasificacion_GIMX = st.number_input("Ingresa el numero de columna que contiene la clasificacion de GIMX", step=1)
            with col4:
                col_rubro_GIMX = st.number_input("Ingresa el numero de columna que contiene el rubro de GIMX", step=1)
            with col5:
                col_saldo_GIMX = st.number_input("Ingresa el numero de columna que contiene el saldo de la cuenta de GIMX", step=1)
            if (col_cuenta_GIMX is not col_clasificacion_GIMX) and (col_cuenta_GIMX is not col_rubro_GIMX) and (col_cuenta_GIMX is not col_saldo_GIMX):
                GIMX_Balances = GIMX_Balances.iloc[:, [col_cuenta_GIMX, col_clasificacion_GIMX, col_rubro_GIMX, col_saldo_GIMX]]
                GIMX_Balances = GIMX_Balances.rename(columns={GIMX_Balances.columns[col_cuenta_GIMX]: 'Cuenta', GIMX_Balances.columns[col_clasificacion_GIMX]: 'Clasificacion', GIMX_Balances.columns[col_rubro_GIMX]: 'Rubro', GIMX_Balances.columns[col_saldo_GIMX]: 'Saldo'})
                GIMX_Balances = GIMX_Balances[(GIMX_Balances['Clasificacion'].isin(GIMX_Clasificacion)) & (GIMX_Balances['Saldo'] != 0)]
                
                
                Total_Income_Balance = GIMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(GIMX_Balances)
            else:
                st.dataframe(GIMX_Balances)
            
            














# with tab2:
#     subtab1, subtab2 = st.tabs(['PnL','Accounts'])
#     with subtab1:
#         if uploaded_GSMX and sheet_PnL_GSMX is not "Select":
#             GSMX_PnL = load_sheet(uploaded_GSMX, sheet_PnL_GSMX)
#             col_options = GSMX_PnL.columns.tolist()
#             selected_columns = st.multiselect("Selecciona las columnas que quieres usar", col_options)
#             if selected_columns:
#             # Filtrar las columnas seleccionadas
#                 GSMX_PnL = GSMX_PnL[selected_columns]
#             st.dataframe(GSMX_PnL)
#     #         col1, col2, col3 =st.columns([0.2, 0.2, 0.6])
#     #         with col1:
            
#     #             col_desc_GSMX = st.number_input("Ingresa el numero de columna que contiene los Conceptos de Ingresos de GSMX", step=1)
#     #         with col2:
#     #             col_balance_GSMX = st.number_input("Ingresa el numero de columna que contiene el saldo final de GSMX", step=1)
                
#     #         if col_desc_GSMX is not col_balance_GSMX:
                
#     #             GSMX_PnL = GSMX_PnL.iloc[:, [col_desc_GSMX, col_balance_GSMX]]
#     #             GSMX_PnL = GSMX_PnL.rename(columns={GSMX_PnL.columns[col_desc_GSMX]: 'Description', GSMX_PnL.columns[col_balance_GSMX]: 'Balance'})
        
#     #             GSMX_PnL["Income Rows"] = ''
#     #             GSMX_PnL['Balance'] = pd.to_numeric(GSMX_PnL['Balance'], errors='coerce')
#     #             GSMX_PnL['Balance'] = GSMX_PnL['Balance'].astype(float)
#     #             edited_GSMX = st.data_editor(GSMX_PnL, column_config={
#     #                         "Income Rows": st.column_config.CheckboxColumn(default=False)
#     #                     }, disabled=["Description", "Balance"], hide_index=True)
        
                
#     #             GSMX_PnL = edited_GSMX
#     #             GSMX_PnL = GSMX_PnL[GSMX_PnL['Income Rows'] == "True"]
#     #             GSMX_Clasificacion = GSMX_PnL['Description'].unique()
    
#     #             Total_Income = GSMX_PnL["Balance"].sum()
#     #             Total_Income = "{:,.2f}".format(Total_Income)
#     #             st.metric(label="Total Income", value=Total_Income)
        
                
#     #             st.dataframe(GSMX_PnL)
#     #         else:
#     #             st.dataframe(GSMX_PnL)
            

#     # with subtab2:
#     #     if uploaded_GSMX and sheet_PnL_GSMX is not "Select":
#     #         col1, col2, col3, col4, col5 = st.columns(5)
#     #         with col1:
#     #             sheet_AccBal_GSMX = st.selectbox("Select the sheet which contains GSMX Account Balances", sheet_names_GSMX)
#     #             GSMX_Balances = load_sheet(uploaded_GSMX, sheet_AccBal_GSMX)
#     #         with col2:
#     #             col_cuenta_GSMX = st.number_input("Ingresa el numero de columna que contiene la Cuenta de GSMX", step=1)
#     #         with col3:
#     #             col_clasificacion_GSMX = st.number_input("Ingresa el numero de columna que contiene la clasificacion de GSMX", step=1)
#     #         with col4:
#     #             col_rubro_GSMX = st.number_input("Ingresa el numero de columna que contiene el rubro de GSMX", step=1)
#     #         with col5:
#     #             col_saldo_GSMX = st.number_input("Ingresa el numero de columna que contiene el saldo de la cuenta de GSMX", step=1)
#     #         if (col_cuenta_GSMX is not col_clasificacion_GSMX) and (col_cuenta_GSMX is not col_rubro_GSMX) and (col_cuenta_GSMX is not col_saldo_GSMX):
#     #             GSMX_Balances = GSMX_Balances.iloc[:, [col_cuenta_GSMX, col_clasificacion_GSMX, col_rubro_GSMX, col_saldo_GSMX]]
#     #             GSMX_Balances = GSMX_Balances.rename(columns={GSMX_Balances.columns[col_cuenta_GSMX]: 'Cuenta', GSMX_Balances.columns[col_clasificacion_GSMX]: 'Clasificacion', GSMX_Balances.columns[col_rubro_GSMX]: 'Rubro', GSMX_Balances.columns[col_saldo_GSMX]: 'Saldo'})
#     #             GSMX_Balances = GSMX_Balances[(GSMX_Balances['Clasificacion'].isin(GSMX_Clasificacion)) & (GSMX_Balances['Saldo'] != 0)]
                
                
#     #             Total_Income_Balance = GSMX_Balances["Saldo"].sum()
#     #             Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
#     #             st.metric(label="Total Income", value=Total_Income_Balance)
                
#     #             st.dataframe(GSMX_Balances)
#     #         else:
#     #             st.dataframe(GSMX_Balances)

