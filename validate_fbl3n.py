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

# Función para cargar el DataFrame desde el archivo Excel
@st.cache_data
def load_data(file):
    FBL3N_classified = pd.read_excel(file, sheet_name='FBL3N', dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str,
                                        'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    return FBL3N_classified


upload_FBL3N = st.sidebar.file_uploader("Upload the FBL3N file categorized for validation", type=["xlsx"])

if upload_FBL3N is not None:
    # Cargar el DataFrame desde el archivo Excel
    FBL3N_classified = load_data(upload_FBL3N)

    #----- Create Company Code Filters
    company_code_filter = st.sidebar.multiselect("Seleccionar Company Code:", FBL3N_classified['Company Code'].unique())
    
    if not company_code_filter:
        # Mostrar todo el DataFrame sin filtros
        FBL3N_merged_unfiltered = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' expense'))
        st.write('FBL3N merged & unfiltered')
        st.dataframe(FBL3N_merged_unfiltered)
    else:
        FBL3N_merged_filtered = FBL3N_classified.merge(FBL3N_classified, left_on="Key_1", right_on='Key_2', how='outer', suffixes=('', ' expense'))
        FBL3N_merged_filtered = FBL3N_merged_filtered[((FBL3N_merged_filtered['Company Code'].isin(company_code_filter)) | (FBL3N_merged_filtered['Company Code'].isna())) & ((FBL3N_merged_filtered['Related Party expense'].isin(company_code_filter)) | (FBL3N_merged_filtered['Related Party expense'].isna()))]
        # Mostrar el DataFrame filtrado
        st.write('FBL3N merged & filtered')
        st.dataframe(FBL3N_merged_filtered)




# import streamlit as st
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import accuracy_score
# import pickle
# import os
# import datetime
# from io import BytesIO
# import io
# from io import StringIO
# import base64
# import xlsxwriter
# from xlsxwriter import Workbook
# import time
# # import pygwalker as pyg
# # import streamlit.components.v1 as components
# # from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html



# st.set_page_config(
#     page_title="Tax Package Model",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'mailto:miguel.karim@karimortega.com'
#     }
# )



# st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=120)
# # st.header('Tax Package Model')
# st.subheader('Related Party Operations validations')

# # Función para cargar el DataFrame desde el archivo Excel
# @st.cache_data
# def load_data(file):
#     FBL3N_classified = pd.read_excel(file, sheet_name='FBL3N', dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str,
#                                         'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
#     return FBL3N_classified


# upload_FBL3N = st.sidebar.file_uploader("Upload the FBL3N file categorized for validation", type=["xlsx"])

# if upload_FBL3N is not None:
#     # Cargar el DataFrame desde el archivo Excel
#     FBL3N_classified = load_data(upload_FBL3N)

#     #----- Create Company Code Filters
#     company_code_filter = st.sidebar.multiselect("Seleccionar Company Code:", FBL3N_classified['Company Code'].unique())
#     # related_party_filter = st.sidebar.multiselect("Seleccionar Related Party:", FBL3N_classified['Related Party'].unique())
    

#     if not company_code_filter:
#             # Mostrar todo el DataFrame sin filtros
#             st.dataframe(FBL3N_classified)
#     else:
#         # Aplicar filtros si hay selecciones
#         # filtered_FBL3N_classified = FBL3N_classified[(FBL3N_classified['Company Code'].isin(company_code_filter)) & (FBL3N_classified['Related Party'].isin(related_party_filter))]
#         filtered_FBL3N_classified = FBL3N_classified[(FBL3N_classified['Company Code'].isin(company_code_filter))]
#         # Mostrar el DataFrame filtrado
#         st.dataframe(filtered_FBL3N_classified)




    
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
    
