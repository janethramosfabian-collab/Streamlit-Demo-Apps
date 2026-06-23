import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# CONFIGURACIÓN Y CONSTANTES GLOBALES
# ==========================================

RUTA_CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_PRESIDENTES = os.path.join(RUTA_CARPETA, "presidentesColombia.csv")

# Diccionario de colores para los presidentes
COLORES_PRESIDENTES = {
    "Andrés Pastrana Arango": "#FF4B4B",
    "Álvaro Uribe Vélez (1º periodo)": "#AD6D15",
    "Álvaro Uribe Vélez (2º periodo)": "#FFD166",
    "Juan Manuel Santos (1º periodo)": "#06D6A0",
    "Juan Manuel Santos (2º periodo)": "#118AB2",
    "Iván Duque": "#073B4C",
    "Gustavo Petro": "#9B5DE5"
}

# ==========================================
# FUNCIONES DE PROCESAMIENTO DE DATOS
# ==========================================

@st.cache_data
def cargar_terminos_presidentes(ruta_archivo):
    """
    Lee el archivo CSV de presidentes y define las fechas exactas de inicio y fin de cada gobierno.
    Cada mandato en Colombia comienza el 7 de agosto de un año y termina el 6 de agosto 4 años después.
    """
    if not os.path.exists(ruta_archivo):
        st.error(f"No se encontró el archivo de presidentes en {ruta_archivo}")
        return []
    
    # Lee el archivo de presidentes en un DataFrame.
    df_presidentes = pd.read_csv(ruta_archivo)
    terminos = []
    
    for _, fila in df_presidentes.iterrows():
        nombre = fila['Presidente']
        anio_inicio = int(fila['Inicio del mandato'])
        valor_fin = str(fila['Fin del mandato'])
        
        # Ajusta el año de fin si el presidente actual no tiene fecha de término definida.
        anio_fin = 2026 if 'actual' in valor_fin else int(valor_fin.split()[0])
            
        terminos.append({
            "name": nombre,
            "start_date": pd.Timestamp(year=anio_inicio, month=8, day=7),
            "end_date": pd.Timestamp(year=anio_fin, month=8, day=6)
        })
    return terminos

def mapear_fechas_a_presidente_y_mes(fechas, terminos):
    """
    Determina qué presidente gobernaba en cada fecha y en qué mes de su mandato ocurrió (1 a 48).
    """
    # Inicializa las series de resultados con el mismo índice de las fechas.
    presidentes = pd.Series(index=fechas.index, dtype='object')
    meses = pd.Series(index=fechas.index, dtype='float64')
    
    for termino in terminos:
        # Crea una máscara booleana con las fechas que caen dentro del mandato actual.
        mascara = (fechas >= termino["start_date"]) & (fechas <= termino["end_date"])
        if not mascara.any():
            continue
        
        # Asigna el nombre del presidente para las fechas correspondientes.
        presidentes.loc[mascara] = termino["name"]
        
        # Calcula el mes de mandato para las fechas dentro del mandato.
        fechas_enmascaradas = fechas.loc[mascara]
        diferencia_anios = fechas_enmascaradas.dt.year - termino["start_date"].year
        diferencia_meses = diferencia_anios * 12 + fechas_enmascaradas.dt.month - termino["start_date"].month
        
        # Ajusta el cálculo si el día del mes es anterior al día de inicio del mandato.
        ajuste_dia = (fechas_enmascaradas.dt.day < termino["start_date"].day).astype(int)
        meses_diferencia = diferencia_meses - ajuste_dia
        
        # El primer mes del mandato es 1 y el máximo es 48.
        meses.loc[mascara] = (meses_diferencia + 1).clip(1, 48)
            
    return presidentes, meses

@st.cache_data
def obtener_datos_procesados(nombre_archivo, ruta_presidentes):
    """
    Carga un archivo CSV macroeconómico e inyecta las columnas de 'Presidente' y 'Mes_Mandato'.
    """
    ruta_archivo = os.path.join(RUTA_CARPETA, nombre_archivo)
    df = pd.read_csv(ruta_archivo, sep=';', decimal=',')
    
    columna_fecha = df.columns[0]
    df[columna_fecha] = pd.to_datetime(df[columna_fecha])
    
    terminos = cargar_terminos_presidentes(ruta_presidentes)
    presidentes, meses = mapear_fechas_a_presidente_y_mes(df[columna_fecha], terminos)
    
    df['Presidente'] = presidentes
    df['Mes_Mandato'] = meses
    
    return df, columna_fecha

def normalizar_datos_pivotados(df, metodo):
    """
    Aplica transformación a los datos según el método seleccionado para comparación justa.
    """
    if metodo == "Valor Original":
        return df
    
    df_normalizado = df.copy()
    
    for columna in df.columns:
        indice_primer_valido = df[columna].first_valid_index()
        if indice_primer_valido is None:
            continue
        
        valor_inicial = df.loc[indice_primer_valido, columna]
        if pd.isna(valor_inicial) or valor_inicial == 0:
            continue
            
        if metodo == "Variación Porcentual (%)":
            df_normalizado[columna] = ((df[columna] - valor_inicial) / valor_inicial) * 100.0
        elif metodo == "Indexado (Inicio = 100)":
            df_normalizado[columna] = (df[columna] / valor_inicial) * 100.0
        elif metodo == "Escalado Min-Max (0 a 1)":
            valor_minimo = df[columna].min()
            valor_maximo = df[columna].max()
            if valor_maximo != valor_minimo:
                df_normalizado[columna] = (df[columna] - valor_minimo) / (valor_maximo - valor_minimo)
            else:
                df_normalizado[columna] = 0.0
    return df_normalizado

def procesar_datos_grafico(df, columna_fecha, columna_seleccionada, presidentes_seleccionados, metodo_normalizacion):
    """
    Filtra los datos por presidentes seleccionados, agrupa por mes de mandato,
    pivota la estructura y normaliza los datos.
    """
    df_filtrado = df[df['Presidente'].isin(presidentes_seleccionados)].dropna(subset=['Presidente', 'Mes_Mandato'])
    agrupado = df_filtrado.groupby(['Presidente', 'Mes_Mandato'])[columna_seleccionada].mean().reset_index()
    df_pivotado = agrupado.pivot(index='Mes_Mandato', columns='Presidente', values=columna_seleccionada)
    df_pivotado = df_pivotado.reindex(range(1, 49))
    df_normalizado = normalizar_datos_pivotados(df_pivotado, metodo_normalizacion)
    return df_pivotado, df_normalizado

# ==========================================
# FUNCIONES DE RENDERIZADO Y GRÁFICOS
# ==========================================

def crear_grafico_plotly(df_normalizado, columna_seleccionada, presidentes_seleccionados, metodo_normalizacion):
    """
    Construye un gráfico de líneas interactivo con Plotly para comparar periodos de 1 a 48 meses.
    """
    figura = go.Figure()
    _fg = "#1a1a2e"
    _atenuado = "#6b7280"
    _cuadricula = "rgba(0,0,0,0.06)"
    _linea = "rgba(0,0,0,0.12)"
    _cero = "rgba(0,0,0,0.18)"
    _banda_a = "rgba(0,0,0,0.02)"
    _banda_b = "rgba(0,0,0,0.04)"
    
    for presidente in df_normalizado.columns:
        if presidente in presidentes_seleccionados:
            color = COLORES_PRESIDENTES.get(presidente, "#aaaaaa")
            figura.add_trace(go.Scatter(
                x=df_normalizado.index,
                y=df_normalizado[presidente],
                name=presidente,
                mode='lines+markers',
                line=dict(color=color, width=2.5),
                marker=dict(size=5, symbol='circle'),
                connectgaps=True,
                hovertemplate=f"<b>{presidente}</b><br>Mes: %{{x}}<br>Valor: %{{y:,.2f}}<extra></extra>"
            ))
            
    for x0, x1, color, etiqueta in [
        (0.5, 12.5, _banda_a, "<b>AÑO 1</b>"),
        (12.5, 24.5, _banda_b, "<b>AÑO 2</b>"),
        (24.5, 36.5, _banda_a, "<b>AÑO 3</b>"),
        (36.5, 48.5, _banda_b, "<b>AÑO 4</b>")
    ]:
        figura.add_vrect(x0=x0, x1=x1, fillcolor=color, line_width=0, layer="below")
        figura.add_annotation(x=(x0 + x1) / 2.0, y=0.98, yref="paper", text=etiqueta, showarrow=False, font=dict(size=10, color=_atenuado))
        
    sufijo_titulo = f" ({metodo_normalizacion})" if metodo_normalizacion != "Valor Original" else ""
    
    figura.update_layout(
        title=dict(
            text=f"<b>{columna_seleccionada}</b>{sufijo_titulo}",
            font=dict(family="Outfit, sans-serif", size=15, color=_fg),
            x=0.02
        ),
        xaxis=dict(
            title=dict(text="Mes del Mandato", font=dict(size=10, color=_atenuado)),
            tickmode='array',
            tickvals=[1, 12, 13, 24, 25, 36, 37, 48],
            ticktext=['M1', 'M12', 'M13', 'M24', 'M25', 'M36', 'M37', 'M48'],
            gridcolor=_cuadricula,
            linecolor=_linea,
            tickfont=dict(size=9, color=_atenuado),
            range=[0, 49]
        ),
        yaxis=dict(
            gridcolor=_cuadricula,
            linecolor=_linea,
            tickfont=dict(size=10, color=_atenuado),
            zeroline=True,
            zerolinecolor=_cero
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=9, color=_atenuado),
            bgcolor="rgba(0,0,0,0)"
        ),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=25),
        height=380
    )
    return figura

