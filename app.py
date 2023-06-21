import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import base64
from io import StringIO, BytesIO
from streamlit_option_menu import option_menu

# Object notation
with st.sidebar:
    st.[element_name]

#with st.sidebar:
#    selected = option_menu(
#        menu_title = "HOME",
#        options = ['Parametros','Data'],
#    )

#tab_titles = [
#    'primera',
#    'segunda',]
#tabs = st.tabs(tab_titles)



st.set_page_config(page_title='Tax Package')
st.title('Tax Package 📈')
st.subheader('Cargar los archivos FBL3N y Parametros')

FBL3N_uploaded_file = st.file_uploader('Selecciona el Archivo FBL3N', type='xlsx')
if FBL3N_uploaded_file:
    st.markdown('---')
    df_FBL3N = pd.read_excel(FBL3N_uploaded_file, engine='openpyxl')

Parametros_uploaded_file = st.file_uploader('Selecciona el Archivo Data Master que contenga el catalogo de cuentas', type='xlsx')
if Parametros_uploaded_file:
    st.markdown('---')
    df_parametros = pd.read_excel(Parametros_uploaded_file,
                              sheet_name = 'GL_Accounts', engine='openpyxl',
                             dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})
    
    
    st.subheader('Auxiliar FBL3N')
    #st.dataframe(df_FBL3N)
    st.write(df_FBL3N.shape)
    
    st.subheader('Parametros de clasificación')
    #st.dataframe(df_parametros)
    st.write(df_parametros.shape)

    FBL3N_ctas = df_FBL3N[['Account']].astype(str)
    Parametros_ctas = df_parametros[['GL_Account']].astype(str)
    Ctas_unicas = FBL3N_ctas[['Account']].drop_duplicates()
    result = pd.merge(Ctas_unicas, Parametros_ctas, left_on = 'Account', right_on = 'GL_Account', how = 'left')
    result = result.fillna('Nueva')
    result = result[result['GL_Account'] == 'Nueva']
    result = result.rename(columns={"GL_Account": "Description"})
    result = result.rename(columns={"Account": "GL_Account"})
    result['Country'] = 'Seleccionar'
    result['CoCd'] = 'Seleccionar'
    result = st.data_editor(result)
    
    
    #df_parametros = pd.concat([df_parametros, result])

    #st.dataframe(df_parametros)
    #st.write(df_parametros.shape)
    
    #new_parametros = st.data_editor(df_parametros)
    #,
    #column_config={
    #    "GL_Account": "GL_Account",
    #    "Description": st.text_input(
    #        "Descrption",
    #        help="Copia y pega la descripcion de la cuenta desde SAP",
    #        width="medium",
    #        ),
    #    "is_widget": "Widget ?",
    #},
    #disabled=["command", "is_widget"],
    #hide_index=True,
    #)







    
    #FBL3N_ctas = df_FBL3N['Account'].astype(str)
    #Parametros_ctas = df_parametros['GL_Account'].astype(str)
    #Ctas_unicas = pd.unique(FBL3N_ctas[['Account']].values.ravel())
    #result = pd.merge(Ctas_unicas, Parametros_ctas, left_on = 'Account', right_on = 'GL_Account', how = 'left')
    #st.dataframe('result')




    #edited_df = st.data_editor(
    #df_FBL3N,
    #column_config={
    #    "Company Code": "CoCode",
    #    "Document Number": st.column_config.SelectboxColumn(
    #        "Doc Number",
    #        help="Clasifica el Num de documento",
    #        width="medium",
    #        options=[
    #            "Venta",
    #            "Compra",
    #            "Hedge",
    #        ],
    #    ),
    #    "is_widget": "Widget ?",
    #},
    #disabled=["command", "is_widget"],
    #hide_index=True,
    #)
    
    #groupby_column = st.selectbox(
    #    'What would you like to analyse?',
    #    ('Company Code', 'Account', 'User Name', 'Tax Code'),
    #)

    
    
    
    # -- GROUP DATAFRAME
    #output_columns = ['Amount in local currency']
    #df_grouped_FBL3N = df_FBL3N.groupby(by=[groupby_column], as_index=False)[output_columns].sum()
    ##st.dataframe(df_grouped_FBL3N)

    # -- Información filtrada por company code y agrupada
    #df2 = pd.unique(df_FBL3N[['Company Code']].values.ravel())
    ##st.dataframe(df2)
    
    
    
    ##cocode = st.selectbox('Company Code',df2)
    #cocode = df_FBL3N['Company Code'] == st.selectbox('Choose all Company Codes', df2)
        
    #st.subheader('Auxiliar FBL3N Filtrado por Company code')
    #df_FBL_filtered = df_FBL3N[[cocode]]
    #st.dataframe(df_FBL_filtered)
    
    
    #st.subheader('Gráfica')
    ## -- PLOT DATAFRAME
    #fig = px.bar(
    #    df_grouped_FBL3N,
    #    x=groupby_column,
    #    y='Amount in local currency',
    #    color='Amount in local currency',
    #    color_continuous_scale=['purple', 'green'],
    #    template='plotly_white',
    #    title=f'<b>Sales & Profit by {groupby_column}</b>'
    #)
    #st.plotly_chart(fig)

    ## -- DOWNLOAD SECTION
    
    #def generate_excel_download_link(df_grouped_FBL3N):
        # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    #    towrite = BytesIO()
    #    df_grouped_FBL3N.to_excel(towrite, index=False, header=True)  # write to BytesIO buffer
    #    towrite.seek(0)  # reset pointer
    #    b64 = base64.b64encode(towrite.read()).decode()
    #    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    #    return st.markdown(href, unsafe_allow_html=True)

    
    
    #st.subheader('Downloads:')
    #generate_excel_download_link(df_grouped_FBL3N)
    ##generate_html_download_link(fig)
