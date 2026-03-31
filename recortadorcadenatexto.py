import streamlit as st
import pandas as pd

def recortar_texto(texto, max_caracteres):
    if pd.isna(texto) or len(str(texto)) <= max_caracteres:
        return texto
    
    texto = str(texto)[:max_caracteres]
    # Buscamos el último punto para que la frase no quede a medias
    ultimo_punto = texto.rfind('.')
    
    if ultimo_punto != -1:
        return texto[:ultimo_punto + 1]
    else:
        # Si no hay puntos, buscamos el último espacio para no cortar una palabra
        ultimo_espacio = texto.rfind(' ')
        return texto[:ultimo_espacio] if ultimo_espacio != -1 else texto

# Configuración de la interfaz
st.set_page_config(page_title="Optimizador de Textos SEO", layout="centered")
st.title("✂️ Recortador Inteligente de Excel")
st.write("Sube tu archivo y ajustaremos los textos según el límite de caracteres.")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    tipo_proceso = st.radio("¿Qué vas a procesar?", ("Título (128 car.)", "Descripción (2000 car.)"))
    limite = 128 if "Título" in tipo_proceso else 2000

# Subida de archivo
archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    columna = st.selectbox("Selecciona la columna a procesar:", df.columns)
    
    if st.button("Procesar y Descargar"):
        # Aplicamos la lógica de recorte
        df[f"{columna}_recortado"] = df[columna].apply(lambda x: recortar_texto(x, limite))
        
        st.success("¡Procesado con éxito!")
        st.dataframe(df.head()) # Vista previa

        # Botón de descarga
        @st.cache_data
        def convertir_df(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')

        csv = convertir_df(df)
        st.download_button(
            label="Descargar Excel Procesado (CSV)",
            data=csv,
            file_name="archivo_optimizado.csv",
            mime="text/csv",
        )