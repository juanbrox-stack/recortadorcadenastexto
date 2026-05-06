import streamlit as st
import pandas as pd
import io

def recortar_limpio(texto, limite):
    """
    Función optimizada para SEO: 
    - Corta antes de comas finales (evita el ", Total").
    - Corta en puntos finales para descripciones.
    - Nunca deja palabras a medias.
    """
    texto_str = str(texto).strip() if pd.notna(texto) else ""
    
    if not texto_str:
        return ""

    # Si el texto es más largo que el límite, primero lo truncamos para analizar el borde
    if len(texto_str) > limite:
        texto_analizar = texto_str[:limite]
    else:
        texto_analizar = texto_str

    # Buscamos posiciones de signos de puntuación y espacios
    ultimo_punto = texto_analizar.rfind('.')
    ultima_coma = texto_analizar.rfind(',')
    ultimo_espacio = texto_analizar.rfind(' ')

    # --- CASO 1: TÍTULOS (Límites cortos, ej. 128) ---
    if limite <= 200:
        # Prioridad 1: Si hay una coma cerca del final, cortamos AHÍ (para quitar ", Total")
        # Miramos si hay una coma en los últimos 15 caracteres del recorte
        if ultima_coma != -1 and ultima_coma > (len(texto_analizar) - 15):
            return texto_analizar[:ultima_coma].strip()
        
        # Prioridad 2: Si el texto original era más largo, cortamos en el último espacio
        if len(texto_str) > limite and ultimo_espacio != -1:
            return texto_analizar[:ultimo_espacio].strip()
        
        return texto_analizar

    # --- CASO 2: DESCRIPCIONES (Límites largos, ej. 2000) ---
    else:
        # Si no llega al límite, lo devolvemos tal cual
        if len(texto_str) <= limite:
            return texto_str
            
        # Prioridad 1: Buscar el último punto para no dejar frases a medias
        if ultimo_punto != -1 and ultimo_punto > (limite * 0.85):
            return texto_analizar[:ultimo_punto + 1].strip()
        
        # Prioridad 2: Buscar la última coma
        if ultima_coma != -1 and ultima_coma > (limite * 0.85):
            return texto_analizar[:ultima_coma].strip()
        
        # Prioridad 3: Último espacio
        if ultimo_espacio != -1:
            return texto_analizar[:ultimo_espacio].strip()
        
        return texto_analizar

# --- Configuración de la Interfaz Streamlit ---
st.set_page_config(page_title="Optimizador de Catálogo SEO", page_icon="📦", layout="wide")

st.title("📦 Generador de Títulos y Descripciones SEO")
st.markdown("""
Esta herramienta recorta tus textos de forma inteligente:
- **Títulos:** Elimina comas finales y palabras cortadas.
- **Descripciones:** Intenta siempre terminar en un punto completo.
""")

with st.sidebar:
    st.header("Configuración")
    modo = st.radio("Tipo de optimización:", ["Título (128 chars)", "Descripción (2000 chars)"])
    limite = 128 if "Título" in modo else 2000
    st.info(f"El límite actual es de **{limite}** caracteres.")

archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo:
    df_original = pd.read_excel(archivo)
    
    col1, col2 = st.columns(2)
    with col1:
        col_sku = st.selectbox("Columna de SKU / Referencia:", df_original.columns)
    with col2:
        col_texto = st.selectbox("Columna de Texto a optimizar:", df_original.columns)
    
    if st.button("🚀 Procesar Catálogo"):
        # Crear copia para el resultado
        df_resultado = pd.DataFrame()
        df_resultado['SKU_Referencia'] = df_original[col_sku]
        
        # Aplicar la lógica de recorte
        df_resultado['Texto_Optimizado'] = df_original[col_texto].apply(
            lambda x: recortar_limpio(x, limite)
        )
        
        # Añadir conteo de caracteres para verificar
        df_resultado['Longitud'] = df_resultado['Texto_Optimizado'].str.len()
        
        st.success("¡Procesamiento completado!")
        
        # Vista previa
        st.subheader("Vista previa del resultado")
        st.dataframe(df_resultado.head(15), use_container_width=True)
        
        # Generar archivo de descarga
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Solo exportamos las dos columnas principales
            df_final_descarga = df_resultado[['SKU_Referencia', 'Texto_Optimizado']]
            df_final_descarga.to_excel(writer, index=False, sheet_name='SEO_Optimizado')
            
        st.download_button(
            label="⬇️ Descargar Excel Optimizado",
            data=buffer.getvalue(),
            file_name="catalogo_seo_listo.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )