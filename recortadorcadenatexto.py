import streamlit as st
import pandas as pd
import io

def recortar_limpio(texto, limite):
    texto_str = str(texto).strip() if pd.notna(texto) else ""
    
    # REGLA: Si ya cumple el límite, no tocar nada
    if len(texto_str) <= limite:
        return texto_str
    
    # Cortamos al límite para analizar
    recorte_previo = texto_str[:limite]
    
    # Buscar último punto o coma
    ultimo_punto = recorte_previo.rfind('.')
    ultima_coma = recorte_previo.rfind(',')
    
    posicion_corte = max(ultimo_punto, ultima_coma)
    
    if posicion_corte != -1:
        # Cortamos ANTES del signo y limpiamos espacios finales
        return recorte_previo[:posicion_corte].strip()
    else:
        # Si no hay signos, buscamos el último espacio
        ultimo_espacio = recorte_previo.rfind(' ')
        if ultimo_espacio != -1:
            return recorte_previo[:ultimo_espacio].strip()
        return recorte_previo

# --- Interfaz ---
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
        # Creamos el nuevo DataFrame con la estructura solicitada
        df_resultado = pd.DataFrame()
        df_resultado['SKU_Referencia'] = df_original[col_sku]
        df_resultado['Texto_Optimizado'] = df_original[col_texto].apply(lambda x: recortar_limpio(x, limite))
        
        # Mostrar vista previa
        st.subheader("Vista previa de las 2 columnas")
        st.dataframe(df_resultado.head(10))
        
        # Lógica para descargar como EXCEL (.xlsx)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False, sheet_name='Resultado')
            # No es necesario writer.save() en las versiones nuevas de pandas con 'with'
        
        st.download_button(
            label="⬇️ Descargar Excel (A: SKU, B: Texto)",
            data=buffer.getvalue(),
            file_name="catalogo_optimizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )