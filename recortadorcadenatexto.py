def recortar_limpio(texto, limite):
    texto_str = str(texto).strip() if pd.notna(texto) else ""
    
    # 1. Si el texto es más corto que el límite, igual revisamos si termina en coma o espacio
    if len(texto_str) <= limite:
        # Caso específico: si termina en ", Total" o similar, lo quitamos
        # Buscamos si hay una coma sospechosa cerca del final del string
        if "," in texto_str[-7:]: # Miramos los últimos caracteres
            ultima_coma = texto_str.rfind(',')
            return texto_str[:ultima_coma].strip()
        return texto_str

    # 2. Si excede el límite, cortamos estrictamente al límite para analizar
    recorte_previo = texto_str[:limite]
    
    # Buscamos puntos, comas y espacios
    ultimo_punto = recorte_previo.rfind('.')
    ultima_coma = recorte_previo.rfind(',')
    ultimo_espacio = recorte_previo.rfind(' ')

    # LÓGICA PARA TÍTULOS (CORTOS)
    if limite <= 200:
        # Priorizamos quitar la coma si existe (para evitar el ", Total")
        if ultima_coma != -1 and ultima_coma > (limite * 0.7):
            return recorte_previo[:ultima_coma].strip()
        # Si no, por el último espacio para no romper palabras
        if ultimo_espacio != -1:
            return recorte_previo[:ultimo_espacio].strip()
            
    # LÓGICA PARA DESCRIPCIONES (LARGAS)
    else:
        # Priorizamos el último punto para cerrar frases completas
        if ultimo_punto != -1 and ultimo_punto > (limite * 0.8):
            return recorte_previo[:ultimo_punto + 1].strip()
        # Si no hay punto, buscamos la coma
        if ultima_coma != -1 and ultima_coma > (limite * 0.8):
            return recorte_previo[:ultima_coma].strip()
        # Si no, el último espacio
        if ultimo_espacio != -1:
            return recorte_previo[:ultimo_espacio].strip()

    return recorte_previo