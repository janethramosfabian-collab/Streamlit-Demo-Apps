# -*- coding: utf-8 -*-
# """
# MÓDULO: Entiende tu Préstamo / Understand Your Loan

# Descripción:
# Aplicación web interactiva desarrollada con Streamlit que permite ingresar
# los datos de un crédito (tal como los entrega el banco) y descubrir la cuota
# real, la tasa efectiva, los cargos ocultos y la fecha de finalización del pago.

# Este script es ideal para aprender a integrar cálculos financieros (numpy-financial),
# manipulación de datos tabulares (pandas), visualización de datos (plotly) 
# y desarrollo de interfaces web rápidas (streamlit).
# """

# ==========================================
# IMPORTACIÓN Y EXPLICACIÓN DE LIBRERÍAS
# ==========================================

# Streamlit: Framework principal para crear la interfaz web interactiva de la aplicación.
# Permite convertir scripts de datos en aplicaciones web en minutos, sin saber HTML/CSS.
# Instalación: pip install streamlit
import streamlit as st

# Pandas: Librería fundamental para la manipulación y análisis de datos en formato de tablas (DataFrames).
# En este proyecto, se usa para estructurar y totalizar la tabla de amortización del crédito.
# Instalación: pip install pandas
import pandas as pd

# NumPy Financial: Contiene funciones matemáticas financieras elementales (TIR, VAN, pago de cuotas, etc.).
# Lo usamos para calcular la cuota teórica y despejar la tasa de interés.
# Instalación: pip install numpy-financial
# https://numpy.org/numpy-financial/latest/
import numpy_financial as npf

# npf.fv(rate, nper, pmt, pv, when) - Calcula el valor futuro de una inversión.
# npf.pv(rate, nper, pmt, fv, when) - Calcula el valor presente de un préstamo o inversión.
# npf.npv(rate, values) - Calcula el valor actual neto (VAN/NPV) de flujos de efectivo.
# npf.pmt(rate, nper, pv, fv, when) - Calcula el pago periódico total de un préstamo.
# npf.ppmt(rate, per, nper, pv, fv, when) - Calcula la porción de capital de un pago específico.
# npf.ipmt(rate, per, nper, pv, fv, when) - Calcula la porción de intereses de un pago específico.
# npf.irr(values) - Calcula la tasa interna de retorno (TIR/IRR) de flujos financieros.
# npf.mirr(values, finance_rate, reinvest_rate) - Calcula la tasa interna de retorno modificada (TIRM).
# npf.nper(rate, pmt, pv, fv, when) - Calcula el número total de periodos de pago.
# npf.rate(nper, pmt, pv, fv, when, guess, tol, maxiter) - Calcula la tasa de interés por periodo.


# Plotly Graph Objects: Módulo de Plotly para crear gráficos altamente personalizados e interactivos.
# Lo usamos para crear el gráfico de pastel y el gráfico de barras apiladas.
# Instalación: pip install plotly
import plotly.graph_objects as go

# Datetime: Módulo estándar de Python para manipular fechas y horas. 
# Lo usamos para establecer la fecha actual de inicio del crédito.
# No requiere instalación (viene preinstalado con Python).
import datetime

# python-dateutil: Su clase relativedelta permite sumar/restar meses o años a una fecha 
# respetando correctamente los desbordamientos de año y los fin de mes (28/29/30/31 días).
# Instalación: pip install python-dateutil
from dateutil.relativedelta import relativedelta

# """
# =========================================================
# BLOQUE 1: CONFIGURACIÓN DE LA PÁGINA Y SIDEBAR
# =========================================================
# Aquí configuramos las propiedades básicas de la app en Streamlit y 
# creamos el menú lateral (sidebar) para la selección de idioma.
# """
st.set_page_config(
    page_title="Entiende tu Préstamo",
    page_icon=":material/calculate:",
    layout="wide",
)

with st.sidebar:
    st.markdown("### :material/language: Idioma / Language")
    locale = st.segmented_control(
        "language_selection",
        ["Español 🇪🇸", "English 🇺🇸"],
        default="Español 🇪🇸",
        label_visibility="collapsed",
    )
    is_es = locale == "Español 🇪🇸"

    st.space("medium")
    st.markdown("---")
    st.space("medium")

    with st.container(border=True):
        st.markdown(
            "#### :material/info: " + ("Sobre la App" if is_es else "About the App")
        )
        if is_es:
            st.markdown(
                "Esta aplicación usa la librería estándar `numpy-financial` para calcular la cuota real "
                "de tu crédito, la tasa efectiva y detectar cargos no explicados."
            )
        else:
            st.markdown(
                "This application uses the industry-standard `numpy-financial` library to calculate your "
                "loan's actual payment, effective rate, and detect unexplained charges."
            )

