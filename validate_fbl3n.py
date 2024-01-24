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
    page_title="Tax Package ML Classification Model",
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

# st.divider()
uploades_FBL3N_classified = st.sidebar.file_uploader("Upload FBL3N classified", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()

if uploades_FBL3N_classified:
    FBL3N_classified = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', 
                               dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str,
                                        'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    # FBL3N_new = pd.read_excel(uploaded_new_FBL3N, engine='openpyxl', sheet_name='FBL3N',
    #             dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Document Number': str,
    #                     'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    # accounts = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='GL_Accounts',
    #             dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})
    # subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
    #               dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
    #                      'Code_RP': str, 'Code_Desc_RP': str,})


    company_codes = st.sidebar.selectbox("Select Company Codes", FBL3N_classified['Company Code'].unique())
    related_parties = st.sidebar.selectbox("Select Related Parties", FBL3N_classified['Related Party'].unique())
    FBL3N_classified = FBL3N_classified[FBL3N_classified['Company Code'].isin(company_codes) & FBL3N_classified['Related Party'].isin(related_parties)]
    st.dataframe(FBL3N_classified)
