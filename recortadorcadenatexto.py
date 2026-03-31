import streamlit as st
import pandas as pd

def recortar_inteligente(texto, limite):
    # Convertimos a string y manejamos nulos
    texto_str = str(texto) if pd.notna(texto) else ""
    
    # REGLA 1: Si no supera el límite, se queda como está
    if len(texto_str) <= limite:
        return texto_str
    
    # Recortamos inicialmente al límite para buscar dentro
    recorte_previo = texto_str[:limite]
    
    # REGLA 2: Buscar el último punto o la última coma
    ultimo_punto = recorte_previo.rfind('.')
    ultima_coma = recorte_previo.rfind(',')
    
    # Determinamos cuál de los dos signos está más cerca del final
    posicion_corte = max(ultimo_punto, ultima_coma)
    
    if posicion_corte != -1:
        # Retornamos hasta el signo (incluyéndolo) y limpiamos espacios
        return recorte_previo[:posicion_corte + 1].strip()
    else:
        # REGLA 3: Si no hay signos, buscamos el último espacio para no romper palabras
        ultimo_espacio = recorte_previo.rfind(' ')
        return recorte_previo[:ultimo_espacio].strip() if ultimo_espacio != -1 else recorte_previo

# --- Interfaz de Streamlit ---
st.set_page_config(page_title="SEO Text Optimizer", page_icon="✂️")

st.title("✂️ Optimizador de Títulos y Descripciones")
st.markdown("""
Esta herramienta recorta textos automáticamente buscando el **último punto o coma** para que las frases tengan sentido gramatical.
""")

with st.sidebar:
    st.header("Ajustes")
    modo = st.radio("Tipo de contenido:", ["Título (128 car.)", "Descripción (2000 car.)"])
    limite = 128 if "Título" in modo else 2000

archivo_subido = st.file_uploader("Carga tu Excel", type=["xlsx", "xls"])

if archivo_subido:
    df = pd.read_excel(archivo_subido)
    columna_objetivo = st.selectbox("Selecciona la columna a recortar:", df.columns)
    
    if st.button("Ejecutar limpieza"):
        # Aplicamos la función
        df[f"{columna_objetivo}_OPTIMIZADO"] = df[columna_objetivo].apply(lambda x: recortar_inteligente(x, limite))
        
        # Mostramos comparativa de caracteres
        st.subheader("Vista previa del resultado")
        # Mostramos solo las columnas relevantes para comparar
        st.dataframe(df[[columna_objetivo, f"{columna_objetivo}_OPTIMIZADO"]].head(10))
        
        # Botón para descargar
        csv = df.to_csv(index=False).encode('utf-8-sig') # utf-8-sig para que Excel lea bien las tildes
        st.download_button(
            label="Descargar archivo corregido",
            data=csv,
            file_name="resultado_seo.csv",
            mime="text/csv"
        )