# """
# =========================================================
# BLOQUE 2: DICCIONARIO DE TEXTOS (INTERNACIONALIZACIÓN)
# =========================================================
# Almacenamos los textos de la interfaz en un diccionario para 
# cambiar fácilmente entre inglés y español dependiendo de la selección del usuario.
# """
texts = {
    "title": "🔎 Entiende tu Préstamo" if is_es else "🔎 Understand Your Loan",
    "subtitle": (
        "Ingresa los datos de tu crédito y descubre lo que realmente estás pagando."
        if is_es
        else "Enter your loan details and discover what you are really paying."
    ),        
    "assist_inputs": "Datos de tu Préstamo" if is_es else "Your Loan Details",
    "disb_date": "Fecha de Desembolso / Primer Pago" if is_es else "Disbursement Date",
    "term_months": "Plazo (en meses)" if is_es else "Term (in months)",
    "loan_val": "Monto del Préstamo (Lo que te prestan)" if is_es else "Loan Amount (What you borrow)",
    "pmt_val_lbl": "Cuota Mensual (Opcional si sabes el interés)" if is_es else "Monthly Payment (Optional if rate is known)",
    "interest_type": "Interés" if is_es else "Interest Type",
    "rate_annual_opt": "Tasa Anual (%)" if is_es else "Annual Rate (%)",
    "rate_monthly_opt": "Tasa Mensual (%)" if is_es else "Monthly Rate (%)",
    "rate_unknown_opt": "No lo sé (Calcular de la Cuota)" if is_es else "I don't know (Calculate from payment)",
    "interest_val_lbl": "Valor del Interés (%)" if is_es else "Interest Rate (%)",
    "rate_sub_type": "Tipo de Tasa Anual" if is_es else "Annual Rate Type",
    "sub_tna": "Tasa Nominal Anual (TNA)" if is_es else "Nominal Annual Rate (TNA)",
    "sub_tea": "Tasa Efectiva Anual (TEA)" if is_es else "Effective Annual Rate (TEA)",
    "additional_costs_header": "Costos Adicionales (Mensuales)" if is_es else "Additional Costs (Monthly)",
    "life_insurance": "Seguro de Vida / Deudor" if is_es else "Life / Debtor Insurance",
    "admin_fee": "Cuota de Manejo" if is_es else "Admin / Account Fee",
    "other_fees": "Otros Cargos" if is_es else "Other Charges",
    "hidden_fees": "Cargos Ocultos (No Explicados)" if is_es else "Unexplained Hidden Fees",
    "declared_fees": "Cargos Declarados" if is_es else "Declared Charges",
    "err_missing_rate_or_pmt": "Falta información: debes ingresar al menos el Interés o el valor de la Cuota." if is_es else "Missing information: you must enter either the Interest or the Payment amount.",
    "err_negative_interest": "El monto total a pagar (Cuota × Plazo) es menor o igual al monto prestado. Esto indica una tasa del 0% o negativa (préstamo subsidiado)." if is_es else "The total amount to be paid (Payment × Term) is less than or equal to the borrowed amount. This indicates a 0% or negative interest rate (subsidized loan).",
    "metric_real_pmt": "Tu Cuota Mensual" if is_es else "Your Monthly Payment",
    "metric_rate_monthly": "Tasa Mensual" if is_es else "Monthly Rate",
    "metric_rate_annual": "Tasa Anual" if is_es else "Annual Rate",
    "metric_end_date": "Fecha de Fin" if is_es else "End Date",
    "metric_total_cost": "Total a Pagar" if is_es else "Total Paid",
    "metric_borrowed": "Préstamo Original" if is_es else "Original Loan",
    "analysis_text": "Análisis Explicativo" if is_es else "Explanatory Analysis",
    "compare_warning_title": "⚠️ Comparación de Cuota" if is_es else "⚠️ Payment Comparison",
    "amort_table": "Tabla de Amortización Detallada" if is_es else "Detailed Amortization Schedule",
    "download_csv": "Descargar Calendario (CSV)" if is_es else "Download Amortization (CSV)",
}

