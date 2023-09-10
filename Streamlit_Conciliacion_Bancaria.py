#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import streamlit as st

# Función para cargar un archivo CSV o Excel
def cargar_archivo(archivo):
    if archivo is not None:
        if archivo.name.endswith('.csv'):
            return pd.read_csv(archivo)
        elif archivo.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(archivo, engine='openpyxl')
    return None

# Función para procesar los archivos y realizar la conciliación bancaria
def procesar_archivos(archivo_empresa, archivo_banco):
    # Cargar datos en dataframes de pandas
    df_empresa = cargar_archivo(archivo_empresa)
    df_banco = cargar_archivo(archivo_banco)

    if df_empresa is None or df_banco is None:
        st.warning("Por favor, carga ambos archivos primero.")
        return None

    # Limpiar espacios y barras entre columnas
    df_empresa.columns = df_empresa.columns.str.strip()
    df_banco.columns = df_banco.columns.str.strip()

    # Supongamos que df_empresa y df_banco tienen la misma estructura de columnas
    # Ambas columnas contienen múltiples valores separados por "|"
    # Dividimos las columnas en ambas tablas y seleccionamos la columna 'Amount' y 'Date'
    df_empresa['Amount'] = df_empresa['Date|Amount|Entered by|Batch|Reference|Description'].str.split('|').str[1].astype(float)
    df_empresa['Date'] = df_empresa['Date|Amount|Entered by|Batch|Reference|Description'].str.split('|').str[0]

    df_banco['Amount'] = df_banco['Date|Amount|Entered by|Batch|Reference|Description'].str.split('|').str[1].astype(float)
    df_banco['Date'] = df_banco['Date|Amount|Entered by|Batch|Reference|Description'].str.split('|').str[0]

    # Identificar registros que no coinciden entre los dataframes
    registros_no_coinciden = df_empresa[~df_empresa[['Date', 'Amount']].apply(tuple, axis=1).isin(df_banco[['Date', 'Amount']].apply(tuple, axis=1))]

    # Imprimir los registros que no coinciden
    if registros_no_coinciden.empty:
        st.success("Todos los importes coinciden. La conciliación bancaria es exitosa.")
    else:
        st.warning("Registros que no coinciden:")
        st.write(registros_no_coinciden)

# Configuración de la aplicación
st.title("Aplicación de Conciliación Bancaria")

# Cargar archivos CSV o Excel
archivo_empresa = st.file_uploader("Cargar archivo de empresa (CSV o Excel)", type=["csv", "xls", "xlsx"])
archivo_banco = st.file_uploader("Cargar archivo de banco (CSV o Excel)", type=["csv", "xls", "xlsx"])

# Realizar la conciliación al presionar un botón
if st.button("Realizar Conciliación"):
    if archivo_empresa is not None and archivo_banco is not None:
        procesar_archivos(archivo_empresa, archivo_banco)
    else:
        st.warning("Por favor, carga ambos archivos primero.")


# In[ ]:




