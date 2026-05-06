import streamlit as st
import pandas as pd
import io

def recortar_limpio(texto, limite):
    """
    Recorta un texto de forma inteligente sin romper palabras 
    y priorizando signos de puntuación.
    """
    texto_str = str(texto).strip() if pd.notna(texto) else ""
    
    # REGLA: Si ya cumple el límite, no tocar nada
    if len(texto_str) <= limite:
        return texto_str
    
    # Tomamos una muestra ligeramente mayor para ver qué hay en el borde
    # pero el corte final debe estar dentro del 'limite'
    muestra = texto_str[:limite]
    
    # 1. Intentar cortar en el último punto (ideal para descripciones)
    ultimo_punto = muestra.rfind('.')
    # 2. Intentar cortar en la última coma (bueno para títulos)
    ultima_coma = muestra.rfind(',')
    # 3. Intentar cortar en el último espacio (mínimo aceptable)
    ultimo_espacio = muestra.rfind(' ')

    # Lógica de decisión de corte
    if ultimo_punto != -1 and ultimo_punto > (limite * 0.8):
        # Si hay un punto cerca del final, cortamos ahí (incluyendo el punto)
        return muestra[:ultimo_punto + 1].strip()
    
    elif ultima_coma != -1 and ultima_coma > (limite * 0.8):
        # Si hay una coma cerca del final, cortamos antes de la coma
        return muestra[:ultima_coma].strip()
    
    elif ultimo_espacio != -1:
        # Si no hay signos claros, cortamos en el último espacio
        return muestra[:ultimo_espacio].strip()
    
    return muestra

# --- Interfaz Streamlit ---
st.set_page_config(page_title="Optimizador de Catálogo", page_icon="📦")
st.title("📦 Generador de Títulos/Descripciones SEO")

with st.sidebar:
    st.header("Ajustes de Recorte")
    modo = st.radio("Tipo de campo:", ["Título (128)", "Descripción (2000)"])
    limite = 128 if "Título" in modo else 2000

archivo = st.file_uploader("Sube tu Excel original", type=["xlsx"])

if archivo:
    df_original = pd.read_excel(archivo)
    
    col_sku = st.selectbox("Selecciona la columna de SKU / Referencia:", df_original.columns)
    col_texto = st.selectbox("Selecciona la columna de Texto a recortar:", df_original.columns)
    
    if st.button("Procesar y generar Excel"):
        df_resultado = pd.DataFrame()
        df_resultado['SKU_Referencia'] = df_original[col_sku]
        
        # Aplicamos la nueva lógica
        df_resultado['Texto_Optimizado'] = df_original[col_texto].apply(
            lambda x: recortar_limpio(x, limite)
        )
        
        # Estadísticas de ayuda
        st.subheader("Vista previa")
        st.dataframe(df_resultado.head(10))
        
        # Exportación
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False, sheet_name='Resultado')
        
        st.download_button(
            label="⬇️ Descargar Excel Optimizado",
            data=buffer.getvalue(),
            file_name="catalogo_optimizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )