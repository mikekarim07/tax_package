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

def load_data(uploaded_file):
    FBL3N_classified = pd.read_excel(uploades_FBL3N_classified, engine='openpyxl', sheet_name='FBL3N', 
                               dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Text': str,
                                        'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    return FBL3N_classified


# st.divider()
uploades_FBL3N_classified = st.sidebar.file_uploader("Upload FBL3N classified", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()

if 'FBL3N_classified' not in st.session_state:
    st.session_state.FBL3N_classified = None

if st.session_state.FBL3N_classified is None and uploades_FBL3N_classified is not None:
    st.session_state.FBL3N_classified = load_data(uploades_FBL3N_classified)

    company_codes = st.sidebar.selectbox("Select Company Codes", st.session_state.FBL3N_classified['Company Code'].unique())
    
    st.session_state.FBL3N_classified = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Company Code'] == company_codes]
    related_parties = st.sidebar.selectbox("Select Related Parties", st.session_state.FBL3N_classified['Related Party'].unique())
    st.session_state.FBL3N_classified = st.session_state.FBL3N_classified[st.session_state.FBL3N_classified['Related Party'] == related_parties]
    st.dataframe(st.session_state.FBL3N_classified)