st.title(texts["title"])
st.caption(texts["subtitle"])
st.space("medium")

# """
# =========================================================
# BLOQUE 3: INTERFAZ DE ENTRADA DE DATOS (INPUTS)
# =========================================================
# Generamos las cajas de texto, calendarios y selectores numéricos para
# que el usuario ingrese la información de su crédito.
# """
st.space("small")

cols_as = st.columns([1, 2.2])

with cols_as[0].container(border=True):
    st.markdown(f"##### :material/tune: {texts['assist_inputs']}")

    fecha_desembolso = st.date_input(texts["disb_date"], value=datetime.date.today(), key="as_date")
    plazo_meses = st.number_input(texts["term_months"], min_value=1, max_value=600, value=24, step=1, key="as_term")
    monto_prestamo = st.number_input(texts["loan_val"], min_value=0.0, max_value=1000000000.0, value=10000.0, step=500.0, format="%.2f", key="as_amount")
    cuota_ingresada = st.number_input(texts["pmt_val_lbl"], min_value=0.0, max_value=100000000.0, value=0.0, step=50.0, format="%.2f", key="as_pmt")

    opcion_interes = st.selectbox(
        texts["interest_type"],
        [texts["rate_unknown_opt"], texts["rate_annual_opt"], texts["rate_monthly_opt"]],
        key="as_rate_opt"
    )

    sub_tipo_anual = None
    if opcion_interes == texts["rate_annual_opt"]:
        sub_tipo_anual = st.segmented_control(
            texts["rate_sub_type"],
            [texts["sub_tna"], texts["sub_tea"]],
            default=texts["sub_tna"],
            key="as_annual_sub_type"
        )

    interes_ingresado = 0.0
    if opcion_interes != texts["rate_unknown_opt"]:
        interes_ingresado = st.number_input(texts["interest_val_lbl"], min_value=0.0, max_value=100.0, value=12.0, step=0.1, format="%.2f", key="as_rate_val")

    # == Costos adicionales declarados ===========================
    st.space("small")
    with st.expander(f":material/add_circle: {texts['additional_costs_header']}", expanded=False):
        st.caption(
            "Ingresa los valores mensuales que el banco te cobra además de la cuota de capital e interés. "
            "Si no los tienes claros, déjalos en 0 y el sistema los detectará automáticamente."
            if is_es else
            "Enter the monthly amounts the bank charges in addition to principal and interest. "
            "If unsure, leave them at 0 and the system will detect them automatically."
        )
        costo_seguro_vida  = st.number_input(texts["life_insurance"],  min_value=0.0, value=0.0, step=1.0, format="%.2f", key="as_seg_vida")
        costo_cuota_manejo = st.number_input(texts["admin_fee"],        min_value=0.0, value=0.0, step=1.0, format="%.2f", key="as_cta_man")
        costo_otros        = st.number_input(texts["other_fees"],       min_value=0.0, value=0.0, step=1.0, format="%.2f", key="as_otros")
    total_declared_extra = costo_seguro_vida + costo_cuota_manejo + costo_otros

