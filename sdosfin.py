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
    sheet_PnL_KCMX = st.sidebar.selectbox("Select the sheet which contains KCMX P&L", sheet_names_KCMX)
    sheet_AccBal_KCMX = st.sidebar.selectbox("Select the sheet which contains KCMX Account Balances", sheet_names_KCMX)
st.sidebar.divider()

uploaded_KLMX = st.sidebar.file_uploader("Upload KLMX Financial Statements", type=["xlsx"])
if uploaded_KLMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_KLMX = get_sheet_names(uploaded_KLMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_KLMX.insert(0, "Select")
    sheet_PnL_KLMX = st.sidebar.selectbox("Select the sheet which contains KLMX P&L", sheet_names_KLMX)
    sheet_AccBal_KLMX = st.sidebar.selectbox("Select the sheet which contains KLMX Account Balances", sheet_names_KLMX)
st.sidebar.divider()

uploaded_PRMX = st.sidebar.file_uploader("Upload PRMX Financial Statements", type=["xlsx"])
if uploaded_PRMX is not None:
    # Obtener nombres de las hojas del archivo
    sheet_names_PRMX = get_sheet_names(uploaded_PRMX)
    
    # Seleccionar la hoja de Excel
    sheet_names_PRMX.insert(0, "Select")
    sheet_PnL_PRMX = st.sidebar.selectbox("Select the sheet which contains PRMX P&L", sheet_names_PRMX)
    sheet_AccBal_PRMX = st.sidebar.selectbox("Select the sheet which contains PRMX Account Balances", sheet_names_PRMX)
st.sidebar.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["GIMX", "GSMX", "KCMX", "KLMX", "PRMX", "All CoCodes"])

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
                GIMX_PnL['Description'] = GIMX_PnL['Description'].str.lower()
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
                GIMX_Balances['Clasificacion'] = GIMX_Balances['Clasificacion'].str.lower()
                GIMX_Balances = GIMX_Balances[(GIMX_Balances['Clasificacion'].isin(GIMX_Clasificacion)) & (GIMX_Balances['Saldo'] != 0)]
                GIMX_Balances['Co_Cd'] = "GIMX"
                
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
                GSMX_PnL = GSMX_PnL[['Description', 'Balance']]
                GSMX_PnL["Income Rows"] = ''
                GSMX_PnL['Balance'] = pd.to_numeric(GSMX_PnL['Balance'], errors='coerce')
                GSMX_PnL['Balance'] = GSMX_PnL['Balance'].astype(float)
                edited_GSMX = st.data_editor(GSMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                GSMX_PnL = edited_GSMX
                GSMX_PnL = GSMX_PnL[GSMX_PnL['Income Rows'] == "True"]
                GSMX_PnL['Description'] = GSMX_PnL['Description'].str.lower()
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
                GSMX_Balances['Clasificacion'] = GSMX_Balances['Clasificacion'].str.lower()
                GSMX_Balances = GSMX_Balances[(GSMX_Balances['Clasificacion'].isin(GSMX_Clasificacion)) & (GSMX_Balances['Saldo'] != 0)]
                GSMX_Balances['Co_Cd'] = "GSMX"
                
                Total_Income_Balance = GSMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(GSMX_Balances)
            else:
                st.dataframe(GSMX_Balances)
            









with tab3:
    subtab1_KCMX, subtab2_KCMX = st.tabs(['PnL','Accounts'])    
    with subtab1_KCMX:
        if uploaded_KCMX and sheet_PnL_KCMX is not "Select" and sheet_AccBal_KCMX is not "Select":
            KCMX_PnL = load_sheet(uploaded_KCMX, sheet_PnL_KCMX)
            col_options_KCMX = KCMX_PnL.columns.tolist()
            col_options_KCMX.insert(0, "Select")
            col1_KCMX, col2_KCMX, col3_KCMX =st.columns([0.2, 0.2, 0.6])
            with col1_KCMX:
                col_desc_KCMX = st.selectbox("Select columns which contains KCMX P&L Description", col_options_KCMX)
                               
            with col2_KCMX:
                col_balance_KCMX = st.selectbox("Select columns which contains KCMX P&L Balance", col_options_KCMX)
                
            if col_desc_KCMX is not "Select" and col_balance_KCMX is not "Select":
                KCMX_PnL.rename(columns={col_desc_KCMX: "Description", col_balance_KCMX: "Balance"}, inplace=True)
                KCMX_PnL = KCMX_PnL[['Description', 'Balance']]
                KCMX_PnL["Income Rows"] = ''
                KCMX_PnL['Balance'] = pd.to_numeric(KCMX_PnL['Balance'], errors='coerce')
                KCMX_PnL['Balance'] = KCMX_PnL['Balance'].astype(float)
                edited_KCMX = st.data_editor(KCMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                KCMX_PnL = edited_KCMX
                KCMX_PnL = KCMX_PnL[KCMX_PnL['Income Rows'] == "True"]
                KCMX_PnL['Description'] = KCMX_PnL['Description'].str.lower()
                KCMX_Clasificacion = KCMX_PnL['Description'].unique()
                    
                Total_Income = KCMX_PnL["Balance"].sum()
                Total_Income = "{:,.2f}".format(Total_Income)
                st.metric(label="Total Income", value=Total_Income)
        
                
                st.dataframe(KCMX_PnL)
            else:
                st.dataframe(KCMX_PnL)
            

    with subtab2_KCMX:
        if uploaded_KCMX and sheet_PnL_KCMX is not "Select":
            KCMX_Balances = load_sheet(uploaded_KCMX, sheet_AccBal_KCMX)
            cols_acc_bal_KCMX = KCMX_Balances.columns.tolist()
            cols_acc_bal_KCMX.insert(0, "Select")
            
            col1_KCMX, col2_KCMX, col3_KCMX, col4_KCMX = st.columns(4)
            with col1_KCMX:
                col_cuenta_KCMX = st.selectbox("Select the column which contains KCMX - Cuenta", cols_acc_bal_KCMX)
            with col2_KCMX:
                col_clasificacion_KCMX = st.selectbox("Select the column which contains KCMX - Clasificacion", cols_acc_bal_KCMX)
            with col3_KCMX:
                col_rubro_KCMX = st.selectbox("Select the column which contains KCMX - Rubro", cols_acc_bal_KCMX)
            with col4_KCMX:
                col_saldo_KCMX = st.selectbox("Select the column which contains KCMX - Saldo", cols_acc_bal_KCMX)
            
            if (col_cuenta_KCMX is not "Select") and (col_clasificacion_KCMX is not "Select") and (col_rubro_KCMX is not "Select") and (col_saldo_KCMX is not "Select"):
                KCMX_Balances.rename(columns={col_cuenta_KCMX: "Cuenta", col_clasificacion_KCMX: "Clasificacion", col_rubro_KCMX: "Rubro", col_saldo_KCMX: "Saldo"}, inplace=True)
                KCMX_Balances = KCMX_Balances[['Cuenta', 'Clasificacion', 'Rubro', 'Saldo']]
                KCMX_Balances['Clasificacion'] = KCMX_Balances['Clasificacion'].str.lower()
                KCMX_Balances = KCMX_Balances[(KCMX_Balances['Clasificacion'].isin(KCMX_Clasificacion)) & (KCMX_Balances['Saldo'] != 0)]
                KCMX_Balances['Co_Cd'] = "KCMX"
                
                Total_Income_Balance = KCMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(KCMX_Balances)
            else:
                st.dataframe(KCMX_Balances)
            







with tab4:
    subtab1_KLMX, subtab2_KLMX = st.tabs(['PnL','Accounts'])    
    with subtab1_KLMX:
        if uploaded_KLMX and sheet_PnL_KLMX is not "Select" and sheet_AccBal_KLMX is not "Select":
            KLMX_PnL = load_sheet(uploaded_KLMX, sheet_PnL_KLMX)
            col_options_KLMX = KLMX_PnL.columns.tolist()
            col_options_KLMX.insert(0, "Select")
            col1_KLMX, col2_KLMX, col3_KLMX =st.columns([0.2, 0.2, 0.6])
            with col1_KLMX:
                col_desc_KLMX = st.selectbox("Select columns which contains KLMX P&L Description", col_options_KLMX)
                               
            with col2_KLMX:
                col_balance_KLMX = st.selectbox("Select columns which contains KLMX P&L Balance", col_options_KLMX)
                
            if col_desc_KLMX is not "Select" and col_balance_KLMX is not "Select":
                KLMX_PnL.rename(columns={col_desc_KLMX: "Description", col_balance_KLMX: "Balance"}, inplace=True)
                KLMX_PnL = KLMX_PnL[['Description', 'Balance']]
                KLMX_PnL["Income Rows"] = ''
                KLMX_PnL['Balance'] = pd.to_numeric(KLMX_PnL['Balance'], errors='coerce')
                KLMX_PnL['Balance'] = KLMX_PnL['Balance'].astype(float)
                edited_KLMX = st.data_editor(KLMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                KLMX_PnL = edited_KLMX
                KLMX_PnL = KLMX_PnL[KLMX_PnL['Income Rows'] == "True"]
                KLMX_PnL['Description'] = KLMX_PnL['Description'].str.lower()
                KLMX_Clasificacion = KLMX_PnL['Description'].unique()
    
                Total_Income = KLMX_PnL["Balance"].sum()
                Total_Income = "{:,.2f}".format(Total_Income)
                st.metric(label="Total Income", value=Total_Income)
        
                
                st.dataframe(KLMX_PnL)
            else:
                st.dataframe(KLMX_PnL)
            

    with subtab2_KLMX:
        if uploaded_KLMX and sheet_PnL_KLMX is not "Select":
            KLMX_Balances = load_sheet(uploaded_KLMX, sheet_AccBal_KLMX)
            cols_acc_bal_KLMX = KLMX_Balances.columns.tolist()
            cols_acc_bal_KLMX.insert(0, "Select")
            
            col1_KLMX, col2_KLMX, col3_KLMX, col4_KLMX = st.columns(4)
            with col1_KLMX:
                col_cuenta_KLMX = st.selectbox("Select the column which contains KLMX - Cuenta", cols_acc_bal_KLMX)
            with col2_KLMX:
                col_clasificacion_KLMX = st.selectbox("Select the column which contains KLMX - Clasificacion", cols_acc_bal_KLMX)
            with col3_KLMX:
                col_rubro_KLMX = st.selectbox("Select the column which contains KLMX - Rubro", cols_acc_bal_KLMX)
            with col4_KLMX:
                col_saldo_KLMX = st.selectbox("Select the column which contains KLMX - Saldo", cols_acc_bal_KLMX)
            
            if (col_cuenta_KLMX is not "Select") and (col_clasificacion_KLMX is not "Select") and (col_rubro_KLMX is not "Select") and (col_saldo_KLMX is not "Select"):
                KLMX_Balances.rename(columns={col_cuenta_KLMX: "Cuenta", col_clasificacion_KLMX: "Clasificacion", col_rubro_KLMX: "Rubro", col_saldo_KLMX: "Saldo"}, inplace=True)
                KLMX_Balances = KLMX_Balances[['Cuenta', 'Clasificacion', 'Rubro', 'Saldo']]
                KLMX_Balances['Clasificacion'] = KLMX_Balances['Clasificacion'].str.lower()
                KLMX_Balances = KLMX_Balances[(KLMX_Balances['Clasificacion'].isin(KLMX_Clasificacion)) & (KLMX_Balances['Saldo'] != 0)]
                KLMX_Balances['Co_Cd'] = "KLMX"
                
                Total_Income_Balance = KLMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(KLMX_Balances)
            else:
                st.dataframe(KLMX_Balances)
            






with tab5:
    subtab1_PRMX, subtab2_PRMX = st.tabs(['PnL','Accounts'])    
    with subtab1_PRMX:
        if uploaded_PRMX and sheet_PnL_PRMX is not "Select" and sheet_AccBal_PRMX is not "Select":
            PRMX_PnL = load_sheet(uploaded_PRMX, sheet_PnL_PRMX)
            col_options_PRMX = PRMX_PnL.columns.tolist()
            col_options_PRMX.insert(0, "Select")
            col1_PRMX, col2_PRMX, col3_PRMX =st.columns([0.2, 0.2, 0.6])
            with col1_PRMX:
                col_desc_PRMX = st.selectbox("Select columns which contains PRMX P&L Description", col_options_PRMX)
                               
            with col2_PRMX:
                col_balance_PRMX = st.selectbox("Select columns which contains PRMX P&L Balance", col_options_PRMX)
                
            if col_desc_PRMX is not "Select" and col_balance_PRMX is not "Select":
                PRMX_PnL.rename(columns={col_desc_PRMX: "Description", col_balance_PRMX: "Balance"}, inplace=True)
                PRMX_PnL = PRMX_PnL[['Description', 'Balance']]
                PRMX_PnL["Income Rows"] = ''
                PRMX_PnL['Balance'] = pd.to_numeric(PRMX_PnL['Balance'], errors='coerce')
                PRMX_PnL['Balance'] = PRMX_PnL['Balance'].astype(float)
                edited_PRMX = st.data_editor(PRMX_PnL, column_config={
                            "Income Rows": st.column_config.CheckboxColumn(default=False)
                        }, disabled=["Description", "Balance"], hide_index=True)
        
                
                PRMX_PnL = edited_PRMX
                PRMX_PnL = PRMX_PnL[PRMX_PnL['Income Rows'] == "True"]
                PRMX_PnL['Description'] = PRMX_PnL['Description'].str.lower()
                PRMX_Clasificacion = PRMX_PnL['Description'].unique()
    
                Total_Income = PRMX_PnL["Balance"].sum()
                Total_Income = "{:,.2f}".format(Total_Income)
                st.metric(label="Total Income", value=Total_Income)
        
                
                st.dataframe(PRMX_PnL)
            else:
                st.dataframe(PRMX_PnL)
            

    with subtab2_PRMX:
        if uploaded_PRMX and sheet_PnL_PRMX is not "Select":
            PRMX_Balances = load_sheet(uploaded_PRMX, sheet_AccBal_PRMX)
            cols_acc_bal_PRMX = PRMX_Balances.columns.tolist()
            cols_acc_bal_PRMX.insert(0, "Select")
            
            col1_PRMX, col2_PRMX, col3_PRMX, col4_PRMX = st.columns(4)
            with col1_PRMX:
                col_cuenta_PRMX = st.selectbox("Select the column which contains PRMX - Cuenta", cols_acc_bal_PRMX)
            with col2_PRMX:
                col_clasificacion_PRMX = st.selectbox("Select the column which contains PRMX - Clasificacion", cols_acc_bal_PRMX)
            with col3_PRMX:
                col_rubro_PRMX = st.selectbox("Select the column which contains PRMX - Rubro", cols_acc_bal_PRMX)
            with col4_PRMX:
                col_saldo_PRMX = st.selectbox("Select the column which contains PRMX - Saldo", cols_acc_bal_PRMX)
            
            if (col_cuenta_PRMX is not "Select") and (col_clasificacion_PRMX is not "Select") and (col_rubro_PRMX is not "Select") and (col_saldo_PRMX is not "Select"):
                PRMX_Balances.rename(columns={col_cuenta_PRMX: "Cuenta", col_clasificacion_PRMX: "Clasificacion", col_rubro_PRMX: "Rubro", col_saldo_PRMX: "Saldo"}, inplace=True)
                PRMX_Balances = PRMX_Balances[['Cuenta', 'Clasificacion', 'Rubro', 'Saldo']]
                PRMX_Balances['Clasificacion'] = PRMX_Balances['Clasificacion'].str.lower()
                PRMX_Balances = PRMX_Balances[(PRMX_Balances['Clasificacion'].isin(PRMX_Clasificacion)) & (PRMX_Balances['Saldo'] != 0)]
                PRMX_Balances['Co_Cd'] = "PRMX"
                
                Total_Income_Balance = PRMX_Balances["Saldo"].sum()
                Total_Income_Balance = "{:,.2f}".format(Total_Income_Balance)
                st.metric(label="Total Income", value=Total_Income_Balance)
                
                st.dataframe(PRMX_Balances)
            else:
                st.dataframe(PRMX_Balances)
            
with tab6:
    
    Saldos_Financieros = pd.concat([GIMX_Balances,GSMX_Balances,KCMX_Balances,KLMX_Balances,PRMX_Balances])
    Saldos_Financieros['Debit Account'] = Saldos_Financieros['Cuenta'].str[:10]
    Saldos_Financieros.rename(columns={"Cuenta": "Account Name", "Saldo": "Balance"}, inplace=True)
    Saldos_Financieros['Type'] = "Cuentas de Ingresos"

    data_imp = {
        'Debit Account': [
            '1118116399', '1118116223', '1767221222', '1118116250', '1767221350',
            '1767221227', '1767221223', '1767221399', '1118116399', '1767221099',
            '1767221299', '1769226100', '1767221599'
        ],
        'Account Name': [
            '16% Input Tax', '16% Input Tax', 'VAT Payable ITCO', '8% Input IEPS Tax', 
            '8% Output IEPS Tax', '8% Output Manual IEPS', 'VAT Payable ITCO',
            '16% VAT Intercompany - Fiscal', '16% INPUT TAX - INT V0', 'Vat Industria y Comercio', 
            '16% Services Fiscal', 'WH Income Tax - External payments w/o taxable agre',
            '8% output Manual IE'
        ],
        'Type': [
            'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos',
            'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos',
            'Cuentas de Impuestos', 'Cuentas de Impuestos', 'Cuentas de Impuestos'
        ]
    }
    
    # Crear el DataFrame inicial
    ctas_impuestos = pd.DataFrame(data_imp)
    
    # Lista de valores para la columna Co_Cd
    co_cd_values = ['GIMX', 'GSMX', 'KCMX', 'KLMX', 'PRMX']
    
    # Crear un nuevo DataFrame con la columna Co_Cd
    df_list = []
    for co_cd in co_cd_values:
        df_temp = ctas_impuestos.copy()
        df_temp['Co_Cd'] = co_cd
        df_list.append(df_temp)
    
    # Concatenar todos los DataFrames
    ctas_impuestos = pd.concat(df_list, ignore_index=True)

    Saldos_Financieros = pd.concat([Saldos_Financieros,ctas_impuestos])

    Saldos_Financieros['Concat'] = Saldos_Financieros['Co_Cd'] + Saldos_Financieros['Debit Account']
    Saldos_Financieros['Currency'] = "MXN"
    Saldos_Financieros = Saldos_Financieros[['Concat', 'Co_Cd', 'Debit Account', 'Account Name', 'Type', 'Balance']]
    Saldos_Financieros = Saldos_Financieros.sort_values(by=['Co_Cd', 'Debit Account'], ascending=[True, True])    
    
    st.dataframe(Saldos_Financieros)
    
    # Crear y guardar el archivo FBL3N
    excel_buffer_sdos_fin = BytesIO()
    with pd.ExcelWriter(excel_buffer_sdos_fin, engine='xlsxwriter') as writer:
        Saldos_Financieros.to_excel(writer, index=False, sheet_name='SaldosFin_MX')
        
    # Descargar el archivo Excel en Streamlit
    st.download_button(
        label="Download Saldos Financieros",
        data=excel_buffer_sdos_fin.getvalue(),
        file_name="SaldosFinancierosMX.xlsx",
        key='download_button_SdosFin'
    )
    
