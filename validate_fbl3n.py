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
st.header('Tax Package Model')
st.subheader('Related Party Operations validations')


def highlight_rows(val):
    if val['Subcode expense'] == 0:
        return 'background-color: yellow'
    elif val['Subcode expense'] == 300:
        return 'background-color: lightgreen'
    else:
        return ''



# Función para cargar el DataFrame desde el archivo Excel
@st.cache_data
def load_data(file):
    FBL3N_classified = pd.read_excel(file, sheet_name='FBL3N', dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str,
                                        'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    return FBL3N_classified

def load_data1(file):
    subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
                  dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
                         'Code_RP': str, 'Code_Desc_RP': str,})
    return subcodes

upload_FBL3N = st.sidebar.file_uploader("Upload the FBL3N file categorized for validation", type=["xlsx"])
uploaded_masters = st.sidebar.file_uploader("Upload masters file which contains the Chart of Accounts and Subcodes", key="masters", type=["xlsx"], accept_multiple_files=False)

if upload_FBL3N is not None and uploaded_masters is not None:
    #----- Cargar el DataFrame desde el archivo Excel
    FBL3N_classified = load_data(upload_FBL3N)
    subcodes = load_data1(uploaded_masters)
    #----- Crear un nuevo dataframe con base en el Dataframe original (FBL3N_classified) que se cruce a si mismo con base en las columnas Key_1 y Key_2
    FBL3N_merged = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' expense'))
    #----- Crear un selectbox para realizar un filtro con base en el company code
    company_code_filter = st.sidebar.selectbox("Select Company Code:", FBL3N_classified['Company Code'].unique())
    #----- Crear un nuevo dataframe con base en el dataframe previo y cruzado con el filtro aplicado
    FBL3N_merged_filtered = FBL3N_merged[((FBL3N_merged['Company Code'] == company_code_filter) | (FBL3N_merged['Company Code'].isna())) & ((FBL3N_merged['Related Party expense'] == company_code_filter) | (FBL3N_merged['Related Party expense'].isna()))]
    FBL3N_merged_filtered = FBL3N_merged_filtered.merge(subcodes, left_on="Subcode", right_on='Code', how='left')
    #----- Funcion para analizar si la conciliacion entre datos es correcta en cuanto a subcodes se refiere
    def sc_ok(row):
        if row['Subcode expense'] == row['Code_RP']:
            return "Ok"
        else:
            return 'Not Ok'
    FBL3N_merged_filtered['Validation'] = FBL3N_merged_filtered.apply(sc_ok, axis=1)
    
    edited_df = st.data_editor(FBL3N_merged_filtered, disabled=["Related Party sell", "Company Code sell"], hide_index=False)
    FBL3N_merged.update(edited_df)
    col1, col2 = st.columns(2)
    with col1:
       doc_num_filter = st.text_input("Introduce the Document number you want to see the information")
    with col2:
       st.text("Introduce the Document number you want to see the information")
           
    CC_info = edited_df[edited_df['Document Number'] == doc_num_filter]
    RP_info = edited_df[edited_df['Document Number'] == doc_num_filter]
    CC_info = CC_info[['CONCAT', 'Subcode', 'Related Party', 'Company Code', 'Document Number', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Posting period']].T
    RP_info = RP_info[['CONCAT expense', 'Subcode expense', 'Related Party expense', 'Company Code expense', 'Document Number expense', 'Document Type expense', 'Account expense', 'Text expense', 'Reference expense', 'Document Header Text expense', 'User Name expense', 'Posting period expense']].T    
    col1, col2 = st.columns(2)
    with col1:
        st.write(CC_info)
        # st.write(CC_info[['CONCAT', 'Subcode']])
    with col2:
        st.write(RP_info)
    
    st.write('Dataframe actualizado')
    st.dataframe(FBL3N_merged)
    st.dataframe(subcodes)



    # #----- Create Company Code Filters
    # # company_code_filter = st.sidebar.multiselect("Select Company Code:", FBL3N_classified['Company Code'].unique())
    # company_code_filter = st.sidebar.selectbox("Select Company Code:", FBL3N_classified['Company Code'].unique())
    
    # if not company_code_filter:
    #     # Mostrar todo el DataFrame sin filtros
    #     FBL3N_merged_unfiltered = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' expense'))
    #     st.write('FBL3N merged & unfiltered')
    #     st.dataframe(FBL3N_merged_unfiltered)
    # else:
    #     FBL3N_merged_filtered = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' expense'))
    #     # FBL3N_merged_filtered = FBL3N_merged_filtered[((FBL3N_merged_filtered['Company Code'].isin(company_code_filter)) | (FBL3N_merged_filtered['Company Code'].isna())) & ((FBL3N_merged_filtered['Related Party expense'].isin(company_code_filter)) | (FBL3N_merged_filtered['Related Party expense'].isna()))]
    #     FBL3N_merged_filtered = FBL3N_merged_filtered[((FBL3N_merged_filtered['Company Code'] == company_code_filter) | (FBL3N_merged_filtered['Company Code'].isna())) & ((FBL3N_merged_filtered['Related Party expense'] == company_code_filter) | (FBL3N_merged_filtered['Related Party expense'].isna()))]
    #     # FBL3N_merged_filtered = [[
    #     FBL3N_merged_filtered = FBL3N_merged_filtered.fillna('')
        
    #     edited_df = st.data_editor(FBL3N_merged_filtered, disabled=["Related Party sell", "Company Code sell"], hide_index=True)
    #     FBL3N_classified.update(merged_FBL3N_classified)

        
    #     # Mostrar el DataFrame filtrado
    #     st.write('FBL3N merged & filtered')
    #     st.dataframe(FBL3N_merged_filtered)




    
#     # # Aplicar filtros
#     # # filtered_FBL3N_classified = apply_filters(FBL3N_classified, company_code_filter, related_party_filter)
#     # # filtered_FBL3N_classified = FBL3N_classified[FBL3N_classified['Company Code'].isin(company_code_filter)]
    
#     # filtered_FBL3N_classified = FBL3N_classified[(FBL3N_classified['Company Code'].isin(company_code_filter)) & (FBL3N_classified['Related Party'].isin(related_party_filter))]
#     # merged_FBL3N_classified = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=(' sell', ' purchase'))
#     merged_FBL3N_classified = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' purchase'))
#     st.write(merged_FBL3N_classified.columns)
#     st.write('FBL3N merged unfiltered')
#     st.dataframe(merged_FBL3N_classified)
#     # merged_FBL3N_classified = merged_FBL3N_classified[(merged_FBL3N_classified['Company Code sell'].isin(company_code_filter)) & (merged_FBL3N_classified['Company Code purchase'].isin(related_party_filter))]
#     merged_FBL3N_classified = merged_FBL3N_classified[(merged_FBL3N_classified['Company Code'].isin(company_code_filter)) & (merged_FBL3N_classified['Related Party purchase'].isin(company_code_filter))]
    
    
    
#     # columns_to_eliminate = ['CONCAT sell', 'Subcode 2 sell', 'Document Date sell', 'Amount in local currency sell', 'Local Currency sell', 'Key_1 sell', 'Key_2 sell', 'CONCAT purchase', 'Document Date purchase', 'Amount in local currency purchase', 'Local Currency purchase', 'Key_1 purchase', 'Key_2 purchase', 'Subcode 2 purchase']
#     columns_to_eliminate = ['Subcode 2', 'Document Date', 'Amount in local currency', 'Local Currency', 'Key_1', 'Key_2', 'CONCAT purchase', 'Document Date purchase', 'Amount in local currency purchase', 'Local Currency purchase', 'Key_1 purchase', 'Key_2 purchase', 'Subcode 2 purchase']
#     merged_FBL3N_classified = merged_FBL3N_classified.drop(columns=columns_to_eliminate)
    
#     # Mostrar el DataFrame filtrado
#     st.write('FBL3N filtered')
#     st.dataframe(filtered_FBL3N_classified)
#     st.write('FBL3N merged filtered')
#     st.dataframe(merged_FBL3N_classified)
#     edited_df = st.data_editor(merged_FBL3N_classified, disabled=["Related Party sell", "Company Code sell"], hide_index=True)
#     FBL3N_classified.update(merged_FBL3N_classified)
#     st.dataframe(FBL3N_classified)

#     # pyg_html = pyg.walk(filtered_FBL3N_classified, return_html=True)
#     # components.html = (pyg_html)
    