# """
# =========================================================
# BLOQUE 4: CÁLCULOS FINANCIEROS Y MATEMÁTICOS
# =========================================================
# Se analiza si tenemos los datos suficientes. Dependiendo de los datos,
# usamos numpy-financial para hallar la tasa o la cuota faltante.
# """
with cols_as[1]:
    if monto_prestamo <= 0 or plazo_meses <= 0:
        st.info(
            "👋 **" + ("Bienvenido al Asistente de Préstamos" if is_es else "Welcome to the Loan Assistant") + "**\n\n" +
            ("Ingresa el **Monto del Préstamo** y el **Plazo** en la columna de la izquierda para comenzar el análisis sin tecnicismos." if is_es else "Enter the **Loan Amount** and the **Term** on the left column to start the jargon-free analysis."),
            icon=":material/info:"
        )
    else:
        has_rate = opcion_interes != texts["rate_unknown_opt"] and interes_ingresado > 0
        has_cuota = cuota_ingresada > 0

        if not has_rate and not has_cuota:
            st.warning(
                texts["err_missing_rate_or_pmt"],
                icon=":material/warning:"
            )
        else:
            calc_ok = True
            error_details = ""

            tasa_mensual = 0.0
            cuota_teorica = 0.0
            cuota_real = 0.0
            tasa_nomina_anual = 0.0
            tasa_efectiva_anual = 0.0

            if opcion_interes == texts["rate_annual_opt"]:
                # Caso 1: el usuario conoce la tasa ANUAL (TNA o TEA) y hay que llevarla a tasa mensual
                # =================================================================================
                if sub_tipo_anual == texts["sub_tna"]:
                    # TNA (Tasa Nominal Anual): se divide entre 12 para obtener la tasa mensual
                    # Ejemplo: TNA 12% anual → 1% mensual (12/12)
                    tasa_nomina_anual = interes_ingresado
                    tasa_mensual = (interes_ingresado / 100.0) / 12.0
                    # La TEA se calcula capitalizando la tasa mensual durante 12 meses
                    # TEA = ((1 + tasa_mensual)^12 - 1) * 100
                    tasa_efectiva_anual = ((1.0 + tasa_mensual) ** 12 - 1.0) * 100.0
                else: 
                    # TEA (Tasa Efectiva Anual): se descompone usando la 12ava raíz
                    # Ejemplo: TEA 12.68% → tasa_mensual ≈ 1% (porque (1.01)^12 ≈ 1.1268)
                    tasa_efectiva_anual = interes_ingresado
                    tasa_mensual = (1.0 + interes_ingresado / 100.0) ** (1.0 / 12.0) - 1.0
                    # TNA = tasa_mensual * 12 * 100 (composición simple, sin capitalización)
                    tasa_nomina_anual = tasa_mensual * 12.0 * 100.0

                if tasa_mensual == 0:
                    # Si no hay interés, la cuota es simplemente capital dividido entre los meses
                    cuota_teorica = monto_prestamo / plazo_meses
                else:
                    # npf.pmt(): Calcula la cuota fija mensual usando la fórmula de anualidad ordinaria
                    # Parámetros: (tasa_mensual, número_periodos, valor_presente, valor_futuro, tipo)
                    # Retorna valor negativo (flujo de salida), por eso usamos abs() para hacerlo positivo
                    # Fórmula: Cuota = VP * [r(1+r)^n] / [(1+r)^n - 1]
                    cuota_teorica = abs(npf.pmt(tasa_mensual, plazo_meses, monto_prestamo, 0, 0))
                cuota_real = cuota_ingresada if has_cuota else cuota_teorica

            elif opcion_interes == texts["rate_monthly_opt"]:
                # Caso 2: el usuario ya conoce directamente la tasa MENSUAL
                # =========================================================
                # Se convierte el porcentaje a decimal dividiendo entre 100
                tasa_mensual = interes_ingresado / 100.0
                # TNA se obtiene multiplicando la tasa mensual por 12 (sin capitalización)
                tasa_nomina_anual = tasa_mensual * 12.0 * 100.0
                # TEA se calcula elevando (1 + tasa_mensual) a la 12ava potencia
                # TEA = ((1 + tasa_mensual)^12 - 1) * 100
                tasa_efectiva_anual = ((1.0 + tasa_mensual) ** 12 - 1.0) * 100.0
                if tasa_mensual == 0:
                    cuota_teorica = monto_prestamo / plazo_meses
                else:
                    # Cálculo de la cuota usando la fórmula de anualidad ordinaria
                    cuota_teorica = abs(npf.pmt(tasa_mensual, plazo_meses, monto_prestamo, 0, 0))
                cuota_real = cuota_ingresada if has_cuota else cuota_teorica

            else: 
                # Caso 3: el usuario sabe su cuota pero no su tasa. Se despeja la tasa con npf.rate
                # ===============================================================================
                # Aquí usamos el método iterativo de Newton-Raphson (npf.rate) para encontrar
                # la tasa de interés implícita que hace que la cuota ingresada sea matemáticamente válida
                cuota_real = cuota_ingresada
                if cuota_real * plazo_meses <= monto_prestamo:
                    # Validación: si el total pagado es ≤ al monto prestado, no hay interés válido
                    # (ni siquiera 0%, porque al menos debe devolverse lo prestado)
                    calc_ok = False
                    error_details = texts["err_negative_interest"]
                else:
                    try:
                        # npf.rate(nper, pmt, pv, fv): Encuentra la tasa que satisface:
                        # pv + pmt*(1+r)^nper / (1+r-1) + fv/(1+r)^nper = 0
                        # Pasamos -cuota_real porque es un flujo de salida (negativo para el prestatario)
                        r = npf.rate(plazo_meses, -cuota_real, monto_prestamo, 0)
                        if pd.isna(r) or r < 0:
                            # Si no converge o da negativo, el crédito es inválido
                            calc_ok = False
                            error_details = texts["err_negative_interest"]
                        else:
                            tasa_mensual = r
                            # Conversión a tasas anuales (nominales y efectivas)
                            tasa_nomina_anual = r * 12.0 * 100.0
                            tasa_efectiva_anual = ((1.0 + r) ** 12 - 1.0) * 100.0
                            cuota_teorica = cuota_real
                    except Exception:
                        calc_ok = False
                        error_details = (
                            "No se pudo calcular una tasa de interés válida."
                            if is_es else "Could not calculate a valid interest rate."
                        )

            if not calc_ok:
                st.error(error_details, icon=":material/error:")
            else:
                cuota_sin_extras  = cuota_teorica
                cuota_con_extras  = cuota_teorica + total_declared_extra
                ocultos_por_mes  = 0.0
                is_different      = False

                if has_cuota:
                    surplus = cuota_ingresada - cuota_con_extras
                    if surplus > 0.10:
                        ocultos_por_mes = surplus
                        is_different = True
                    elif surplus < -0.10:
                        is_different = True  

                cuota_real = cuota_ingresada if has_cuota else cuota_con_extras
                difference = cuota_real - cuota_sin_extras
                
                # Construcción del cronograma de pagos iterando mes a mes
                schedule_as         = []
                balance             = monto_prestamo
                total_interest_paid = 0.0
                total_declared_paid = 0.0
                total_hidden_paid   = 0.0

                for t in range(1, plazo_meses + 1):
                    interest_t = balance * tasa_mensual

                    if tasa_mensual == 0:
                        principal_t = balance / (plazo_meses - t + 1)
                        interest_t  = 0.0
                    else:
                        pmt_t       = abs(npf.pmt(tasa_mensual, plazo_meses - t + 1, -balance, 0, 0))
                        principal_t = pmt_t - interest_t

                    declared_t = total_declared_extra
                    hidden_t   = ocultos_por_mes

                    if t == plazo_meses:
                        principal_t = balance
                        pure_t      = principal_t + interest_t
                        surplus_t   = cuota_real - pure_t - declared_t
                        hidden_t    = max(0.0, surplus_t)

                    balance -= principal_t
                    if balance < 0 or t == plazo_meses:
                        balance = 0.0

                    total_interest_paid += interest_t
                    total_declared_paid += declared_t
                    total_hidden_paid   += hidden_t

                    schedule_as.append({
                        "Mes":              t,
                        "Cuota Total":      principal_t + interest_t + declared_t + hidden_t,
                        "Capital":          principal_t,
                        "Interés":          interest_t,
                        "Seguros y Cargos": declared_t,
                        "No Explicado":     hidden_t,
                        "Saldo Pendiente":  balance,
                    })

                # """
                # =========================================================
                # BLOQUE 5: TRANSFORMACIONES CON PANDAS Y RESULTADOS
                # =========================================================
                # Aquí ocurre la magia de los DataFrames de Pandas. Convertimos 
                # la lista creada iterativamente en un DataFrame tabular robusto
                # para extraer totales, graficar y exportar fácilmente a CSV.
                # """
                # Transformación 1: Conversión de Lista de Diccionarios a DataFrame
                # Convertimos 'schedule_as' a un DataFrame. Esto ordena automáticamente
                # las claves del diccionario como columnas y nos da métodos analíticos avanzados.
                df_display_as = pd.DataFrame(schedule_as)

                # Transformación 2: Agregación o totalización (Suma de columnas)
                # Al acceder a la Serie ["Cuota Total"] del DataFrame y aplicarle .sum(),
                # Pandas calcula el valor total pagado a lo largo de toda la vida del crédito instantáneamente.
                total_pagado = df_display_as["Cuota Total"].sum()

                diferencia_total  = total_pagado - monto_prestamo
                total_extra_paid  = total_declared_paid + total_hidden_paid
                
                # relativedelta suma de manera inteligente los meses a una fecha
                fecha_terminacion = fecha_desembolso + relativedelta(months=plazo_meses)

                # == Mostrar Métricas en Streamlit ===================================
                with st.container(horizontal=True):
                    st.metric(
                        texts["metric_real_pmt"],
                        f"${cuota_real:,.2f}",
                        delta=(f"solo capital+interés: ${cuota_sin_extras:,.2f}" if total_declared_extra > 0 else None),
                        delta_color="off",
                        help="Cuota real mensual (capital + interés + todos los cargos declarados y no explicados)." if is_es else "Actual monthly payment (principal + interest + all declared and unexplained charges).",
                        border=True
                    )
                    st.metric(
                        texts["metric_rate_monthly"],
                        f"{tasa_mensual * 100.0:.2f}%",
                        help="Tasa de interés cargada mensualmente sobre el saldo pendiente." if is_es else "Interest rate charged monthly on the outstanding balance.",
                        border=True
                    )
                    st.metric(
                        texts["metric_rate_annual"],
                        f"{tasa_efectiva_anual:.2f}% TEA",
                        delta=f"{tasa_nomina_anual:.2f}% TNA",
                        delta_color="off",
                        help="TEA (Tasa Efectiva Anual) y TNA (Tasa Nominal Anual) del crédito." if is_es else "Effective and Nominal annual rates of the credit.",
                        border=True
                    )
                    st.metric(
                        texts["metric_end_date"],
                        fecha_terminacion.strftime("%d-%b-%Y"),
                        help="Fecha estimada del último pago." if is_es else "Estimated date of the last payment.",
                        border=True
                    )

                with st.container(horizontal=True):
                    st.metric(
                        texts["metric_borrowed"],
                        f"${monto_prestamo:,.2f}",
                        help="El monto original del préstamo recibido." if is_es else "The original loan amount received.",
                        border=True
                    )
                    st.metric(
                        texts["metric_total_cost"],
                        f"${total_pagado:,.2f}",
                        help="Monto total pagado al banco al finalizar el plazo (capital + intereses + todos los cargos)." if is_es else "Total paid to the bank (principal + interest + all charges).",
                        border=True
                    )
                    st.metric(
                        "Total Intereses" if is_es else "Total Interest",
                        f"${total_interest_paid:,.2f}",
                        help="Intereses puros pagados sobre el saldo de capital durante toda la vida del crédito." if is_es else "Pure interest paid on the outstanding balance over the full loan term.",
                        border=True
                    )
                    st.metric(
                        texts["declared_fees"],
                        f"${total_declared_paid:,.2f}",
                        delta=(f"+ ${total_hidden_paid:,.2f} {texts['hidden_fees']}" if total_hidden_paid > 0.5 else None),
                        delta_color="inverse" if total_hidden_paid > 0.5 else "off",
                        help="Cargos declarados (seguros, cuota de manejo, otros) acumulados en todo el plazo. El delta en rojo indica cargos no explicados detectados." if is_es else "Declared fees (insurance, admin, others) accumulated over the full term. Red delta indicates detected unexplained charges.",
                        border=True
                    )
                    st.metric(
                        "Costo Financiero Total" if is_es else "Total Cost Ratio",
                        f"{diferencia_total / monto_prestamo:.1%}",
                        help="Porcentaje de costo adicional sobre el capital prestado originalmente." if is_es else "Additional cost percentage over the originally borrowed capital.",
                        border=True
                    )

                # == Advertencias ==========================
                if is_different:
                    with st.expander(texts["compare_warning_title"], expanded=True, icon=":material/warning:"):
                        if ocultos_por_mes > 0.10:
                            st.markdown(
                                "🚨 **" + ("Cargos mensuales no explicados detectados:" if is_es else "Unexplained monthly charges detected:") + "**\n\n" +
                                (f"La cuota matemática pura (capital + interés) es **:green[${cuota_sin_extras:,.2f}]**.\n"
                                 f"Los cargos que declaraste suman **:green[${total_declared_extra:,.2f}/mes]**.\n"
                                 f"Eso totaliza **:green[${cuota_con_extras:,.2f}/mes]** que se explican.\n\n"
                                 f"Sin embargo, tu cuota real es **:green[${cuota_real:,.2f}]**, lo que deja **:green[${ocultos_por_mes:,.2f}/mes sin explicación]**.\n\n"
                                 f"**¿Qué podría ser?** Cobros administrativos, seguros adicionales no informados, impuestos locales o comisiones ocultas. Consulta a tu entidad bancaria el detalle de cada cobro."
                                 if is_es else
                                 f"The pure math payment (principal + interest) is **:green[${cuota_sin_extras:,.2f}]**.\n"
                                 f"Your declared charges add up to **:green[${total_declared_extra:,.2f}/mo]**.\n"
                                 f"That totals **:green[${cuota_con_extras:,.2f}/mo]** that is accounted for.\n\n"
                                 f"However, your actual payment is **:green[${cuota_real:,.2f}]**, leaving **:green[${ocultos_por_mes:,.2f}/mo unexplained]**.\n\n"
                                 f"**What could it be?** Administrative charges, undisclosed insurance, local taxes or hidden fees. Ask your bank for a full itemized breakdown.")
                            )
                        elif cuota_real < cuota_sin_extras - 0.10:
                            st.markdown(
                                "ℹ️ **" + ("Tu cuota real es menor que la cuota teórica calculada:" if is_es else "Your actual payment is lower than the theoretical payment:") + "**\n\n" +
                                (f"La cuota teórica es **:green[${cuota_sin_extras:,.2f}]** pero pagas **:green[${cuota_real:,.2f}]**. Esto podría indicar una tasa subsidiada, un período de gracia o una promoción bancaria especial."
                                 if is_es else
                                 f"The theoretical payment is **:green[${cuota_sin_extras:,.2f}]** but you pay **:green[${cuota_real:,.2f}]**. This might indicate a subsidized rate, grace period, or special bank promotion.")
                            )

                with st.container(border=True):
                    st.markdown("##### :material/chat_bubble: " + texts["analysis_text"])
                    pct_capital = (monto_prestamo / total_pagado) * 100
                    pct_interest = (total_interest_paid / total_pagado) * 100
                    pct_extra = (total_extra_paid / total_pagado) * 100 if total_extra_paid > 0 else 0.0

                    if is_es:
                        st.write(
                            f"De cada $100 pesos que pagues en este crédito:\n"
                            f"- **:green[${pct_capital:.1f}]** irán directamente a pagar la deuda original (capital).\n"
                            f"- **:red[${pct_interest:.1f}]** serán intereses cobrados por el banco.\n"
                        )
                        if pct_extra > 0:
                            st.write(f"- **:green[${pct_extra:.1f}]** corresponderán a cargos adicionales y seguros mensuales.")
                        st.write(
                            f"En total, por prestarte **:red[${monto_prestamo:,.2f}]**, terminarás devolviendo **:red[${total_pagado:,.2f}]** "
                            f"(es decir, **{total_pagado/monto_prestamo:.1f} veces** la cantidad prestada)."
                        )
                    else:
                        st.write(
                            f"For every $100 you pay in this loan:\n"
                            f"- **:green[${pct_capital:.1f}]** goes directly to repaying the original debt (principal).\n"
                            f"- **:red[${pct_interest:.1f}]** is interest charged by the bank.\n"
                        )
                        if pct_extra > 0:
                            st.write(f"- **:green[${pct_extra:.1f}]** corresponds to monthly fees and insurance.")
                        st.write(
                            f"En total, for borrowing **:red[${monto_prestamo:,.2f}]**, you will return **:red[${total_pagado:,.2f}]** "
                            f"(which is **{total_pagado/monto_prestamo:.1f} times** the borrowed amount)."
                        )

                st.space("small")

                # """
                # =========================================================
                # BLOQUE 6: GRÁFICOS INTERACTIVOS (PLOTLY)
                # =========================================================
                # Utilizamos Plotly para generar un gráfico circular (Pie) y uno 
                # de barras (Bar). Pandas nos permite pasar fácilmente las columnas 
                # enteras (ej. df_display_as["Capital"]) como el Eje Y.
                # """
                chart_cols_as = st.columns(2)

                with chart_cols_as[0].container(border=True):
                    st.markdown("**" + ("Composición del Costo Total" if is_es else "Total Cost Composition") + "**")
                    pie_labels = [
                        "Capital Prestado" if is_es else "Borrowed Capital",
                        "Intereses del Banco" if is_es else "Bank Interest",
                    ]
                    pie_values = [monto_prestamo, total_interest_paid]
                    pie_colors = ["#60A5FA", "#94A3B8"]

                    if total_declared_paid > 0.01:
                        pie_labels.append("Seguros y Cargos Declarados" if is_es else "Declared Fees & Insurance")
                        pie_values.append(total_declared_paid)
                        pie_colors.append("#FBBF24")

                    if total_hidden_paid > 0.5:
                        pie_labels.append("Cargos No Explicados ⚠️" if is_es else "Unexplained Charges ⚠️")
                        pie_values.append(total_hidden_paid)
                        pie_colors.append("#F87171")

                    fig_pie = go.Figure(data=[go.Pie(
                        labels=pie_labels,
                        values=pie_values,
                        hole=0.4,
                        marker=dict(colors=pie_colors)
                    )])
                    fig_pie.update_layout(
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=260,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#1E293B",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
                    )
                    st.plotly_chart(fig_pie)

                with chart_cols_as[1].container(border=True):
                    st.markdown("**" + ("Desglose Mensual" if is_es else "Monthly Breakdown") + "**")

                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(
                        x=df_display_as["Mes"],
                        y=df_display_as["Capital"],
                        name="Capital" if is_es else "Principal",
                        marker_color="#60A5FA"
                    ))
                    fig_bar.add_trace(go.Bar(
                        x=df_display_as["Mes"],
                        y=df_display_as["Interés"],
                        name="Interés" if is_es else "Interest",
                        marker_color="#94A3B8"
                    ))
                    if total_declared_paid > 0.01:
                        fig_bar.add_trace(go.Bar(
                            x=df_display_as["Mes"],
                            y=df_display_as["Seguros y Cargos"],
                            name="Seguros y Cargos" if is_es else "Fees & Insurance",
                            marker_color="#FBBF24"
                        ))
                    if total_hidden_paid > 0.5:
                        fig_bar.add_trace(go.Bar(
                            x=df_display_as["Mes"],
                            y=df_display_as["No Explicado"],
                            name="No Explicado ⚠️" if is_es else "Unexplained ⚠️",
                            marker_color="#F87171"
                        ))

                    fig_bar.update_layout(
                        barmode="stack",
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=260,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#1E293B",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                        xaxis=dict(title="Mes" if is_es else "Month"),
                        yaxis=dict(title="Monto ($)" if is_es else "Amount ($)")
                    )
                    st.plotly_chart(fig_bar)

                st.space("small")

                # """
                # =========================================================
                # BLOQUE 7: VISUALIZACIÓN DE LA TABLA Y EXPORTACIÓN CSV
                # =========================================================
                # Finalmente, aprovechamos Streamlit para renderizar el DataFrame de Pandas
                # en una tabla interactiva. También usamos el método de Pandas `.to_csv()` 
                # para permitir la descarga de la información al usuario.
                # """
                with st.container(border=True):
                    tbl_head_cols_as = st.columns([3, 1])
                    tbl_head_cols_as[0].markdown(f"**{texts['amort_table']}**")

                    # Transformación 3: Exportar el DataFrame a CSV
                    # El método .to_csv() convierte los datos a formato delimitado por comas.
                    # El parámetro "index=False" es crucial para no exportar los números de fila automáticos de Pandas.
                    # Se usa .encode('utf-8') para garantizar la compatibilidad de caracteres especiales (ñ, tildes).
                    csv_data_as = df_display_as.to_csv(index=False).encode('utf-8')
                    tbl_head_cols_as[1].download_button(
                        label=texts["download_csv"],
                        data=csv_data_as,
                        file_name="asistente_amortizacion.csv",
                        mime="text/csv",
                        icon=":material/download:",
                        key="dl_as",
                        width="content"
                    )

                    # Mostrar el DataFrame de Pandas en la interfaz de Streamlit
                    st.dataframe(
                        df_display_as,
                        column_config={
                            "Mes":              st.column_config.NumberColumn("Mes" if is_es else "Month",                      format="%d"),
                            "Cuota Total":      st.column_config.NumberColumn("Cuota Total" if is_es else "Total Payment",        format="$%,.2f"),
                            "Capital":          st.column_config.NumberColumn("Capital" if is_es else "Principal",                format="$%,.2f"),
                            "Interés":          st.column_config.NumberColumn("Interés" if is_es else "Interest",                 format="$%,.2f"),
                            "Seguros y Cargos": st.column_config.NumberColumn("Seguros / Cargos" if is_es else "Insurance & Fees", format="$%,.2f"),
                            "No Explicado":     st.column_config.NumberColumn("No Explicado ⚠️" if is_es else "Unexplained ⚠️",   format="$%,.2f"),
                            "Saldo Pendiente":  st.column_config.NumberColumn("Saldo Pendiente" if is_es else "Remaining Balance", format="$%,.2f"),
                        },
                        hide_index=True
                    )