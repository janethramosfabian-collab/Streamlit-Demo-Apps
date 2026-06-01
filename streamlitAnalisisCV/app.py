"""
TUTORIAL: Optimizador de CVs con IA usando Python
-------------------------------------------------
Librerías utilizadas y comandos de instalación:

1. Streamlit: Framework para crear interfaces web interactivas rápidamente.
   -> pip install streamlit
2. Pandas: Librería fundamental para análisis y transformación de datos.
   -> pip install pandas
3. Jinja2: Motor de plantillas para generar HTML dinámico.
   -> pip install Jinja2
4. Markdown2: Convierte texto en formato Markdown a HTML.
   -> pip install markdown2
5. Json: Librería nativa de Python para manejar estructuras de datos. (No requiere instalación)

Nota: Las librerías 'utils.pdf_parser' y 'utils.gemini_analyzer' son módulos 
personalizados asumidos como parte previa del tutorial.
"""

import streamlit as st
import pandas as pd # Importado para realizar transformaciones de datos
from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_analyzer import analyze_cv
from jinja2 import Template
import markdown2

# Configuración inicial de la página web
st.set_page_config(
    page_title="Optimizador de CVs con IA",
    page_icon="📄",
    layout="wide",
)

# Cargar Material Icons y Estilos CSS Personalizados
st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Ajustes generales */
        .main { background-color: #F2EFE7; }
        h1, h2, h3 { color: #2C3E50 !important; }
        .stButton>button { border-radius: 8px; font-weight: 600; }
        .material-icons { vertical-align: middle; }
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: 600; font-size: 16px; }
        .streamlit-expanderHeader { background-color: #E7E4DB !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

def main():
    """
    Función principal que renderiza la interfaz gráfica de Streamlit y maneja 
    la lógica de la aplicación.
    
    Flujo de la aplicación:
    1. Recibe el CV en PDF y la descripción del cargo (opcional).
    2. Extrae el texto y lo envía a la IA (Gemini) para su análisis.
    3. Muestra métricas, transforma los datos de errores usando pandas, 
       y despliega sugerencias.
    4. Permite editar la información en un formulario.
    5. Exporta el CV final utilizando plantillas HTML (Jinja2).
    """
    st.markdown('<h1><span class="material-icons" style="font-size: 40px; color: #48A6A7;">description</span> Optimizador de CVs con IA</h1>', unsafe_allow_html=True)
    st.markdown("Analiza tu CV, compáralo con un perfil de cargo y genera recomendaciones estratégicas en un solo lugar.")

    # --- Sección de Entrada de Datos ---
    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<h3><span class="material-icons" style="vertical-align: middle;">upload_file</span> 1. Sube tu CV</h3>', unsafe_allow_html=True)
        uploaded_cv = st.file_uploader("Cargar CV (PDF)", type=["pdf"], label_visibility="collapsed")
    
    with col2:
        st.markdown('<h3><span class="material-icons" style="vertical-align: middle;">work_outline</span> 2. Perfil del Cargo (Opcional)</h3>', unsafe_allow_html=True)
        jd_text_input = st.text_area("Pega aquí la descripción del puesto o perfil deseado", height=150, placeholder="Ej: Buscamos un Desarrollador Python con experiencia en Streamlit y APIs de IA...", label_visibility="collapsed")

    # Botón principal de ejecución
    if st.button("Analizar y Optimizar", type="primary", use_container_width=True):
        if not uploaded_cv:
            st.error("Por favor, sube un CV antes de continuar.")
        else:
            with st.spinner("Analizando con Inteligencia Artificial..."):
                # Extracción y Análisis llamando a nuestras funciones de utilidad
                cv_text = extract_text_from_pdf(uploaded_cv)
                analysis = analyze_cv(cv_text, jd_text_input)
                
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    # Guardamos el resultado en el estado de la sesión para no perderlo al recargar la web
                    st.session_state['cv_analysis'] = analysis
                    st.session_state['analysis_done'] = True
                    st.success("Análisis completado con éxito.")

    # --- Sección de Resultados ---
    if st.session_state.get('analysis_done'):
        analysis = st.session_state['cv_analysis']
        
        # Creación de pestañas para organizar la información
        tab1, tab2, tab3 = st.tabs(["Informe de Análisis", "Editor de CV", "Exportar"])

        # PESTAÑA 1: INFORME Y TRANSFORMACIÓN DE DATOS
        with tab1:
            st.subheader("Análisis Detallado")
            
            # Cálculo y muestra del Score de Alineación
            if jd_text_input and analysis.get("alineacion_jd"):
                score = analysis["alineacion_jd"]["score"]
                st.metric("Score de Alineación", f"{score}%")
                st.progress(score / 100)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('**<span class="material-icons" style="color: green; font-size: 18px; vertical-align: middle;">check_circle</span> Habilidades coincidentes:**', unsafe_allow_html=True)
                    for skill in analysis["alineacion_jd"]["habilidades_coincidentes"]:
                        st.markdown(f"- {skill}")
                with c2:
                    st.markdown('**<span class="material-icons" style="color: orange; font-size: 18px; vertical-align: middle;">error_outline</span> Habilidades a fortalecer:**', unsafe_allow_html=True)
                    for skill in analysis["alineacion_jd"]["habilidades_faltantes"]:
                        st.markdown(f"- {skill}")
            
            # --- TRANSFORMACIÓN DE DATOS CON PANDAS ---
            st.divider()
            st.markdown('<h3><span class="material-icons" style="color: #d32f2f; vertical-align: middle;">bug_report</span> Errores y Correcciones</h3>', unsafe_allow_html=True)
            
            if analysis.get("errores"):
                # 1. Cargamos la lista de diccionarios (JSON) en un DataFrame de pandas
                df_errores = pd.DataFrame(analysis["errores"])
                
                # 2. Transformación: Limpieza y formateo de datos
                # Capitalizamos los nombres de las columnas para mejor presentación
                df_errores.columns = [col.capitalize() for col in df_errores.columns]
                
                # 3. Transformación: Reemplazamos posibles valores nulos por texto genérico
                df_errores = df_errores.fillna("No especificado")
                
                # Mostramos el DataFrame transformado en Streamlit
                st.table(df_errores)
            else:
                st.success("No se encontraron errores críticos.")

            # Recomendaciones
            st.divider()
            st.markdown('<h3><span class="material-icons" style="color: #fbc02d; vertical-align: middle;">lightbulb</span> Recomendaciones de IA</h3>', unsafe_allow_html=True)
            if analysis.get("recomendaciones"):
                for rec in analysis["recomendaciones"]:
                    # Usamos expanders (acordeones) para ahorrar espacio
                    with st.expander(f"Mejora: {rec['original'][:60]}..."):
                        st.markdown(f"**Original:** {rec['original']}")
                        st.markdown(f"**Optimizado:** {rec['optimizado']}")
                        st.info(f"**Impacto:** {rec['impacto']}")
            
            if analysis.get("sugerencias_estructura"):
                st.divider()
                st.markdown('<h3><span class="material-icons" style="color: #0288d1; vertical-align: middle;">info</span> Sugerencias de Estructura</h3>', unsafe_allow_html=True)
                for sug in analysis["sugerencias_estructura"]:
                    st.info(sug)

        # PESTAÑA 2: EDITOR DEL CV
        with tab2:
            st.subheader("Editor Estratégico")
            st.info("Ajusta tu información basándote en el análisis anterior. Los campos se han pre-llenado con las sugerencias de la IA.")
            
            # Obtenemos los datos sugeridos por la IA, o un diccionario vacío si no existen
            opt = analysis.get("cv_optimizado", {})
            
            # Formulario para que el usuario edite la respuesta de la IA antes de exportar
            with st.form("cv_editor_form"):
                col_n, col_e = st.columns(2)
                with col_n:
                    nombre = st.text_input("Nombre Completo", value=opt.get("nombre", ""))
                with col_e:
                    email = st.text_input("Correo Electrónico", value=opt.get("email", ""))
                
                col_t, col_u = st.columns(2)
                with col_t:
                    telefono = st.text_input("Teléfono", value=opt.get("telefono", ""))
                with col_u:
                    ubicacion = st.text_input("Ubicación", value=opt.get("ubicacion", ""))
                
                exp_text = st.text_area("Experiencia Profesional (Markdown)", value=opt.get("experiencia", ""), height=350)
                edu_text = st.text_area("Educación y Formación (Markdown)", value=opt.get("educacion", ""), height=200)
                hab_text = st.text_area("Habilidades (Markdown)", value=opt.get("habilidades", ""), height=150)
                
                # Al enviar el formulario, guardamos los cambios en el session_state
                if st.form_submit_button("Guardar Cambios para Exportar"):
                    st.session_state['edited_cv'] = {
                        "metadata": {"nombre": nombre, "email": email, "telefono": telefono, "ubicacion": ubicacion},
                        "experiencia": exp_text,
                        "educacion": edu_text,
                        "habilidades": hab_text
                    }
                    st.success("Cambios guardados. Pasa a la pestaña 'Exportar'.")

        # PESTAÑA 3: RENDERIZADO Y EXPORTACIÓN HTML
        with tab3:
            st.subheader("Generar Archivo")
            if 'edited_cv' not in st.session_state:
                st.warning("Primero completa los datos en la pestaña 'Editor' y guárdalos.")
            else:
                cv_data = st.session_state['edited_cv']
                
                # Convertimos el código Markdown escrito en el editor a etiquetas HTML
                exp_html = markdown2.markdown(cv_data.get('experiencia', ""))
                edu_html = markdown2.markdown(cv_data.get('educacion', ""))
                hab_html = markdown2.markdown(cv_data.get('habilidades', ""))
                
                # Plantilla base en HTML usando Jinja2 para inyectar variables dinámicas
                html_template = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>CV - {{ metadata.nombre }}</title>
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <style>
                        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 850px; margin: auto; padding: 50px; }
                        h1 { color: #2c3e50; border-bottom: 3px solid #2c3e50; margin-bottom: 10px; font-size: 2.5em; }
                        .info { font-style: italic; color: #555; margin-bottom: 30px; display: flex; align-items: center; flex-wrap: wrap; gap: 15px; }
                        .info-item { display: flex; align-items: center; gap: 5px; }
                        .info-item .material-icons { font-size: 18px; color: #2c3e50; }
                        h2 { color: #2980b9; border-bottom: 1px solid #ddd; padding-bottom: 8px; margin-top: 40px; display: flex; align-items: center; gap: 10px; }
                        h2 .material-icons { font-size: 24px; }
                        .content { margin-top: 15px; }
                        .content ul { list-style-type: disc; padding-left: 25px; margin-bottom: 15px; }
                        .content li { margin-bottom: 5px; }
                        @media print {
                            body { padding: 20px; }
                            .no-print { display: none; }
                        }
                    </style>
                </head>
                <body>
                    <h1>{{ metadata.nombre }}</h1>
                    <div class="info">
                        <div class="info-item"><span class="material-icons">email</span> {{ metadata.email }}</div>
                        <div class="info-item"><span class="material-icons">phone</span> {{ metadata.telefono }}</div>
                        <div class="info-item"><span class="material-icons">place</span> {{ metadata.ubicacion }}</div>
                    </div>
                    
                    <h2><span class="material-icons">history_edu</span> Experiencia Profesional</h2>
                    <div class="content">{{ experiencia_html | safe }}</div>
                    
                    <h2><span class="material-icons">stars</span> Habilidades</h2>
                    <div class="content">{{ habilidades_html | safe }}</div>

                    <h2><span class="material-icons">school</span> Educación</h2>
                    <div class="content">{{ educacion_html | safe }}</div>
                </body>
                </html>
                """
                
                # Compilamos la plantilla con Jinja2
                t = Template(html_template)
                
                # Inyectamos los datos renderizados (el filtro 'safe' en el HTML evita que escape las etiquetas)
                rendered_html = t.render(
                    metadata=cv_data['metadata'],
                    experiencia_html=exp_html,
                    educacion_html=edu_html,
                    habilidades_html=hab_html
                )
                
                st.markdown("### Previsualización Profesional")
                # Mostramos un iframe dentro de Streamlit con el resultado final
                st.components.v1.html(rendered_html, height=500, scrolling=True)
                
                # Botón para descargar el HTML generado
                st.download_button(
                    label="Descargar CV optimizado",
                    data=rendered_html,
                    file_name=f"CV_{cv_data['metadata']['nombre'].replace(' ', '_')}.html",
                    mime="text/html",
                    use_container_width=True
                )
                st.caption("Abre el archivo descargado en tu navegador y usa 'Imprimir' (Ctrl+P / Cmd+P) para guardarlo como PDF con un acabado profesional.")

if __name__ == "__main__":
    main()