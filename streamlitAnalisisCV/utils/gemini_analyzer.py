# =========================================================================================
# LIBRERÍAS Y COMANDOS DE INSTALACIÓN
# =========================================================================================
# 1. google.generativeai: SDK oficial de Google para interactuar con la IA de Gemini.
#    Comando de instalación: pip install google-generativeai
#
# 2. streamlit: Framework para crear interfaces web interactivas para datos e IA en minutos.
#    Comando de instalación: pip install streamlit
#
# 3. json: Librería estándar de Python para analizar y manipular datos en formato JSON.
#    (No requiere instalación con pip, viene integrada en Python)
#
# 4. pandas (Mencionada para transformaciones): Librería para análisis y manipulación de datos.
#    Comando de instalación: pip install pandas
# =========================================================================================

import google.generativeai as genai
import streamlit as st
import json
from typing import Optional # Importado para evitar errores con Optional[str]

def get_gemini_model():
    """
    Configura la conexión con la API de Google Gemini y devuelve una instancia del modelo.
    
    Extrae la clave de la API (API Key) desde los secretos de Streamlit (st.secrets), 
    configura la librería de Generative AI y prepara el modelo 'gemini-3.5-flash' 
    para ser utilizado en la generación de texto.

    Returns:
        genai.GenerativeModel: Objeto del modelo Gemini listo para recibir prompts.
    """
    # Obtenemos la API key almacenada de forma segura en Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
    # Configuramos la librería con nuestra credencial
    genai.configure(api_key=api_key)
    # Instanciamos y retornamos el modelo específico
    # return genai.GenerativeModel("gemini-3.5-flash")
    return genai.GenerativeModel("gemini-flash-lite-latest")

def analyze_cv(cv_text: str, jd_text: Optional[str] = None):
    """
    Analiza el texto de un Curriculum Vitae (CV) usando IA, comparándolo opcionalmente 
    con una Descripción de Puesto (JD). 
    
    Envía un prompt estructurado a Gemini pidiendo la respuesta estrictamente en JSON.
    Luego, procesa el texto generado para extraer el JSON válido.

    Args:
        cv_text (str): El contenido de texto del Curriculum Vitae.
        jd_text (Optional[str]): El contenido de texto de la oferta de trabajo (opcional).

    Returns:
        dict: Un diccionario de Python con el análisis del CV (errores, recomendaciones, 
              alineación y versión optimizada). En caso de error, retorna un diccionario con el fallo.
    """
    # Obtenemos el modelo configurado
    model = get_gemini_model()
    
    # Construimos el prompt (instrucción para la IA)
    # Le indicamos explícitamente a la IA que asuma el rol de experto en Recursos Humanos
    prompt = f"""
    Eres un experto en Reclutamiento y Selección con amplia experiencia en optimización de CVs.
    Analiza el siguiente CV y, si se proporciona, compáralo con la Descripción de Puesto (JD).
    
    Debes devolver la respuesta estrictamente en formato JSON con la siguiente estructura:
    {{
      "errores": [
        {{ "tipo": "ortografia|gramatica|fecha|inconsistencia", "texto_original": "...", "correccion": "...", "ubicacion": "..." }}
      ],
      "recomendaciones": [
        {{ "original": "...", "optimizado": "...", "impacto": "..." }}
      ],
      "alineacion_jd": {{
        "score": 0-100,
        "habilidades_coincidentes": [],
        "habilidades_faltantes": []
      }},
      "sugerencias_estructura": [],
      "cv_optimizado": {{
        "nombre": "...",
        "email": "...",
        "telefono": "...",
        "ubicacion": "...",
        "experiencia": "Contenido de experiencia en formato Markdown, incorporando las optimizaciones de logros.",
        "educacion": "Contenido de educación en formato Markdown.",
        "habilidades": "Lista de habilidades técnicas y blandas en formato Markdown, usando estrictamente viñetas (ej: - Habilidad 1\n- Habilidad 2)."
      }}
    }}

    CV:
    {cv_text}

    JD (Opcional):
    {jd_text if jd_text else "No proporcionado"}
    """
    
    # Enviamos el prompt a Gemini
    response = model.generate_content(prompt)
    
    try:
        # Extraemos el contenido de texto de la respuesta
        content = response.text
        
        # Limpieza de datos: A veces Gemini envuelve el JSON en bloques de código Markdown (```json ... ```)
        # Este bloque limpia esos caracteres para poder parsearlo correctamente.
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
            
        # TRANSFORMACIÓN DE DATOS (JSON a Diccionario)
        # Aquí convertimos el string de JSON a un diccionario nativo de Python
        datos_analisis = json.loads(content)
        
        # =========================================================================================
        # EJEMPLO EDUCATIVO: TRANSFORMACIONES DE DATOS CON PANDAS
        # Si quisiéramos analizar los errores o recomendaciones masivamente, podríamos 
        # usar pandas para transformar estas listas de diccionarios en DataFrames estructurados:
        #
        # import pandas as pd
        # 
        # 1. Transformar los errores a un DataFrame:
        # df_errores = pd.DataFrame(datos_analisis['errores'])
        # 
        # 2. Filtrar con pandas solo los errores ortográficos:
        # errores_ortograficos = df_errores[df_errores['tipo'] == 'ortografia']
        #
        # 3. Transformar recomendaciones y añadir una columna calculada:
        # df_recomendaciones = pd.DataFrame(datos_analisis['recomendaciones'])
        # df_recomendaciones['longitud_original'] = df_recomendaciones['original'].apply(len)
        # =========================================================================================
        
        return datos_analisis
        
    except Exception as e:
        # Manejo de errores: Si el JSON viene malformado o la API falla, evitamos que la app colapse
        return {
            "error": f"Error al procesar la respuesta de la IA: {str(e)}",
            "raw_response": response.text
        }