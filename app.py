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
    page_title="Tax Package ML Classification Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)


st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=120)
# st.header('Machine Learnig Model')
st.subheader('Tax Package - Related Party Operations Category Classification Machine Learning Model')


@st.cache_data
def get_sheet_names(file):
    # Leer todas las hojas del archivo y devolver sus nombres
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    return excel_file.sheet_names

@st.cache_data
def load_sheet(file, sheet_name, dtype):
    # Leer una hoja específica del archivo de Excel
    return pd.read_excel(file, engine='openpyxl', sheet_name=sheet_name, dtype=dtype)


dtype_FBL3N_full = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,}

dtype_FBL3N_new = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Document Number': str, 'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,}

dtype_ZLAAUDIT = {'CONCAT': str, 'CONCAT_2': str, 'Company Code': str, 'Document Number': str, 'Business Area': str, 'Document type': str, 'Tax Code': str, 'Line item': str, 'Posting Key': str, 'Account': str, 'Assignment': str, 'User Name': str, 'Reference': str, 'Document Header Text': str, 'Currency': str, 'Local Currency': str,}

dtype_accounts = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str}

dtype_tax_accounts = {'Co_Cd': str, 'Debit Account': str, 'Account Name': str, 'CoCd': str}

dtype_subcodes = {'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str, 'Code_RP': str, 'Code_Desc_RP': str,}

dtype_sdosfin = {'Concat': str, 'Co_Cd': str, 'Debit Account': str, 'Account Name': str, 'Type': str, 'Balance': str,}

dtype_fb03 = {'CoCd': str, 'DocumentNo': str, 'Reversal': str, 'Doc. Date': str, 'Entered': str, 'Pstng Date': str}


# st.divider()

start_time01 = time.time()
st.sidebar.subheader('Historical Data')
uploaded_FBL3N_train = st.sidebar.file_uploader("Upload FBL3N file which contains historical data classified to train the Machine Learning Model", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()
st.sidebar.subheader('New FBL3N Dataset')
uploaded_new_FBL3N = st.sidebar.file_uploader("Upload the file which contains the new dataset to be classified", key="new_FBL3N", type=["xlsx"], accept_multiple_files=False)
st.sidebar.subheader('ZLAAUDIT')
uploaded_ZLAAUDIT = st.sidebar.file_uploader("Upload the file which contains the ZLAAUDIT dataset", key="ZLAAUDIT", type=["xlsx"], accept_multiple_files=False)
st.sidebar.subheader('FB03')
uploaded_FB03 = st.sidebar.file_uploader("Upload the file which contains the FB03 dataset", key="FB03", type=["xlsx"], accept_multiple_files=False)
st.sidebar.subheader('Saldos Financieros')
uploaded_SdosFin = st.sidebar.file_uploader("Upload the file which contains the SALDOS FINANCIEROS dataset", key="SaldosFinancieros", type=["xlsx"], accept_multiple_files=False)
st.sidebar.subheader('Masters')
uploaded_masters = st.sidebar.file_uploader("Upload masters file which contains the Chart of Accounts and Subcodes", key="masters", type=["xlsx"], accept_multiple_files=False)
st.sidebar.divider()
if uploaded_FBL3N_train and uploaded_new_FBL3N and uploaded_masters and uploaded_SdosFin: #and uploaded_ZLAAUDIT:
    FBL3N_full = load_sheet(uploaded_FBL3N_train, 'FBL3N', dtype_FBL3N_full)
    FBL3N_new = load_sheet(uploaded_new_FBL3N, 'FBL3N', dtype_FBL3N_new)
    ZLAAUDIT = load_sheet(uploaded_ZLAAUDIT, 'ZLAAUDIT', dtype_ZLAAUDIT)
    accounts = load_sheet(uploaded_masters, 'GL_Accounts', dtype_accounts)
    subcodes = load_sheet(uploaded_masters, 'Subcodes', dtype_subcodes)
    tax_accounts = load_sheet(uploaded_masters, 'Cuentas Taxes', dtype_tax_accounts)
    saldos_financieros = load_sheet(uploaded_SdosFin, 'SaldosFin_MX', dtype_sdosfin)
    fb03 = load_sheet(uploaded_FB03, 'Sheet1', dtype_fb03)

    
    # FBL3N_full = pd.read_excel(uploaded_FBL3N_train, engine='openpyxl', sheet_name='FBL3N', 
    #                            dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Document Number': str, 'Account': str, 'Text': str,
    #                                     'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})
    # FBL3N_new = pd.read_excel(uploaded_new_FBL3N, engine='openpyxl', sheet_name='FBL3N',
    #             dtype = {'Subcode': str, 'Company Code': str, 'Document Type': str, 'Account': str, 'Document Number': str,
    #                     'Text': str, 'Reference': str, 'Document Header Text': str, 'User Name': str, 'Tax Code': str,})

    # ZLAAUDIT = pd.read_excel(uploaded_ZLAAUDIT, engine='openpyxl', sheet_name='ZLAAUDIT',
    #             dtype = {'CONCAT': str, 'CONCAT_2': str, 'Company Code': str, 'Document Number': str, 'Business Area': str,
    #                     'Document type': str, 'Tax Code': str, 'Line item': str, 'Posting Key': str, 'Account': str, 'Assignment': str,
    #                     'User Name': str, 'Reference': str, 'Document Header Text': str, 'Currency': str, 'Local Currency': str,})

    # accounts = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='GL_Accounts',
    #             dtype = {'GL_Account': str, 'Description': str, 'Country': str, 'CoCd': str})

    # subcodes = pd.read_excel(uploaded_masters, engine='openpyxl', sheet_name='Subcodes',
    #               dtype={'Code_Type': str, 'Code': str, 'Code_Desc': str, 'Code_Type_RP': str,
    #                      'Code_RP': str, 'Code_Desc_RP': str,})

    # saldos_financieros = pd.read_excel(uploaded_SdosFin, engine='openpyxl', sheet_name='SaldosFin_MX',
    #               dtype={'Concat': str, 'Co_Cd': str, 'Debit Account': str, 'Account Name': str,
    #                      'Type': str, 'Balance': str,})
    
    # fb03 = pd.read_excel(uploaded_FB03, engine='openpyxl', sheet_name='Sheet1',
    #               dtype={'CoCd': str, 'DocumentNo': str, 'Reversal': str, 'Key_Doc': str,
    #                      'Key_Rev': str, 'Doc. Date': str,})

    ######----------MACHINE LEARNING MODEL----------######
    #-----Stage 1: Clean dataset, to get unique records and avoid NA, to have a clean Dataset to run the Machine Learning Model
    #----- Step 1: Fill "NaN" cell as empty ('') at specified columns
    NA_Fill_Columns = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_full[NA_Fill_Columns] = FBL3N_full[NA_Fill_Columns].fillna('')
    # FBL3N_full.dropna(subset=NA_Fill_Columns, how='any', inplace=True)
    
    #----- Step 2: Delete rows with no Subcode (either NA or blank)
    FBL3N_full.dropna(subset=['Subcode'], how='any', inplace=True)
    FBL3N_full = FBL3N_full[FBL3N_full['Subcode'] != 0]
    #----- Step 3: Create a new column "ML"
    FBL3N_full['CONCAT'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str))
    FBL3N_full['ML'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + FBL3N_full['Account'] + ' ' + FBL3N_full['Text'] + ' ' + FBL3N_full['Reference'] + ' ' + FBL3N_full['Document Header Text'] + ' ' + FBL3N_full['User Name'] + ' ' + FBL3N_full['Tax Code']
    # FBL3N_full['Id'] = FBL3N_full['Company Code'] + ' ' + FBL3N_full['Document Type'] + ' ' + (FBL3N_full['Document Number'].astype(str)) + ' ' + (FBL3N_full['Amount in doc. curr.'].astype(str)) + ' ' + (FBL3N_full['Posting Date'].astype(str))

    #----- Step 4: Create a new column "Subcode_td", which contains the Subcode that has been assigned previously in order to use it later
    FBL3N_full['Subcode_td'] = FBL3N_full['Company Code'] + (FBL3N_full['Document Number'].astype(str)) + FBL3N_full['Document Type'] + (FBL3N_full['Posting period'].astype(str)) + (FBL3N_full['Amount in doc. curr.'].astype(str))
    
        
    #----- Step 6: Delete duplicated values of ML column in order to train the model (test dataset is setup to 20%, this can be adjusted)
    FBL3N_train = FBL3N_full[['ML', 'Subcode']].drop_duplicates()
    X = FBL3N_train['ML']
    y = FBL3N_train['Subcode']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #----- Step 7: Vectorize text data using TF-IDF (in previous versions max_features were set at 1,000, beacuse that provides the best accuracy when training the model, however this can be adjusted manually or with a streamlit widget, but re-runnings take time)
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    #----- Step 8: Train the classification model
    modelo = MultinomialNB()
    modelo.fit(X_train_tfidf, y_train)

    #----- Step 9: Make predictions to the test dataset
    y_pred = modelo.predict(X_test_tfidf)

    #----- Step 10: Calculate model accuracy
    accuracy = accuracy_score(y_test, y_pred)
    accuracy = "{:.2%}".format(accuracy)
    st.metric(label="Model Accuracy", value=accuracy, delta=accuracy)
    
    end_time01 = time.time()
    processing_time01 = end_time01 - start_time01
    processing_time_formatted01 = "{:.2f}".format(processing_time01)
    st.info(f'Machine Learning model training time: {processing_time_formatted01} seconds')

    st.divider()
    # st.subheader('Una vez entrenado el modelo de ML, se realizará la clasificación en el nuevo conjunto de datos')

    start_time02 = time.time()
    

    #----- Stage 2: Work with new FBL3N dataset, Masters (GL_Accounts and Subcodes), ZLAAUDIT and Saldos Financieros
    #----- Step 1: Fill "NaN" cell as empty ('') at specified columns
    st.write(FBL3N_new.shape)
    columnas_rellenar_real = ['Company Code', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 'User Name', 'Tax Code']
    FBL3N_new[columnas_rellenar_real] = FBL3N_new[columnas_rellenar_real].fillna('')
    cols_previous_fbl3n = ['Period', 'Doc. Date', 'Entered', 'Pstng Date', 'Key_Concat', 'Key_Reversal', 'Period_Rev', 'Doc. Date_Rev', 'Entered_Rev', 'Pstng Date_Rev', 'Key_1', 'Key_2', 'Taxes']
    FBL3N_new = FBL3N_new.drop(columns=[col for col in cols_previous_fbl3n if col in FBL3N_new.columns])
    
    #----- Step 2: Create a new column "ML"
    FBL3N_new['CONCAT_01'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str))
    FBL3N_new['ML'] = FBL3N_new['Company Code'] + ' ' + FBL3N_new['Document Type'] + ' ' + FBL3N_new['Account'] + ' ' + FBL3N_new['Text'] + ' ' + FBL3N_new['Reference'] + ' ' + FBL3N_new['Document Header Text'] + ' ' + FBL3N_new['User Name'] + ' ' + FBL3N_new['Tax Code']
    
    #----- Step 3: Create a new column for comparing FBL3N (Original and New) to get the previously assigned subcode
    FBL3N_new['Subcode_td_1'] = FBL3N_new['Company Code'] + (FBL3N_new['Document Number'].astype(str)) + FBL3N_new['Document Type'] + (FBL3N_new['Posting period'].astype(str)) + (FBL3N_new['Amount in doc. curr.'].astype(str))
    FBL3N_previous_subcodes = FBL3N_new.copy()
    FBL3N_previous_subcodes = FBL3N_previous_subcodes[['CONCAT', 'Subcode']]
    # st.write('previous subcodes')
    # st.dataframe(FBL3N_previous_subcodes)
    # st.write(FBL3N_previous_subcodes.columns)
    
    #----- Step 4: Assign the Subcode to the new FBL3N dataset uploades, according to the ML model
    X_new_data_tfidf = tfidf_vectorizer.transform(FBL3N_new['ML'])
    # Realizar predicciones con el modelo entrenado en el conjunto de datos real
    FBL3N_new['Subcode_ML'] = modelo.predict(X_new_data_tfidf)

    #### Testing
    #----- Codigo para crear una nueva columna que contenga el porcentaje de certeza en la prediccion, vamos a ver si funciona
    # Assuming 'modelo' is your trained model
    # probability_matrix = modelo.predict_proba(X_new_data_tfidf)
    
    # Extract the probabilities for the predicted class
    # certainty_percentages = [max(probabilities) * 100 for probabilities in probability_matrix]
    
    # Create a new column 'Certainty_Percentage' in your DataFrame
    # FBL3N_new['Certainty_Percentage'] = certainty_percentages
    
    # Now, FBL3N_new contains a column with the certainty percentage for each prediction
    #### Testing ends

    FBL3N_new = FBL3N_new.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
    NA_Fill_CoCd = ['CoCd']
    FBL3N_new[NA_Fill_CoCd] = FBL3N_new[NA_Fill_CoCd].fillna('')
       
    
    #---------------FB03-------------
    with st.expander("FB03 Original"):
        # st.write("FB03 Original")
        fb03['Reversal'] = fb03['Reversal'].fillna('')
        fb03['doc date year'] = fb03['Doc. Date'].str[:4]
        fb03['clave01'] = fb03['CoCd'] + fb03['DocumentNo'] + fb03['Doc. Date'].str[:4]
        fb03['clave02'] = fb03['CoCd'] + fb03['Reversal'] + fb03['Doc. Date'].str[:4]
        fb03_fix = pd.merge(fb03, fb03, left_on='clave01', right_on='clave02', how='left', suffixes=('', '_fix'))
        st.dataframe(fb03_fix)
    fb03_NA_Fill_Columns = ['Reversal']
    fb03 = fb03.dropna(subset=fb03_NA_Fill_Columns)
    fb03 = fb03.drop_duplicates()
    with st.expander('''FB03 - Clean (Remove Duplicates and Drop NA's in Reversal Columns)'''):
        st.dataframe(fb03)
    # st.write("fb03")
    # st.dataframe(fb03)
    fb03['Key_Concat'] = fb03['CoCd'] + fb03['DocumentNo']
    fb03['Key_Reversal'] = fb03['CoCd'] + fb03['Reversal']
    
    fb03_cols_elim = ['User', 'CoCd', 'Doc.Header Text', 'DocumentNo', 'Year', 'Reference', 'Type',
                                'TCode', 'Reversal flag', 'Reversal', 'Ref. proc.', 'Tran', 'Ref.key 1', 'Reason', 'Act', 
                               'Time', 'LCurr', 'Crcy']
    
    fb03 = fb03.drop(columns=fb03_cols_elim)
    with st.expander('''FB03 Prior to cross tables'''):
        st.dataframe(fb03)
        

    # fb03 = fb03.drop_duplicates(subset=['Key_Concat', 'Key_Reversal'], keep='first')
    fb03_left = fb03.copy()
    fb03_right = fb03.copy()    
    # fb03_merged = pd.merge(fb03, fb03, left_on='Key_Concat', right_on='Key_Reversal', how='left', suffixes=('', '_Rev'))
    fb03_merged = fb03_left.merge(fb03_right, left_on="Key_Concat", right_on='Key_Reversal', how='left', suffixes=('', '_Rev'))
    with st.expander('''FB03 Merged'''):
        st.dataframe(fb03_merged)
        
    FBL3N_new = FBL3N_new.merge(fb03_merged, left_on="CONCAT_01", right_on='Key_Concat', how='left')
    with st.expander('''FBL3N Merged with FB03'''):
        st.dataframe(FBL3N_new)
    
    #----- ZLAAUDIT filter by account 7736000018 & 19 (Hedge) -----#
    hedge_accnts = ZLAAUDIT[ZLAAUDIT['Account'].isin(['7736000018', '7736000019', '2901300000'])]
    hedge_accnts = hedge_accnts[['CONCAT', 'Account']]
    hedge_accnts.rename(columns={'CONCAT': 'Key_ZLAAUDIT', 'Account': 'ZLAAUDIT_Acc'}, inplace=True)
    # st.write('Hedge Accounts')
    # st.dataframe(hedge_accnts)

    FBL3N_new = FBL3N_new.merge(hedge_accnts, left_on="CONCAT_01", right_on='Key_ZLAAUDIT', how='left')
    # st.dataframe(FBL3N_new)
    # st.write(FBL3N_new.columns)
    
    #---------------Funciones para subcodes fijas-------------------
    
    def sc_121(row):
        if (row['Reference'].startswith("00015-") and row['Document Header Text'].startswith("117")) or (row['Document Header Text'].startswith("117") and row['Document Type'].startswith("RV")) or row['Reference'].startswith("00016-") or (row['Text'].startswith("121")):
            return "121"
        else:
            return ''
    FBL3N_new['SC_1'] = FBL3N_new.apply(sc_121, axis=1)
    
    def sc_221(row):
        if (row['Reference'].startswith("117") and row['Document Type'].startswith("RN")) or (row['Document Number'].startswith("5") and ((row['Document Type'].startswith("RN") or row['Document Type'].startswith("RE")))
                                                                                              and (not (row['Text'].startswith("220") or row['User Name'].startswith("WF-BATCH"))) and (not (row['Account'].startswith("1556250212") or row['Account'].startswith("1556250302") or row['Account'].startswith("1556250392") or row['Account'].startswith("1556250472") or row['Account'].startswith("1556250440")))) or (row['Text'].startswith("221")) or (row['Document Header Text'].startswith("Interim")) or (row['User Name'].startswith("WF-BATCH") and row['Document Type'].startswith("RE") and (not (row['Account'].startswith("1556250212") or row['Account'].startswith("1556250302") or row['Account'].startswith("1556250392") or row['Account'].startswith("1556250472") or row['Account'].startswith("1556250440")))):
            return "221"
        else:
            return ''
    FBL3N_new['SC_2'] = FBL3N_new.apply(sc_221, axis=1)
    
    def sc_150(row):
    # Verificar las condiciones
        # if "loan int" in str(row['Document Header Text']).lower() and row['Reference'].startswith(str(row['Company Code']) + str(row['CoCd'])) and row['Document Type'].startswith("YH"):
        if ("loan int" in str(row['Document Header Text']).lower() and (row['Document Type'].startswith("YH") or row['Document Type'].startswith("DR"))) or ("loan int" in str(row['Document Header Text']).lower() and (row['Document Type'].startswith("SA")) and (row['Account'].startswith("1556250021"))):
            return "150"
        else:
            return ''
    FBL3N_new['SC_3'] = FBL3N_new.apply(sc_150, axis=1)

    def sc_250(row):
    # Verificar las condiciones
        if "loan int" in str(row['Document Header Text']).lower() and row['Document Type'].startswith("SA") and (not(row['Account'].startswith("1556250021"))):
            return "250"
        else:
            return ''
    FBL3N_new['SC_4'] = FBL3N_new.apply(sc_250, axis=1)

    def sc_300(row):
    # Verificar las condiciones
        if ("wf-batch" in str(row['User Name']).lower() and row['Document Type'].startswith("SA")) or (row['Text'].startswith("300")) or ((row['Document Type'].startswith("DZ") or row['Document Type'].startswith("KZ") or row['Document Type'].startswith("ZP") or row['Document Type'].startswith("KA")) and (not (row['Text'].startswith("210")))) or (row['Document Number'].startswith("14") or row['Document Number'].startswith("21") or row['Document Number'].startswith("20")) or (row['Account'].startswith("1556251210") or row['Account'].startswith("1556251270") or row['Account'].startswith("1556251300") or row['Account'].startswith("1556251400") or row['Account'].startswith("1556251450") or row['Account'].startswith("1556251470")) or ((row['Company Code'].startswith("KLMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("SAMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("GIMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("GSMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("KSMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("PRMX") and row['Account'].startswith("1556251390")) or (row['Company Code'].startswith("KLCM") and row['Account'].startswith("1556251390"))):
            return "300"
        else:
            return ''
    FBL3N_new['SC_5'] = FBL3N_new.apply(sc_300, axis=1)

    def sc_301(row):
        if ("valuation" in str(row['Text']).lower() or ("revaluacion" in str(row['Text']).lower())):
            return "301"
        else:
            return ''
    FBL3N_new['SC_6'] = FBL3N_new.apply(sc_301, axis=1)
    
    def sc_214(row):
        # if (row['Account'].startswith("1556160000") or (row['Account'].startswith("1556260000") and row['Text'].startswith("210"))) and (not (row['Text'].startswith("300"))):
        if ((row['Account'].startswith("1556160000") or (row['Account'].startswith("1556260000") and row['Text'].startswith("210"))) and (not (row['Text'].startswith("300")))) or ("7736000019" in str(row['ZLAAUDIT_Acc']).lower()) or ("2901300000" in str(row['ZLAAUDIT_Acc']).lower()):
            return "214"
        else:
            return ''
    FBL3N_new['SC_7'] = FBL3N_new.apply(sc_214, axis=1)

    def sc_114(row):
        # if ((row['Account'].startswith("1556260000") and row['Text'].startswith("110"))) and (not (row['Text'].startswith("300"))):
        if (((row['Account'].startswith("1556260000") and row['Text'].startswith("110"))) and (not (row['Text'].startswith("300")))) or ("7736000018" in str(row['ZLAAUDIT_Acc']).lower()):
            return "114"
        else:
            return ''
    FBL3N_new['SC_17'] = FBL3N_new.apply(sc_114, axis=1)

    def sc_601(row):
        if (row['Document Header Text'].startswith("610") or row['Text'].startswith("610") or row['Document Header Text'].startswith("601") or row['Text'].startswith("601")) and (row['Reference'].startswith(str(row['Company Code']))):
            return "601"
        else:
            return ''
    FBL3N_new['SC_8'] = FBL3N_new.apply(sc_601, axis=1)

    def sc_610(row):
        if (row['Document Header Text'].startswith("610") or row['Text'].startswith("610") or row['Document Header Text'].startswith("601") or row['Text'].startswith("601")) and (not (row['Reference'].startswith(str(row['Company Code'])))):
            return "610"
        else:
            return ''
    FBL3N_new['SC_9'] = FBL3N_new.apply(sc_610, axis=1)
    
    def sc_620(row):
        if (row['Document Header Text'].startswith("620") or row['Text'].startswith("620")) and (not (row['Account'].startswith("1556250212") or row['Account'].startswith("1556250302") or row['Account'].startswith("1556250392") or row['Account'].startswith("1556250472") or row['Account'].startswith("1556250440"))):
            return "620"
        else:
            return ''
    FBL3N_new['SC_10'] = FBL3N_new.apply(sc_620, axis=1)
    
    def sc_120(row):
        if (row['Document Header Text'].startswith("120") or row['Text'].startswith("120")) and (not (row['Document Header Text'].startswith("620"))):
            return "120"
        else:
            return ''
    FBL3N_new['SC_11'] = FBL3N_new.apply(sc_120, axis=1)

    def sc_220(row):
        if ((row['Document Header Text'].startswith("220") or row['Text'].startswith("220")) and (not (row['Document Header Text'].startswith("620")))) and not ("2901300000" in str(row['ZLAAUDIT_Acc']).lower()):
            return "220"
        else:
            return ''
    FBL3N_new['SC_12'] = FBL3N_new.apply(sc_220, axis=1)

    def sc_110(row):
        if ((row['Text'].startswith("110") or row['Text'].startswith("111")) and not ("loan int" in str(row['Document Header Text']).lower()) and not ((row['Document Header Text'].startswith("620"))) and not (("valuation" in str(row['Text']).lower()) or ("revaluacion" in str(row['Text']).lower())) and not (("guts" in str(row['Reference']).lower())) and not ("7736000018" in str(row['ZLAAUDIT_Acc']).lower())) or (row['Company Code'].startswith("KPRS") and row['Account'].startswith("1556250440") and row['Document Type'].startswith("SA") and row['Document Header Text'].startswith("Alloc ROC")):
            return "110"
        else:
            return ''
    FBL3N_new['SC_13'] = FBL3N_new.apply(sc_110, axis=1)

    def sc_210(row):
        if ((row['Text'].startswith("210") or row['Text'].startswith("211")) and (not (row['Account'].startswith("1556160000") or row['Account'].startswith("1556260000") or ("loan int" in str(row['Document Header Text']).lower()))) and not ("7736000019" in str(row['ZLAAUDIT_Acc']).lower())) or (row['Company Code'].startswith("KCAR") and row['Account'].startswith("1556250440") and row['Document Type'].startswith("SA") and row['Document Header Text'].startswith("Alloc ROC")):
            return "210"
        else:
            return ''
    FBL3N_new['SC_14'] = FBL3N_new.apply(sc_210, axis=1)

    def sc_400(row):
        if (row['Text'].startswith("400")):
            return "400"
        else:
            return ''
    FBL3N_new['SC_15'] = FBL3N_new.apply(sc_400, axis=1)

    def sc_0(row):
        if (row['Account'].startswith("1556250212") or row['Account'].startswith("1556250302") or row['Account'].startswith("1556250392") or row['Account'].startswith("1556250472")) or (row['Account'].startswith("1556250440") and (row['Document Type'].startswith("RE") or row['Document Type'].startswith("RN") or row['Document Type'].startswith("KG") or row['Document Type'].startswith("KR"))):
            return "0"
        else:
            return ''
    FBL3N_new['SC_16'] = FBL3N_new.apply(sc_0, axis=1)
    
    FBL3N_new['SC_concat'] = FBL3N_new['SC_1'] + FBL3N_new['SC_2'] + FBL3N_new['SC_3'] + FBL3N_new['SC_4'] + FBL3N_new['SC_5'] + FBL3N_new['SC_6'] + FBL3N_new['SC_7'] + FBL3N_new['SC_8'] + FBL3N_new['SC_9'] + FBL3N_new['SC_10'] + FBL3N_new['SC_11'] + FBL3N_new['SC_12'] + FBL3N_new['SC_13'] + FBL3N_new['SC_14'] + FBL3N_new['SC_15'] + FBL3N_new['SC_16'] + FBL3N_new['SC_17']

    with st.expander('''FBL3N classified with all subcodes columns'''):
        st.dataframe(FBL3N_new)
    
    
    #-----
    
    # def fix_01(reference, FBL3N_new):
    #     # Filtrar el DataFrame para encontrar la fila donde el "Document Number" coincide con la "Reference"
    #     filtro = FBL3N_new['Document Number'] == reference
    #     fila_encontrada = FBL3N_new[filtro]
    
    #     # Si se encuentra una fila que cumple la condición, devolver el valor de la columna "Subcode"
    #     if not fila_encontrada.empty:
    #         subcode = fila_encontrada.iloc[0]['Subcode']
    #         return subcode
    #     else:
    #         return ''
    # FBL3N_new['SC_17'] = FBL3N_new.apply(fix_01, axis=1)
    #-----
    def Subcode_Correction(row):
    # Verificar las condiciones
        if row['SC_concat'] != '' and (row['SC_concat'] != row['Subcode_ML'] ):
        # if row['SC_concat'] != '' and (row['SC_concat'] != row['Subcode_ML']) and (pd.isna(row['Key_Concat'])):
            return row['SC_concat']
        # elif pd.notna(row['Key_Concat']):
        #     return '0'
        else:
            return row['Subcode_ML']
    FBL3N_new['SC_Fix'] = FBL3N_new.apply(Subcode_Correction, axis=1)
    # st.write('after subcode correction')
    # st.dataframe(FBL3N_new)
    
    def Subcode(row):
        if  pd.notna(row['Subcode']) and pd.isna(row['Key_Concat']):
            return row['Subcode']
        elif pd.notna(row['Key_Concat']):
            return '0'
        else:
            return row['SC_Fix']
        # # Verificar las condiciones
        # # if row['Subcode'] != '':
        # if row['Subcode'] != '' and (pd.isna(row['Key_Concat'])):
        #     return row['Subcode']
        # elif pd.notna(row['Key_Concat']):
        #     return '0'
        # else:
        #     return row['SC_Fix']
    FBL3N_new['New Subcode'] = FBL3N_new.apply(Subcode, axis=1)
    with st.expander('''FBL3N subcode fix columns'''):
        st.dataframe(FBL3N_new)
    
    FBL3N_new.rename(columns={'Subcode': 'Previous_subcode', 'New Subcode': 'Subcode'}, inplace=True)
    # st.write('after rename columns')
    # st.dataframe(FBL3N_new)

    def remove_CONCAT(FBL3N_new):
            if "CONCAT" in FBL3N_new.columns:
                FBL3N_new = FBL3N_new.drop("CONCAT", axis=1)
            return FBL3N_new
    FBL3N_new = remove_CONCAT(FBL3N_new)
    # st.write('after remove concat')
    # st.dataframe(FBL3N_new)

    def remove_RelatedParty(FBL3N_new):
            if "Related Party" in FBL3N_new.columns:
                FBL3N_new = FBL3N_new.drop("Related Party", axis=1)
            return FBL3N_new
    FBL3N_new = remove_RelatedParty(FBL3N_new)
    # st.write('after remove related party')
    # st.dataframe(FBL3N_new)
    
    columns_to_rename = {'CoCd': 'Related Party', 'CONCAT_01': 'CONCAT'}
    FBL3N_new = FBL3N_new.rename(columns=columns_to_rename)
    # st.dataframe(FBL3N_new)
    
    FBL3N_new = FBL3N_new[['CONCAT', 'Subcode', 'Related Party', 'Company Code', 'Document Number', 'Document Type', 'Account', 'Text', 'Reference', 'Document Header Text', 
                               'User Name', 'Posting period', 'Tax Code', 'Document Date', 'Amount in local currency', 'Local Currency', 'Amount in doc. curr.', 'Document currency', 'Posting Date',
                               'Period', 'Doc. Date', 'Entered', 'Pstng Date', 'Key_Concat', 'Key_Reversal', 'Period_Rev', 'Doc. Date_Rev', 'Entered_Rev', 'Pstng Date_Rev',]]
    date_columns = ['Document Date', 'Posting Date', 'Doc. Date', 'Entered', 'Pstng Date']
    # Convert to datetime and then extract the date
    FBL3N_new[date_columns] = FBL3N_new[date_columns].apply(pd.to_datetime).apply(lambda x: x.dt.date)
    
    
    
    # st.write('fbl3n categorizado con reglas')
    # st.dataframe(FBL3N_new)

    
    tab1, tab2 = st.tabs(["Resumen", "Detalle"])
    
    with tab1:
        st.subheader('Resumen')
        FBL3N_summary = FBL3N_new.copy()
        # FBL3N_summary['K1'] = FBL3N_summary['Company Code'] + FBL3N_summary['CoCd'] + FBL3N_summary['Document currency'] + (FBL3N_summary['Subcode_ML'].astype(str))
        # FBL3N_summary['K2'] = FBL3N_summary['CoCd'] + FBL3N_summary['Company Code'] + FBL3N_summary['Document currency'] + (FBL3N_summary['Code_RP'].astype(str))
        # FBL3N_summary = FBL3N_summary.groupby(by=['Company Code', 'CoCd', 'Subcode_ML', 'Code_Type', 'Code_Desc', 'Code_RP', 'Document currency', 'K1', 'K2'], as_index=False)['Amount in doc. curr.'].sum()
       
        # FBL3N_summary2 = FBL3N_summary.copy()
        # FBL3N_summary2.columns = [col_name + '_k2' for col_name in FBL3N_summary2]
        # FBL3N_summary = FBL3N_summary.merge(FBL3N_summary2, left_on="K1", right_on='K2_k2', how='left')
        # FBL3N_summary = FBL3N_summary.drop(columns=['K1', 'K2','Company Code_k2','CoCd_k2','Subcode_ML_k2','Code_Type_k2','Code_Desc_k2','Code_RP_k2','K1_k2','K2_k2'])
        # # FBL3N_summary = FBL3N_summary[['Document currency', 'Amount in doc. curr.', 'Document currency_k2', 'Amount in doc. curr._k2']].fillna(0)
        # # FBL3N_summary = FBL3N_summary[['Amount in doc. curr.', 'Amount in doc. curr._k2']].fillna(0)
        # FBL3N_summary['Diferencia'] = FBL3N_summary['Amount in doc. curr.'] + FBL3N_summary['Amount in doc. curr._k2']
    
        # st.dataframe(FBL3N_summary)
        # st.write(FBL3N_summary.columns)

    with tab2:
        #-------- Para volver a cruzar el dataframe con el Subcode ajustado con el catalogo de cuentas y los subcodigos
        # FBL3N_new = FBL3N_new.merge(accounts, left_on="Account", right_on='GL_Account', how='left')
        # FBL3N_new = FBL3N_new.merge(subcodes, left_on="Subcode", right_on='Code', how='left')

        
        # FBL3N_new['Key1'] = FBL3N_new['Company Code'] + FBL3N_new['CoCd'] + (FBL3N_new['Document Date'].astype(str)) + (FBL3N_new['Amount in doc. curr.'].astype(str))
        # FBL3N_new['Key2'] = FBL3N_new['CoCd'] + FBL3N_new['Company Code'] + (FBL3N_new['Document Date'].astype(str)) + (-FBL3N_new['Amount in doc. curr.']).astype(str)
        FBL3N_new['Key1'] = FBL3N_new['Company Code'] + FBL3N_new['Related Party'] + (FBL3N_new['Amount in doc. curr.'].astype(str))
        FBL3N_new['Key2'] = FBL3N_new['Related Party'] + FBL3N_new['Company Code'] + (-FBL3N_new['Amount in doc. curr.']).astype(str)
        
        FBL3N_new['Counter1'] = FBL3N_new.groupby('Key1').cumcount()
        FBL3N_new['Counter1'] += 0 # Sumar 1 al contador para que comience desde 1 en lugar de 0
        FBL3N_new['Key_1'] = FBL3N_new['Key1'] + FBL3N_new['Counter1'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        FBL3N_new['Counter2'] = FBL3N_new.groupby('Key2').cumcount()
        FBL3N_new['Counter2'] += 0 # Contador para que comience desde 0
        FBL3N_new['Key_2'] = FBL3N_new['Key2'] + FBL3N_new['Counter2'].astype(str) # Crear una nueva columna 'key_modified' que contiene la columna 'key' con el contador
        
        # FBL3N_real2 = FBL3N_new.copy()
        # FBL3N_real2.columns = [col_name + '_k2' for col_name in FBL3N_real2]
        # FBL3N_real = FBL3N_real.merge(FBL3N_real2, left_on="Key1", right_on='Key2_k2', how='left')
        # st.dataframe(FBL3N_tobe_class)
        # st.dataframe(FBL3N_classified)

        #----- eliminar las columnas Key1, Key2, Counter1, Counter2
        drop_keycols = ['Key1', 'Key2', 'Counter1', 'Counter2']
        FBL3N_new = FBL3N_new.drop(columns=drop_keycols)

        integer_cols = ['Subcode', 'Account', 'Document Number']
        FBL3N_new[integer_cols] = FBL3N_new[integer_cols].apply(pd.to_numeric, errors='coerce', downcast='integer')

        
        st.dataframe(FBL3N_new)
    
    end_time02 = time.time()
    processing_time02 = end_time02 - start_time02
    processing_time_formatted02 = "{:.4f}".format(processing_time02)
    st.info(f'Subcodes has been assigned to the new FBL3N dataset according to the Machine Learning Model in: {processing_time_formatted02} seconds')
    
    Sdos_Fin_Accounts = saldos_financieros['Concat'].unique()
    ZLAAUDIT_filtrado = ZLAAUDIT[ZLAAUDIT['CONCAT_2'].isin(Sdos_Fin_Accounts)]
    ZLAAUDIT_grouped = ZLAAUDIT_filtrado.groupby(by=['CONCAT', 'Account', 'Local Currency'], as_index=False).agg({'Debit/credit amount': 'sum'})

    ZLAAUDIT_notPnL = ZLAAUDIT.copy()
       
    def PnL_notPnL(row):
        # Verificar las condiciones para 'NotPnL'
        if (row['Account'].startswith(("2", "3", "4", "5", "6", "7", "8", "9")) and len(row['Account']) == 10):
            return "NotPnL"
        else:
            return ''
    
    ZLAAUDIT_notPnL['segmento'] = ZLAAUDIT_notPnL.apply(PnL_notPnL, axis=1)
    ZLAAUDIT_notPnL = ZLAAUDIT_notPnL[(~ZLAAUDIT_notPnL['CONCAT_2'].isin(Sdos_Fin_Accounts)) & (ZLAAUDIT_notPnL['segmento'] == "NotPnL")]
    ZLAAUDIT_grouped_notPnL = ZLAAUDIT_notPnL.groupby(by=['CONCAT', 'Account', 'Local Currency'], as_index=False).agg({'Debit/credit amount': 'sum'})
    ZLAAUDIT_grouped_notPnL = ZLAAUDIT_grouped_notPnL[ZLAAUDIT_grouped_notPnL['Debit/credit amount'] != 0]


    #Cuentas unicas de Impuestos en Saldos Financieros
    tax_accounts = tax_accounts[['Debit Account']].drop_duplicates()
    # st.write('new cuentas impuestos')
    # st.dataframe(tax_accounts)
    ZLAAUDIT_filtrado_tax = ZLAAUDIT[ZLAAUDIT['Account'].isin(tax_accounts['Debit Account'])]
    # st.dataframe(ZLAAUDIT_filtrado_tax)
    ZLAAUDIT_grouped_tax = ZLAAUDIT_filtrado_tax.groupby(by=['CONCAT', 'Account', 'Local Currency'], as_index=False).agg({'Debit/credit amount': 'sum'})
    # st.dataframe(ZLAAUDIT_grouped_tax)


    
    # Sdos_Fin_Accounts_tax = saldos_financieros[['Concat', 'Type']].drop_duplicates()
    # Sdos_Fin_Accounts_tax = Sdos_Fin_Accounts_tax[Sdos_Fin_Accounts_tax ['Type'] == 'Cuentas de Impuestos']
    # st.write('cuentas de impuestos')
    # st.dataframe(Sdos_Fin_Accounts_tax)
    # ZLAAUDIT_filtrado_tax = ZLAAUDIT[ZLAAUDIT['CONCAT_2'].isin(Sdos_Fin_Accounts_tax['Concat'])]
    # ZLAAUDIT_filtrado_tax = ZLAAUDIT_filtrado_tax.merge(Sdos_Fin_Accounts_tax, left_on="CONCAT_2", right_on='Concat', how='left')
    # st.write('cuentas de impuestos')
    # st.dataframe(ZLAAUDIT_filtrado_tax)
    # ZLAAUDIT_grouped_tax = ZLAAUDIT_filtrado_tax.groupby(by=['CONCAT', 'Account', 'Local Currency', 'Type'], as_index=False).agg({'Debit/credit amount': 'sum'})
    # st.write('cuentas de impuestos')
    # st.dataframe(ZLAAUDIT_grouped_tax)

    
    FBL3N_new = FBL3N_new.merge(ZLAAUDIT_grouped_tax, left_on="CONCAT", right_on='CONCAT', how='left', suffixes=('', '_taxes'))
    # st.write('fbl3n merged with taxes')
    # st.dataframe(FBL3N_new)
    delete_colsfromzla = ['Account_taxes', 'Local Currency_taxes']
    FBL3N_new = FBL3N_new.drop(columns=delete_colsfromzla)
    FBL3N_new.rename(columns={'Debit/credit amount': 'Taxes'}, inplace=True)

    #----- ZLAAUDIT KLA
    Cias_Mex = ["GIMX", "GSMX", "KCMX", "KLMX", "PRMX", "KLCM", "SAMX", "KSMX"]
    ZLAAUDIT_KLA = ZLAAUDIT[~ZLAAUDIT['Company Code'].isin(Cias_Mex)]
    ZLAAUDIT_KLA = ZLAAUDIT_KLA[['CONCAT', 'CONCAT_2', 'Company Code', 'Document Number', 'Document type', 'Tax Code', 'Line item', 'Posting Key', 'Posting period', 'Account', 'Assignment', 'User Name', 'Reference', 'Document Header Text', 'Posting Date', 'Entry Date', 'Document Date', 'Amount in foreign cur.', 'Currency', 'Debit/credit amount', 'Local Currency', 'review']]
     
#--------------

    current_datetime = datetime.now().strftime('%y%m%d_%H%M')

    file_name_fbl3n = f'FBL3N_Classified_{current_datetime}.xlsx'
    file_name_zlaaudit = f'ZLAAUDIT_{current_datetime}.xlsx'
    
    
    # Crear y guardar el archivo FBL3N
    excel_buffer_fbl3n = BytesIO()
    with pd.ExcelWriter(excel_buffer_fbl3n, engine='xlsxwriter') as writer:
        FBL3N_new.to_excel(writer, index=False, sheet_name='FBL3N')
        ZLAAUDIT_grouped.to_excel(writer, index=False, sheet_name='ZLAAUDIT_Grouped')
        ZLAAUDIT_grouped_notPnL.to_excel(writer, index=False, sheet_name='ZLAAUDIT_Grouped_NotPnL')
    
    # Descargar el archivo Excel en Streamlit
    st.download_button(
        label="Download FBL3N Classified excel file",
        data=excel_buffer_fbl3n.getvalue(),
        file_name=file_name_fbl3n,  # Puedes cambiar el nombre del archivo según tus necesidades
        key='download_button_fbl3n'
    )
    
    excel_buffer_zla = BytesIO()
    ZLAAUDIT_KLA.to_excel(excel_buffer_zla, index=False, sheet_name='ZLAAUDIT_LA')
    # Descargar el archivo Excel en Streamlit
    st.download_button(
        label="Download ZLAAUDIT Grouped File",
        data=excel_buffer_zla.getvalue(),
        file_name=file_name_zlaaudit,  # Puedes cambiar el nombre del archivo según tus necesidades
        key='download_button_zlaaudit'
    )
