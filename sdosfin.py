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
    subtab1_GIMX, subtab2_GIMX = st.tabs(['PnL','Accounts'])    
    with subtab1_GIMX:
        if uploaded_GIMX and sheet_PnL_GIMX is not "Select" and sheet_AccBal_GIMX is not "Select":
            GIMX_PnL = load_sheet(uploaded_GIMX, sheet_PnL_GIMX)
            col_options_GIMX = GIMX_PnL.columns.tolist()
            col_options_GIMX.insert(0, "Select")
            col1_GIMX, col2_GIMX, col3_GIMX =st.columns([0.2, 0.2, 0.6])
            with col1_GIMX:
                col_desc_GIMX = st.selectbox("Select columns which contains GIMX P&L Description", col_options_GIMX)
                               
            with col2_GIMX:
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
            

    with subtab2_GIMX:
        if uploaded_GIMX and sheet_PnL_GIMX is not "Select":
            GIMX_Balances = load_sheet(uploaded_GIMX, sheet_AccBal_GIMX)
            cols_acc_bal_GIMX = GIMX_Balances.columns.tolist()
            cols_acc_bal_GIMX.insert(0, "Select")
            
            col1_GIMX, col2_GIMX, col3_GIMX, col4_GIMX = st.columns(4)
            with col1_GIMX:
                col_cuenta_GIMX = st.selectbox("Select the column which contains GIMX - Cuenta", cols_acc_bal_GIMX)
            with col2_GIMX:
                col_clasificacion_GIMX = st.selectbox("Select the column which contains GIMX - Clasificacion", cols_acc_bal_GIMX)
            with col3_GIMX:
                col_rubro_GIMX = st.selectbox("Select the column which contains GIMX - Rubro", cols_acc_bal_GIMX)
            with col4_GIMX:
                col_saldo_GIMX = st.selectbox("Select the column which contains GIMX - Saldo", cols_acc_bal_GIMX)
            
            if (col_cuenta_GIMX is not "Select") and (col_clasificacion_GIMX is not "Select") and (col_rubro_GIMX is not "Select") and (col_saldo_GIMX is not "Select"):
                GIMX_Balances.rename(columns={col_cuenta_GIMX: "Cuenta", col_clasificacion_GIMX: "Clasificacion", col_rubro_GIMX: "Rubro", col_saldo_GIMX: "Saldo"}, inplace=True)
                GIMX_Balances = GIMX_Balances[['Cuenta', 'Clasificacion', 'Rubro', 'Saldo']]
                GIMX_Balances = GIMX_Balances[(GIMX_Balances['Clasificacion'].isin(GIMX_Clasificacion)) & (GIMX_Balances['Saldo'] != 0)]
                
                
                Total_Income_Balance = GIMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(GIMX_Balances)
            else:
                st.dataframe(GIMX_Balances)
            










with tab2:
    subtab1_GSMX, subtab2_GSMX = st.tabs(['PnL','Accounts'])    
    with subtab1_GSMX:
        if uploaded_GSMX and sheet_PnL_GSMX is not "Select" and sheet_AccBal_GSMX is not "Select":
            GSMX_PnL = load_sheet(uploaded_GSMX, sheet_PnL_GSMX)
            col_options_GSMX = GSMX_PnL.columns.tolist()
            col_options_GSMX.insert(0, "Select")
            col1_GSMX, col2_GSMX, col3_GSMX =st.columns([0.2, 0.2, 0.6])
            with col1_GSMX:
                col_desc_GSMX = st.selectbox("Select columns which contains GSMX P&L Description", col_options_GSMX)
                               
            with col2_GSMX:
                col_balance_GSMX = st.selectbox("Select columns which contains GSMX P&L Balance", col_options_GSMX)
                
            if col_desc_GSMX is not "Select" and col_balance_GSMX is not "Select":
                GSMX_PnL.rename(columns={col_desc_GSMX: "Description", col_balance_GSMX: "Balance"}, inplace=True)
                GSMX_PnL = GIMX_PnL[['Description', 'Balance']]
                GSMX_PnL["Income Rows"] = ''
                GSMX_PnL['Balance'] = pd.to_numeric(GSMX_PnL['Balance'], errors='coerce')
                GSMX_PnL['Balance'] = GSMX_PnL['Balance'].astype(float)
                edited_GSMX = st.data_editor(GSMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                GSMX_PnL = edited_GSMX
                GSMX_PnL = GSMX_PnL[GSMX_PnL['Income Rows'] == "True"]
                GSMX_Clasificacion = GSMX_PnL['Description'].unique()
    
                Total_Income = GSMX_PnL["Balance"].sum()
                Total_Income = "{:,.2f}".format(Total_Income)
                st.metric(label="Total Income", value=Total_Income)
        
                
                st.dataframe(GSMX_PnL)
            else:
                st.dataframe(GSMX_PnL)
            

    with subtab2_GSMX:
        if uploaded_GSMX and sheet_PnL_GSMX is not "Select":
            GSMX_Balances = load_sheet(uploaded_GSMX, sheet_AccBal_GSMX)
            cols_acc_bal_GSMX = GSMX_Balances.columns.tolist()
            cols_acc_bal_GSMX.insert(0, "Select")
            
            col1_GSMX, col2_GSMX, col3_GSMX, col4_GSMX = st.columns(4)
            with col1_GSMX:
                col_cuenta_GSMX = st.selectbox("Select the column which contains GSMX - Cuenta", cols_acc_bal_GSMX)
            with col2_GSMX:
                col_clasificacion_GSMX = st.selectbox("Select the column which contains GSMX - Clasificacion", cols_acc_bal_GSMX)
            with col3_GSMX:
                col_rubro_GSMX = st.selectbox("Select the column which contains GSMX - Rubro", cols_acc_bal_GSMX)
            with col4_GSMX:
                col_saldo_GSMX = st.selectbox("Select the column which contains GSMX - Saldo", cols_acc_bal_GSMX)
            
            if (col_cuenta_GSMX is not "Select") and (col_clasificacion_GSMX is not "Select") and (col_rubro_GSMX is not "Select") and (col_saldo_GSMX is not "Select"):
                GSMX_Balances.rename(columns={col_cuenta_GSMX: "Cuenta", col_clasificacion_GSMX: "Clasificacion", col_rubro_GSMX: "Rubro", col_saldo_GSMX: "Saldo"}, inplace=True)
                GSMX_Balances = GSMX_Balances[['Cuenta', 'Clasificacion', 'Rubro', 'Saldo']]
                GSMX_Balances = GSMX_Balances[(GSMX_Balances['Clasificacion'].isin(GSMX_Clasificacion)) & (GSMX_Balances['Saldo'] != 0)]
                
                
                Total_Income_Balance = GSMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(GSMX_Balances)
            else:
                st.dataframe(GSMX_Balances)
            