def crear_grafico_historico(df, columna_fecha, columna_seleccionada, terminos):
    """
    Crea un gráfico interactivo continuo que muestra la variable elegida a lo largo de los años,
    coloreando franjas semitransparentes correspondientes a cada mandatario.
    """
    figura = go.Figure()
    _fg = "#1a1a2e"
    _atenuado = "#6b7280"
    _cuadricula = "rgba(0,0,0,0.06)"
    _linea = "rgba(0,0,0,0.12)"
    _cero = "rgba(0,0,0,0.18)"
    
    df_ordenado = df.dropna(subset=[columna_fecha, columna_seleccionada]).sort_values(by=columna_fecha)
    
    figura.add_trace(go.Scatter(
        x=df_ordenado[columna_fecha],
        y=df_ordenado[columna_seleccionada],
        name=columna_seleccionada,
        mode='lines',
        line=dict(color="#118AB2", width=2),
        hovertemplate="Fecha: %{x|%Y-%m-%d}<br>Valor: %{y:,.2f}<extra></extra>"
    ))
    
    for termino in terminos:
        color = COLORES_PRESIDENTES.get(termino["name"], "#aaaaaa")
        figura.add_vrect(
            x0=termino["start_date"],
            x1=termino["end_date"],
            fillcolor=color,
            opacity=0.15,
            line_width=1.5,
            line_dash="dash",
            line_color="rgba(0,0,0,0.3)",
            layer="below"
        )
        
        figura.add_annotation(
            x=termino["start_date"] + (termino["end_date"] - termino["start_date"]) / 2,
            y=0.98,
            yref="paper",
            text=f"<b>{termino['name']}</b>",
            showarrow=False,
            font=dict(size=10, color="#1a1a2e"),
            # textangle=-45,
            yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="rgba(0,0,0,0.15)",
            borderwidth=1.5,
            borderpad=4
        )
        
    figura.update_layout(
        title=dict(
            text=f"<b>Línea de Tiempo Histórica Completa ({columna_seleccionada})</b>",
            font=dict(family="Outfit, sans-serif", size=16, color=_fg),
            x=0.01
        ),
        xaxis=dict(
            title=dict(text="Fecha", font=dict(size=11, color=_atenuado)),
            gridcolor=_cuadricula,
            linecolor=_linea,
            tickfont=dict(size=10, color=_atenuado),
        ),
        yaxis=dict(
            gridcolor=_cuadricula,
            linecolor=_linea,
            tickfont=dict(size=10, color=_atenuado),
            zeroline=True,
            zerolinecolor=_cero
        ),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=65, b=45),
        height=500
    )
    return figura
