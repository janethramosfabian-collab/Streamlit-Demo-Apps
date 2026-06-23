import os
import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA APLICACIÓN WEB
# ==========================================

# Configuración inicial de la página web con Streamlit.
# Define el título que aparece en la pestaña del navegador, el icono,
# el diseño de pantalla ancha (wide) y que el menú lateral comience desplegado.
st.set_page_config(
    page_title="MacroColombia - Análisis por mandatos presidenciales",
    page_icon=":material/flag:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Muestra el logotipo de Colombia (una bandera) en la parte superior del panel lateral.
st.logo("https://flagsapi.com/CO/flat/64.png",size='large')

# ==========================================
# CSS GLOBAL MÍNIMO
# ==========================================
st.markdown("""
<style>
/* Cards de los gráficos: fondo blanco, sombra sutil */
[class*="st-key-container"] {
    background: #ffffff;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. IMPORTACIONES DESDE utils.py
# ==========================================

from utils import (
    RUTA_CARPETA,
    ARCHIVO_PRESIDENTES,
    COLORES_PRESIDENTES,
    cargar_terminos_presidentes,
    obtener_datos_procesados,
    procesar_datos_grafico,
    crear_grafico_plotly,
    crear_grafico_historico,
)

# ==========================================
# 3. CARGA DE ARCHIVOS E INICIALIZACIÓN
# ==========================================

# Escanea la carpeta y hace una lista con todos los archivos CSV de indicadores económicos,
# excluyendo el archivo que contiene la lista de los presidentes.
todos_los_archivos = sorted([f for f in os.listdir(RUTA_CARPETA) if f.endswith('.csv') and f != "presidentesColombia.csv"])
terminos = cargar_terminos_presidentes(ARCHIVO_PRESIDENTES)
nombres_presidentes = [t["name"] for t in terminos]

# ==========================================
# 5. DISEÑO DE LA INTERFAZ DE USUARIO (UI)
# ==========================================

# Banner o cabecera principal de la página web.
with st.container(horizontal=True, vertical_alignment="center"):
    st.image("https://flagsapi.com/CO/flat/64.png", width=150)
    st.title("MacroColombia")
st.markdown("##### Comparativa del comportamiento macroeconómico en los mandatos presidenciales (1998 - 2026)")

# --- PANEL LATERAL DE CONTROL (SIDEBAR) ---
st.sidebar.markdown("### :material/settings: Panel de control")
st.sidebar.markdown("Configura los parámetros globales del dashboard.")

# Menú desplegable para elegir el método de normalización de los datos.
metodo_normalizacion = st.sidebar.selectbox(
    "Normalización de datos",
    ["Valor Original", "Variación Porcentual (%)", "Indexado (Inicio = 100)", "Escalado Min-Max (0 a 1)"],
    help="Elige cómo deseas visualizar y comparar las tendencias."
)

# Textos explicativos para cada método de normalización que se mostrarán si el usuario los solicita.
descripciones_normalizacion = {
    "Valor Original": {
        "calculo": "Muestra los datos brutos del archivo CSV sin modificaciones.",
        "utilidad": "Permite observar el valor nominal real e histórico en sus unidades de medida originales (ej. TRM en pesos, tasas en %)."
    },
    "Variación Porcentual (%)": {
        "calculo": "Calcula el cambio relativo con respecto al primer mes del mandato: `((Valor Actual - Valor Inicial) / Valor Inicial) * 100`.",
        "utilidad": "Facilita comparar el rendimiento y crecimiento porcentual neto acumulado de cada presidente, independientemente de los valores absolutos de partida."
    },
    "Indexado (Inicio = 100)": {
        "calculo": "Establece el valor inicial del mandato en 100: `(Valor Actual / Valor Inicial) * 100`.",
        "utilidad": "Ideal para comparar trayectorias de variables (ej. tasas, inflación) partiendo desde un punto inicial idéntico e igualado para todos."
    },
    "Escalado Min-Max (0 a 1)": {
        "calculo": "Escala los datos del mandato en un rango de 0 a 1: `(Valor Actual - Mínimo) / (Máximo - Mínimo)`.",
        "utilidad": "Muestra el comportamiento relativo, la volatilidad y los puntos máximos (1) o mínimos (0) dentro del periodo de cada mandatario."
    }
}

# Define una ventana emergente interactiva (st.dialog) para explicar detalladamente 
# las matemáticas y utilidad de los métodos de normalización.
@st.dialog("Métodos de normalización", width="large")
def mostrar_popup_explicacion(metodo_seleccionado):
    st.markdown(f"### Método seleccionado: **{metodo_seleccionado}**")
    descripcion = descripciones_normalizacion[metodo_seleccionado]
    
    st.info(
        f"**Cálculo:** {descripcion['calculo']}\n\n**Utilidad:** {descripcion['utilidad']}",
        icon=":material/info:"
    )
    
    st.write("---")
    st.markdown("#### Otras alternativas disponibles:")
    for metodo, detalle in descripciones_normalizacion.items():
        if metodo != metodo_seleccionado:
            with st.expander(metodo):
                st.markdown(f"**Cálculo:** {detalle['calculo']}")
                st.markdown(f"**Utilidad:** {detalle['utilidad']}")

# Botón en la barra lateral para lanzar el popup informativo explicativo.
if st.sidebar.button("Explicación del cálculo", icon=":material/help:", width="stretch"):
    mostrar_popup_explicacion(metodo_normalizacion)

st.sidebar.markdown("### :material/person: Presidentes a comparar")
# Control de botones múltiples interactivos (pills) para seleccionar o deseleccionar qué presidentes graficar.
presidentes_seleccionados = st.sidebar.pills(
    "Seleccionar mandatarios",
    nombres_presidentes,
    default=nombres_presidentes,
    selection_mode="multi",
    help="Filtra las líneas del gráfico para comparar presidentes específicos."
)

# Si el usuario desmarca todos los presidentes, la app muestra una advertencia y se detiene (no graficar nada vacío).
if not presidentes_seleccionados:
    st.warning("Selecciona al menos un presidente en el panel izquierdo para visualizar los datos.", icon=":material/warning:")
    st.stop()

# ==========================================
# 5. MÓDULOS DE RENDERIZADO Y GRÁFICOS
# ==========================================
def mostrar_metricas_variacion(df_pivotado, presidentes_seleccionados):
    """
    Genera tarjetas informativas resumidas (st.metric).
    Compara el valor del primer mes registrado contra el del último mes
    y calcula el porcentaje total de incremento o decremento durante el mandato.
    """
    presidentes_activos = [pres for pres in df_pivotado.columns if pres in presidentes_seleccionados]
    if presidentes_activos:
        with st.expander(":material/trending_up: Ver variación en el mandato", expanded=False):
            # Distribuye los presidentes seleccionados en 3 columnas de tarjetas para ahorrar espacio
            columnas = st.columns(3)
            for indice, pres in enumerate(presidentes_activos):
                datos_columna = df_pivotado[pres].dropna()
                if len(datos_columna) > 0:
                    valor_inicio = datos_columna.iloc[0]
                    valor_fin = datos_columna.iloc[-1]
                    # Fórmula de variación porcentual acumulada
                    variacion_pct = ((valor_fin - valor_inicio) / valor_inicio * 100) if valor_inicio != 0 else 0
                    
                    # Dibuja la tarjeta en pantalla (incluye minichart/Sparkline de la tendencia)
                    columnas[indice % 3].metric(
                        label=pres,
                        value=f"{valor_fin:,.2f}",
                        delta=f"{variacion_pct:+.2f}%",
                        chart_data=list(datos_columna),
                        chart_type="area"
                    )

def mostrar_tabla_estadisticas(df_pivotado, presidentes_seleccionados):
    """
    Construye una tabla detallada con los valores exactos de inicio, fin,
    cambio absoluto e incremento porcentual. Colorea los textos de forma dinámica:
    verde para aumentos y rojo para disminuciones.
    """
    with st.expander(":material/bar_chart: Ver estadísticas y rendimiento completo", expanded=False):
        datos_estadisticas = []
        for pres in df_pivotado.columns:
            if pres in presidentes_seleccionados:
                datos_columna = df_pivotado[pres].dropna()
                if len(datos_columna) > 0:
                    valor_inicio = datos_columna.iloc[0]
                    valor_fin = datos_columna.iloc[-1]
                    cambio_absoluto = valor_fin - valor_inicio
                    variacion_pct = (cambio_absoluto / valor_inicio * 100) if valor_inicio != 0 else 0
                    
                    # Agrupa los resultados del cálculo en una lista de registros
                    datos_estadisticas.append({
                        "Presidente": pres,
                        "Inicio": valor_inicio,
                        "Fin": valor_fin,
                        "Cambio Absoluto": cambio_absoluto,
                        "Crecimiento %": variacion_pct
                    })
        
        if datos_estadisticas:
            # Convierte la lista a un DataFrame para poder formatearlo e imprimirlo en pantalla
            df_estadisticas = pd.DataFrame(datos_estadisticas).set_index("Presidente")
            
            # Función auxiliar para pintar las celdas numéricas de acuerdo a su valor (+/-)
            def color_variacion(val):
                return 'color: #2ecc71;' if val > 0 else ('color: #e74c3c;' if val < 0 else '')

            # Aplica el color a la tabla
            estilo = df_estadisticas.style
            if hasattr(estilo, "map"):
                estilo = estilo.map(color_variacion, subset=["Cambio Absoluto", "Crecimiento %"])
            else:
                estilo = estilo.applymap(color_variacion, subset=["Cambio Absoluto", "Crecimiento %"])
                
            # Renderiza la tabla formateando los decimales y símbolos de porcentaje
            st.dataframe(
                estilo,
                column_config={
                    "Inicio": st.column_config.NumberColumn("Inicio", format="%.2f"),
                    "Fin": st.column_config.NumberColumn("Fin", format="%.2f"),
                    "Cambio Absoluto": st.column_config.NumberColumn("Cambio absoluto", format="%+,.2f"),
                    "Crecimiento %": st.column_config.NumberColumn("Crecimiento", format="%+,.2f%%")
                }
            )
        else:
            st.info("Sin estadísticas disponibles.")

def generar_chart_card(clave_grafico, archivo_defecto, columna_defecto):
    """
    Función contenedora para cada una de las tarjetas del grid. 
    Se encarga de renderizar la caja de selección del archivo, selección del indicador,
    cargar los datos correspondientes, graficarlos y pintar sus métricas y tablas.
    """
    # 1. Caja de selección para escoger el archivo de datos CSV
    archivo_seleccionado = st.selectbox(
        f"Archivo CSV ({clave_grafico})", 
        todos_los_archivos, 
        index=todos_los_archivos.index(archivo_defecto) if archivo_defecto in todos_los_archivos else 0,
        key=f"file_{clave_grafico}"
    )
    
    # Carga y procesa el archivo elegido
    df, columna_fecha = obtener_datos_procesados(archivo_seleccionado, ARCHIVO_PRESIDENTES)
    # Filtra únicamente las columnas numéricas que se pueden graficar
    columnas_seleccionables = [c for c in df.columns if c not in [columna_fecha, 'Archivo', 'Presidente', 'Mes_Mandato']]
    
    # 2. Caja de selección para escoger el indicador o columna del archivo
    columna_seleccionada = st.selectbox(
        f"Indicador a graficar ({clave_grafico})", 
        columnas_seleccionables, 
        index=columnas_seleccionables.index(columna_defecto) if columna_defecto in columnas_seleccionables else 0,
        key=f"col_{clave_grafico}"
    )
    
    # 3. Procesa, normaliza y pivota los datos
    df_pivotado, df_normalizado = procesar_datos_grafico(df, columna_fecha, columna_seleccionada, presidentes_seleccionados, metodo_normalizacion)
    
    # 4. Genera y dibuja el gráfico interactivo
    figura = crear_grafico_plotly(df_normalizado, columna_seleccionada, presidentes_seleccionados, metodo_normalizacion)
    st.plotly_chart(figura)
    
    # 5. Genera y dibuja las métricas y la tabla en la sección desplegable inferior
    mostrar_metricas_variacion(df_pivotado, presidentes_seleccionados)
    mostrar_tabla_estadisticas(df_pivotado, presidentes_seleccionados)

# ==========================================
# 6. MAQUETACIÓN EN CUADRÍCULA (GRID 2x2)
# ==========================================

# Divide la pantalla en dos filas con dos columnas cada una para organizar los 4 gráficos.
fila1_col1, fila1_col2 = st.columns(2)
fila2_col1, fila2_col2 = st.columns(2)

# Parámetros por defecto para cada cuadrante
valores_defecto = [
    {"file": "TRM.csv", "col": "Tasa Representativa del Mercado (TRM)"},
    {"file": "Inflación y meta.csv", "col": "Inflación total"},
    {"file": "Balanza de pagos.csv", "col": "Balanza de pagos - Cuenta corriente - trimestral"},
    {"file": "Mercado laboral y población.csv", "col": "Tasa de desempleo - total nacional"}
]

# Distribuye los cuadrantes utilizando bloques st.container(border=True) para que queden enmarcados
with fila1_col1:
    with st.container(border=True, key="container_chart_1"):
        generar_chart_card("Gráfico 1", valores_defecto[0]["file"], valores_defecto[0]["col"])

with fila1_col2:
    with st.container(border=True, key="container_chart_2"):
        generar_chart_card("Gráfico 2", valores_defecto[1]["file"], valores_defecto[1]["col"])

with fila2_col1:
    with st.container(border=True, key="container_chart_3"):
        generar_chart_card("Gráfico 3", valores_defecto[2]["file"], valores_defecto[2]["col"])

with fila2_col2:
    with st.container(border=True, key="container_chart_4"):
        generar_chart_card("Gráfico 4", valores_defecto[3]["file"], valores_defecto[3]["col"])

# ==========================================
# 7. SECCIÓN HISTÓRICA CONTINUA (LÍNEA DE TIEMPO)
# ==========================================
# Sección al final de la página para la línea de tiempo completa
st.markdown("### :material/timeline: Línea de tiempo histórica completa por mandatos")
st.markdown("Analiza la serie temporal continua y resalta los periodos presidenciales.")

with st.container(border=True, key="container_hist"):
    col_archivo, col_variable = st.columns(2)
    with col_archivo:
        archivo_historico = st.selectbox(
            "Seleccionar archivo CSV (línea de tiempo)",
            todos_los_archivos,
            index=0,
            key="file_hist_selector"
        )
    
    df_historico, columna_fecha_hist = obtener_datos_procesados(archivo_historico, ARCHIVO_PRESIDENTES)
    columnas_seleccionables_hist = [c for c in df_historico.columns if c not in [columna_fecha_hist, 'Archivo', 'Presidente', 'Mes_Mandato']]
    
    with col_variable:
        variable_historica = st.selectbox(
            "Seleccionar indicador / variable",
            columnas_seleccionables_hist,
            index=0,
            key="var_hist_selector"
        )
        
    figura_historica = crear_grafico_historico(df_historico, columna_fecha_hist, variable_historica, terminos)
    st.plotly_chart(figura_historica)