import streamlit as st
import pandas as pd

def load_data(file_path):
    # Cargar datos desde el archivo Excel
    df = pd.read_excel(file_path, sheet_name='FBL3N', engine='openpyxl')
    return df

def save_data(df, output_file):
    # Guardar el DataFrame modificado en un nuevo archivo Excel
    df.to_excel(output_file, index=False, sheet_name='FBL3N', engine='openpyxl')

def main():
    # Barra lateral para cargar archivos
    uploaded_file = st.sidebar.file_uploader("Cargar archivo de Excel", type=["xlsx"])

    # Verificar si se ha cargado un archivo
    if uploaded_file is not None:
        # Cargar datos desde el archivo Excel
        df = load_data(uploaded_file)

        # Verificar si existe el estado de sesión
        if 'dataframe' not in st.session_state:
            st.session_state.dataframe = df

        # Mostrar el DataFrame utilizando st.dataframe
        st.dataframe(st.session_state.dataframe)

        # Permitir la edición de la columna 'subcode'
        st.write("Editar la columna 'subcode'")
        st.session_state.dataframe['subcode'] = st.text_input("Ingrese el nuevo valor para 'subcode'")

        # Botón para guardar el DataFrame editado
        if st.button("Guardar y Descargar"):
            # Guardar el DataFrame modificado
            save_data(st.session_state.dataframe, 'output.xlsx')

            # Generar un botón de descarga
            st.download_button(
                label="Descargar DataFrame Editado",
                data='output.xlsx',
                file_name='output.xlsx',
                key='download_button'
            )

if __name__ == "__main__":
    main()
