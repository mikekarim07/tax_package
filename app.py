import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import base64
from io import StringIO, BytesIO

st.set_page_config(page_title='Tax Package')
st.title('Tax Package 📈')
st.subheader('Cargar archivo con el auxiliar FBL3N')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df_FBL3N = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df_FBL3N)
    groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('Company Code', 'Account', 'User Name', 'Tax Code'),
    )

    # -- GROUP DATAFRAME
    output_columns = ['Amount in local currency']
    df_grouped_FBL3N = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()
    st.dataframe(df_grouped_FBL3N)

    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Amount in local currency',
        color='Amount in local currency',
        color_continuous_scale=['yellow', 'green'],
        template='plotly_white',
        title=f'<b>Sales & Profit by {groupby_column}</b>'
    )
    st.plotly_chart(fig)

    # -- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)

