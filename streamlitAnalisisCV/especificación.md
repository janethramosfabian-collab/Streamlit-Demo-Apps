\# \*\*Especificación de Diseño de Software (SDD)\*\*



\## \*\*Analizador y Optimizador de CVs con IA\*\*



\*Proyecto Educativo | Google Gemini + Streamlit\*



\---



\## 📌 \*\*1. Introducción\*\*



\### \*\*1.1 Propósito\*\*



Desarrollar una aplicación web \*\*basada en Streamlit\*\* que permita:



\- Analizar CVs en \*\*PDF\*\* para detectar errores (ortografía, gramática, fechas, inconsistencias semánticas).

\- Comparar el CV con \*\*descripciones de puesto (Job Descriptions, JD)\*\* para evaluar alineación.

\- Generar \*\*recomendaciones estratégicas\*\* (reescritura de logros, lenguaje profesional, alineación con el mercado).

\- \*\*Editar el CV\*\* en la interfaz y exportarlo en \*\*HTML o PDF optimizado\*\*.



\### \*\*1.2 Alcance\*\*





| \*\*Incluido\*\*                                      | \*\*Excluido\*\*                                |

| ------------------------------------------------- | ------------------------------------------- |

| Análisis de PDFs con texto seleccionable          | Procesamiento de PDFs escaneados (OCR)      |

| Validación de fechas e inconsistencias semánticas | Integración con ATS (Greenhouse, Workday)   |

| Comparación con JDs subidos por el usuario        | Base de datos de ofertas de empleo públicas |

| Generación de CV en HTML/PDF                      | Almacenamiento permanente de datos          |

| Uso de Google Gemini para análisis                | Entrenamiento de modelos propios            |





\### \*\*1.3 Público Objetivo\*\*



\- \*\*Estudiantes\*\* de carreras afines a RRHH, psicología organizacional o desarrollo de software.

\- \*\*Candidatos\*\* que buscan optimizar su CV.

\- \*\*Reclutadores\*\* en formación (para práctica académica).



\---



\## 🎯 \*\*2. Requisitos Funcionales\*\*



\### \*\*2.1 Subida y Procesamiento de Archivos\*\*





| \*\*ID\*\* | \*\*Requisito\*\*           | \*\*Detalle\*\*                                                   | \*\*Prioridad\*\* |

| ------ | ----------------------- | ------------------------------------------------------------- | ------------- |

| RF-001 | Subir CV en PDF         | El usuario puede cargar un archivo PDF (máx. 10MB).           | Alta          |

| RF-002 | Subir JD en PDF/TXT     | Opcional: subir descripción de puesto para comparación.       | Media         |

| RF-003 | Extraer texto del PDF   | Usar `PyPDF2` o `pdfplumber` para extraer texto estructurado. | Alta          |

| RF-004 | Validar formato del PDF | Rechazar archivos corruptos o protegidos con contraseña.      | Alta          |





\### \*\*2.2 Análisis del CV\*\*





| \*\*ID\*\* | \*\*Requisito\*\*                              | \*\*Detalle\*\*                                                                                     | \*\*Prioridad\*\* |

| ------ | ------------------------------------------ | ----------------------------------------------------------------------------------------------- | ------------- |

| RF-010 | Detectar errores ortográficos/gramaticales | Usar Google Gemini para identificar errores en español/inglés.                                  | Alta          |

| RF-011 | Validar fechas                             | Verificar que las fechas de empleo sean consistentes (ej: no solapamientos, formato `MM/YYYY`). | Alta          |

| RF-012 | Detectar inconsistencias semánticas        | Ej: "Gerente de Ventas" vs "Jefe de Ventas" en el mismo CV.                                     | Alta          |

| RF-013 | Identificar contenido genérico             | Frases como "trabajo en equipo" sin métricas concretas.                                         | Media         |

| RF-014 | Analizar estructura                        | Secciones desordenadas, duplicadas o mal nombradas.                                             | Media         |





\### \*\*2.3 Comparación con JD\*\*





| \*\*ID\*\* | \*\*Requisito\*\*                    | \*\*Detalle\*\*                                           | \*\*Prioridad\*\* |

| ------ | -------------------------------- | ----------------------------------------------------- | ------------- |

| RF-020 | Extraer habilidades clave del JD | Usar Gemini para identificar \*skills\* requeridos.     | Alta          |

| RF-021 | Comparar habilidades CV vs JD    | Generar un \*\*score de alineación\*\* (0-100%).          | Alta          |

| RF-022 | Identificar brechas              | Listar habilidades faltantes en el CV para el puesto. | Alta          |

| RF-023 | Sugerir mejoras                  | Recomendar cómo ajustar el CV para el JD.             | Media         |





\### \*\*2.4 Generación de Recomendaciones\*\*





| \*\*ID\*\* | \*\*Requisito\*\*         | \*\*Detalle\*\*                                                                                  | \*\*Prioridad\*\* |

| ------ | --------------------- | -------------------------------------------------------------------------------------------- | ------------- |

| RF-030 | Reescribir logros     | Transformar frases genéricas en logros cuantificables (ej: "aumenté ventas en 30%").         | Alta          |

| RF-031 | Optimizar lenguaje    | Reemplazar verbos pasivos por activos (ej: "fui responsable de" → "lideré").                 | Alta          |

| RF-032 | Priorizar información | Destacar logros más relevantes según el JD.                                                  | Media         |

| RF-033 | Sugerir estructura    | Recomendar orden de secciones (ej: "Experiencia" antes de "Educación" para perfiles senior). | Baja          |





\### \*\*2.5 Edición y Exportación del CV\*\*





| \*\*ID\*\* | \*\*Requisito\*\*             | \*\*Detalle\*\*                                                   | \*\*Prioridad\*\* |

| ------ | ------------------------- | ------------------------------------------------------------- | ------------- |

| RF-040 | Editor de CV en Streamlit | Interfaz para editar texto, secciones y formato.              | Alta          |

| RF-041 | Plantillas predefinidas   | 3-5 plantillas en HTML (ej: "Clásico", "Moderno", "Técnico"). | Media         |

| RF-042 | Exportar a HTML           | Generar archivo HTML con el CV optimizado.                    | Alta          |

| RF-043 | Exportar a PDF            | Usar `weasyprint` o `pdfkit` para convertir HTML a PDF.       | Alta          |





\### \*\*2.6 Generación de Informes\*\*





| \*\*ID\*\* | \*\*Requisito\*\*                | \*\*Detalle\*\*                                                                 | \*\*Prioridad\*\* |

| ------ | ---------------------------- | --------------------------------------------------------------------------- | ------------- |

| RF-050 | Informe de errores           | Lista detallada con: error actual, corrección sugerida, ubicación en el CV. | Alta          |

| RF-051 | Informe de alineación con JD | Score de coincidencia, habilidades faltantes, sugerencias.                  | Alta          |

| RF-052 | Informe de recomendaciones   | Reescritura de logros, lenguaje, estructura.                                | Alta          |

| RF-053 | Exportar informe             | Opción para descargar en \*\*PDF o Markdown\*\*.                                | Media         |





\---



\## ⚙️ \*\*3. Requisitos No Funcionales\*\*





| \*\*Categoría\*\*      | \*\*Requisito\*\*      | \*\*Detalle\*\*                                                          |

| ------------------ | ------------------ | -------------------------------------------------------------------- |

| \*\*Rendimiento\*\*    | Tiempo de análisis | < 1 minuto para CVs de hasta 5 páginas.                              |

| \*\*Rendimiento\*\*    | Concurrentes       | Soportar 5 usuarios simultáneos (para fines educativos).             |

| \*\*Seguridad\*\*      | Datos temporales   | Los archivos subidos se eliminan después del procesamiento.          |

| \*\*Seguridad\*\*      | API Keys           | La clave de Google Gemini se guardará en `secrets.toml` (Streamlit). |

| \*\*Escalabilidad\*\*  | Arquitectura       | Monolítica (Streamlit + Python).                                     |

| \*\*Idiomas\*\*        | Soporte            | Español (principal), inglés (opcional).                              |

| \*\*Compatibilidad\*\* | Navegadores        | Chrome, Firefox, Edge (últimas versiones).                           |

| \*\*Disponibilidad\*\* | Uptime             | 99% (para entorno educativo local).                                  |





\---



\## 🏗️ \*\*4. Arquitectura del Sistema\*\*



\### \*\*4.1 Diagrama de Arquitectura\*\*



```mermaid

graph TD

&#x20;   A\[Usuario] -->|Subir CV/JD| B\[Streamlit Frontend]

&#x20;   B --> C\[Procesador de PDF]

&#x20;   B --> D\[Validador de Datos]

&#x20;   C --> E\[Extracto de Texto]

&#x20;   E --> F\[Google Gemini API]

&#x20;   F --> G\[Análisis: Errores, JD Comparison, Recomendaciones]

&#x20;   G --> H\[Generador de Informes]

&#x20;   G --> I\[Editor de CV]

&#x20;   I --> J\[Generador HTML/PDF]

&#x20;   H --> K\[Exportar Informe PDF/MD]

&#x20;   J --> L\[Exportar CV PDF/HTML]

&#x20;   K --> A

&#x20;   L --> A

```



\### \*\*4.2 Componentes Principales\*\*





| \*\*Componente\*\*            | \*\*Tecnología\*\*               | \*\*Responsabilidad\*\*                                            |

| ------------------------- | ---------------------------- | -------------------------------------------------------------- |

| \*\*Interfaz de Usuario\*\*   | Streamlit                    | Subida de archivos, visualización de resultados, editor de CV. |

| \*\*Procesador de PDF\*\*     | PyPDF2/pdfplumber            | Extraer texto estructurado del PDF.                            |

| \*\*Validador de Datos\*\*    | Python (regex)               | Validar fechas, formatos, consistencia.                        |

| \*\*Módulo de IA\*\*          | Google Gemini API            | Análisis semántico, comparación con JD, recomendaciones.       |

| \*\*Generador de CV\*\*       | Jinja2 + WeasyPrint          | Crear plantillas HTML y convertir a PDF.                       |

| \*\*Generador de Informes\*\* | Python (f-strings, Markdown) | Formatear resultados del análisis.                             |





\---



\## 🗃️ \*\*5. Diseño de Datos\*\*



\### \*\*5.1 Estructura del CV (JSON Interno)\*\*



```json

{

&#x20; "metadata": {

&#x20;   "nombre": "Germán Andrés Castaño Vásquez",

&#x20;   "email": "german@example.com",

&#x20;   "telefono": "+57 300 0000000",

&#x20;   "ubicacion": "Medellín, Colombia"

&#x20; },

&#x20; "secciones": \[

&#x20;   {

&#x20;     "tipo": "experiencia",

&#x20;     "items": \[

&#x20;       {

&#x20;         "puesto": "Gerente de Ventas",

&#x20;         "empresa": "XYZ Corp",

&#x20;         "fecha\_inicio": "01/2020",

&#x20;         "fecha\_fin": "12/2022",

&#x20;         "logros": \[

&#x20;           {

&#x20;             "original": "Aumenté ventas",

&#x20;             "optimizado": "Aumenté ventas en un 35% (de $2M a $2.7M) en 12 meses",

&#x20;             "metrica": "35%",

&#x20;             "impacto": "$700K en ingresos adicionales"

&#x20;           }

&#x20;         ]

&#x20;       }

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "tipo": "educacion",

&#x20;     "items": \[...]

&#x20;   }

&#x20; ],

&#x20; "errores": \[

&#x20;   {

&#x20;     "tipo": "ortografia",

&#x20;     "texto\_original": "persona",

&#x20;     "correccion": "personas",

&#x20;     "ubicacion": "Sección: Experiencia, Línea 5"

&#x20;   }

&#x20; ],

&#x20; "alineacion\_jd": {

&#x20;   "score": 85,

&#x20;   "habilidades\_coincidentes": \["Liderazgo", "Ventas"],

&#x20;   "habilidades\_faltantes": \["AWS", "Kubernetes"]

&#x20; }

}

```



\### \*\*5.2 Plantillas de CV (HTML)\*\*



\- \*\*Estructura base\*\*:

&#x20; ```html

&#x20; <!DOCTYPE html>

&#x20; <html>

&#x20; <head>

&#x20;   <title>{{ nombre }}</title>

&#x20;   <style>

&#x20;     /\* Estilos predefinidos para cada plantilla \*/

&#x20;     body { font-family: Arial; line-height: 1.5; }

&#x20;     .section { margin-bottom: 20px; }

&#x20;     .job-title { font-weight: bold; }

&#x20;   </style>

&#x20; </head>

&#x20; <body>

&#x20;   <h1>{{ nombre }}</h1>

&#x20;   <p>{{ email }} | {{ telefono }} | {{ ubicacion }}</p>

&#x20;   

&#x20;   {% for seccion in secciones %}

&#x20;   <div class="section">

&#x20;     <h2>{{ seccion.tipo|capitalize }}</h2>

&#x20;     {% for item in seccion.items %}

&#x20;       <h3>{{ item.puesto }} - {{ item.empresa }}</h3>

&#x20;       <p>{{ item.fecha\_inicio }} - {{ item.fecha\_fin }}</p>

&#x20;       <ul>

&#x20;         {% for logro in item.logros %}

&#x20;           <li>{{ logro.optimizado }}</li>

&#x20;         {% endfor %}

&#x20;       </ul>

&#x20;     {% endfor %}

&#x20;   </div>

&#x20;   {% endfor %}

&#x20; </body>

&#x20; </html>

&#x20; ```



\---



\## 🔄 \*\*6. Flujos de Trabajo\*\*



\### \*\*6.1 Flujo Principal: Análisis de CV\*\*



```mermaid

flowchart TD

&#x20;   A\[Inicio] --> B\[Subir CV PDF]

&#x20;   B --> C{¿Archivo válido?}

&#x20;   C -->|No| D\[Mostrar error: 'Formato inválido']

&#x20;   C -->|Sí| E\[Extraer texto con PyPDF2]

&#x20;   E --> F\[Validar estructura básica]

&#x20;   F --> G\[Enviar texto a Google Gemini]

&#x20;   G --> H\[Recibir análisis: errores, recomendaciones]

&#x20;   H --> I\[Mostrar informe en Streamlit]

&#x20;   I --> J\[Opción: Editar CV]

&#x20;   J --> K\[Guardar cambios]

&#x20;   K --> L\[Exportar CV/Informe]

&#x20;   L --> M\[Fin]

```



\### \*\*6.2 Flujo de Comparación con JD\*\*



```mermaid

flowchart TD

&#x20;   A\[Subir JD] --> B\[Extraer habilidades clave]

&#x20;   B --> C\[Comparar con CV]

&#x20;   C --> D\[Calcular score de alineación]

&#x20;   D --> E\[Identificar brechas]

&#x20;   E --> F\[Generar recomendaciones específicas]

&#x20;   F --> G\[Mostrar resultados en interfaz]

```



\---



\## 🖥️ \*\*7. Interfaz de Usuario (Streamlit)\*\*



\### \*\*7.1 Diseño de Páginas\*\*





| \*\*Página\*\*         | \*\*Contenido\*\*                                        | \*\*Componentes Streamlit\*\*                     |

| ------------------ | ---------------------------------------------------- | --------------------------------------------- |

| \*\*Inicio\*\*         | Explicación de la herramienta + botón para subir CV. | `st.title`, `st.markdown`, `st.file\_uploader` |

| \*\*Análisis\*\*       | Resultados del análisis (errores, recomendaciones).  | `st.expander`, `st.dataframe`, `st.progress`  |

| \*\*Comparación JD\*\* | Subida de JD + resultados de alineación.             | `st.file\_uploader`, `st.metric` (para score)  |

| \*\*Editor de CV\*\*   | Interfaz para editar texto y secciones.              | `st.text\_area`, `st.selectbox`, `st.button`   |

| \*\*Exportación\*\*    | Opciones para descargar CV/Informe.                  | `st.download\_button`                          |





\### \*\*7.2 Ejemplo de Código Streamlit (Estructura Base)\*\*



```python

import streamlit as st

from PyPDF2 import PdfReader

import google.generativeai as genai



\# Configuración de Google Gemini

genai.configure(api\_key=st.secrets\["GEMINI\_API\_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')



\# --- Página de Inicio ---

st.title("📄 Optimizador de CVs con IA")

st.markdown("Sube tu CV en PDF para recibir un análisis detallado y recomendaciones.")



uploaded\_cv = st.file\_uploader("Subir CV (PDF)", type=\["pdf"])

uploaded\_jd = st.file\_uploader("Subir Descripción de Puesto (Opcional)", type=\["pdf", "txt"])



if uploaded\_cv:

&#x20;   # Extraer texto del PDF

&#x20;   pdf\_reader = PdfReader(uploaded\_cv)

&#x20;   cv\_text = "\\n".join(\[page.extract\_text() for page in pdf\_reader.pages])

&#x20;   

&#x20;   # Analizar con Gemini

&#x20;   prompt = f"""

&#x20;   Analiza el siguiente CV y devuelve un JSON con:

&#x20;   1. errores: lista de errores ortográficos, gramaticales o de formato.

&#x20;   2. recomendaciones: lista de sugerencias para mejorar logros, lenguaje y estructura.

&#x20;   3. alineacion\_jd: (solo si hay JD) score de coincidencia y habilidades faltantes.

&#x20;   

&#x20;   CV: {cv\_text}

&#x20;   JD: {uploaded\_jd.read().decode() if uploaded\_jd else 'None'}

&#x20;   """

&#x20;   

&#x20;   response = model.generate\_content(prompt)

&#x20;   analysis = response.text  # JSON con resultados

&#x20;   

&#x20;   # Mostrar resultados

&#x20;   st.subheader("🔍 Resultados del Análisis")

&#x20;   st.json(analysis)  # Mostrar JSON (para depuración)

&#x20;   

&#x20;   # Opción para editar CV

&#x20;   if st.button("📝 Editar CV"):

&#x20;       st.switch\_page("pages/editor.py")

```



\---



\## 🛠️ \*\*8. Tecnologías y Dependencias\*\*





| \*\*Categoría\*\*         | \*\*Tecnología\*\*    | \*\*Versión\*\* | \*\*Uso\*\*                       |

| --------------------- | ----------------- | ----------- | ----------------------------- |

| \*\*Frontend\*\*          | Streamlit         | 1.29+       | Interfaz de usuario.          |

| \*\*Backend\*\*           | Python            | 3.10+       | Lógica de negocio.            |

| \*\*Procesamiento PDF\*\* | PyPDF2            | 3.0.0       | Extraer texto de PDFs.        |

| \*\*IA\*\*                | Google Gemini API | 1.5-flash   | Análisis semántico.           |

| \*\*Generación PDF\*\*    | WeasyPrint        | 58.1        | Convertir HTML a PDF.         |

| \*\*Plantillas HTML\*\*   | Jinja2            | 3.1.2       | Renderizar CVs.               |

| \*\*Validación\*\*        | Pydantic          | 2.5.0       | Validar estructuras de datos. |





\### \*\*8.1 Instalación (requirements.txt)\*\*



```text

streamlit==1.29.0

PyPDF2==3.0.0

google-generativeai==0.3.2

weasyprint==58.1

jinja2==3.1.2

pydantic==2.5.0

pdfplumber==0.10.3  # Alternativa a PyPDF2

```



\---



\## 📂 \*\*9. Estructura del Proyecto\*\*



```

cv-analyzer/

│

├── .streamlit/

│   └── secrets.toml          # API Key de Google Gemini

│

├── app.py                    # Página principal (Streamlit)

├── pages/

│   ├── analysis.py           # Página de análisis

│   ├── comparison.py         # Página de comparación con JD

│   ├── editor.py             # Editor de CV

│   └── export.py             # Exportación de archivos

│

├── utils/

│   ├── pdf\_parser.py         # Extracción de texto de PDFs

│   ├── gemini\_analyzer.py    # Llamadas a Google Gemini

│   ├── cv\_generator.py       # Generación de CV en HTML/PDF

│   └── validators.py         # Validación de fechas, formatos

│

├── templates/

│   ├── classic.html          # Plantilla CV Clásico

│   ├── modern.html           # Plantilla CV Moderno

│   └── technical.html        # Plantilla CV Técnico

│

├── tests/

│   ├── test\_pdf\_parser.py    # Pruebas unitarias

│   └── test\_gemini.py        # Pruebas de integración con Gemini

│

├── requirements.txt          # Dependencias

└── README.md                 # Documentación

```



\---



\## 🧪 \*\*10. Pruebas\*\*



\### \*\*10.1 Casos de Prueba Funcionales\*\*





| \*\*ID\*\* | \*\*Descripción\*\*               | \*\*Entrada\*\*                    | \*\*Resultado Esperado\*\*                       |

| ------ | ----------------------------- | ------------------------------ | -------------------------------------------- |

| TP-001 | Subir CV válido               | PDF con texto                  | Texto extraído correctamente.                |

| TP-002 | Subir CV corrupto             | PDF dañado                     | Mensaje de error: "Archivo inválido".        |

| TP-003 | Detectar error ortográfico    | CV con "persona" (error)       | Informe muestra corrección a "personas".     |

| TP-004 | Validar fechas inconsistentes | CV con solapamiento de fechas  | Advertencia: "Fechas solapadas en XYZ Corp". |

| TP-005 | Comparar con JD               | CV + JD de "Gerente de Ventas" | Score de alineación + habilidades faltantes. |

| TP-006 | Exportar CV a PDF             | CV editado en HTML             | Archivo PDF descargable.                     |





\### \*\*10.2 Pruebas de Integración\*\*



\- \*\*Google Gemini API\*\*: Verificar que las llamadas devuelvan JSON válido.

\- \*\*WeasyPrint\*\*: Asegurar que el HTML se convierta a PDF sin errores de formato.



\---



\## 📅 \*\*11. Cronograma (Estimado para Proyecto Educativo)\*\*





| \*\*Fase\*\*                           | \*\*Tareas\*\*                                                                | \*\*Duración\*\* | \*\*Entregables\*\*                             |

| ---------------------------------- | ------------------------------------------------------------------------- | ------------ | ------------------------------------------- |

| \*\*Fase 1: Setup\*\*                  | Configurar entorno, instalar dependencias, crear estructura del proyecto. | 3 días       | `requirements.txt`, estructura de carpetas. |

| \*\*Fase 2: Procesamiento de PDF\*\*   | Implementar `pdf\_parser.py` y validaciones básicas.                       | 5 días       | Módulo de extracción de texto.              |

| \*\*Fase 3: Integración con Gemini\*\* | Desarrollar `gemini\_analyzer.py` (análisis de errores, recomendaciones).  | 7 días       | Módulo de IA funcional.                     |

| \*\*Fase 4: Comparación con JD\*\*     | Implementar lógica de alineación y score.                                 | 5 días       | Módulo de comparación.                      |

| \*\*Fase 5: Editor de CV\*\*           | Crear interfaz de edición en Streamlit.                                   | 7 días       | Página `editor.py`.                         |

| \*\*Fase 6: Exportación\*\*            | Generar HTML/PDF con plantillas.                                          | 5 días       | Módulo `cv\_generator.py`.                   |

| \*\*Fase 7: Pruebas\*\*                | Pruebas unitarias e integración.                                          | 5 días       | Informe de pruebas.                         |

| \*\*Fase 8: Documentación\*\*          | README, guía de usuario, ejemplos.                                        | 3 días       | Documentación completa.                     |

| \*\*Total\*\*                          | \&nbsp;                                                                    | \*\*\~40 días\*\* | \*\*Aplicación funcional\*\*                    |





\---



\## ⚠️ \*\*12. Riesgos y Mitigaciones\*\*





| \*\*Riesgo\*\*                             | \*\*Probabilidad\*\* | \*\*Impacto\*\* | \*\*Mitigación\*\*                                                       |

| -------------------------------------- | ---------------- | ----------- | -------------------------------------------------------------------- |

| \*\*Límite de llamadas a Google Gemini\*\* | Media            | Alto        | Usar clave de API con cuota educativa (gratis).                      |

| \*\*PDFs con formato complejo\*\*          | Alta             | Medio       | Limitar a PDFs con texto seleccionable (no escaneados).              |

| \*\*Errores en la extracción de texto\*\*  | Media            | Medio       | Validar texto extraído antes de enviar a Gemini.                     |

| \*\*Dependencia de APIs externas\*\*       | Baja             | Alto        | Implementar \*fallback\* con análisis local (regex, librerías de NLP). |

| \*\*Problemas de rendimiento\*\*           | Baja             | Medio       | Optimizar llamadas a Gemini (batch processing).                      |





\---



\## 📄 \*\*13. Ejemplo de Informe Generado\*\*



\### \*\*📌 Informe de Análisis para: Germán Andrés Castaño Vásquez\*\*



\#### \*\*🔴 Errores Detectados\*\*





| \*\*Tipo\*\*       | \*\*Texto Original\*\*                         | \*\*Corrección\*\*                   | \*\*Ubicación\*\*                     |

| -------------- | ------------------------------------------ | -------------------------------- | --------------------------------- |

| Ortografía     | "Lideré un equipo de 5 persona"            | "Lideré un equipo de 5 personas" | Sección: Experiencia, Línea 3     |

| Fecha          | "2020 - 2023" (solapado con "2021 - 2022") | "01/2020 - 12/2022"              | Sección: Experiencia, Empresa XYZ |

| Inconsistencia | "Gerente de Ventas" vs "Jefe de Ventas"    | Unificar a "Gerente de Ventas"   | Sección: Experiencia              |





\#### \*\*🟡 Recomendaciones para Logros\*\*





| \*\*Original\*\*                     | \*\*Optimizado\*\*                                                      | \*\*Impacto\*\*             |

| -------------------------------- | ------------------------------------------------------------------- | ----------------------- |

| "Responsable de aumentar ventas" | "Aumenté ventas en un \*\*35%\*\* (de $2M a $2.7M) en 12 meses"         | +$700K en ingresos      |

| "Participé en el proyecto X"     | "Lideré el proyecto X, reduciendo tiempos de entrega en un \*\*20%\*\*" | Ahorro de 500 horas/año |





\#### \*\*🟢 Alineación con JD (Gerente de Ventas en Tech)\*\*



\- \*\*Score de Coincidencia\*\*: \*\*85/100\*\*

\- \*\*Habilidades Coincidentes\*\*: Liderazgo, Ventas, Negociación.

\- \*\*Habilidades Faltantes\*\*:

&#x20; - AWS (Certificación recomendada: \*\*AWS Solutions Architect\*\*).

&#x20; - Kubernetes (Curso: \*\*Kubernetes para DevOps\*\*).



\#### \*\*💡 Sugerencias de Estructura\*\*



1\. Mover la sección \*\*"Educación"\*\* después de \*\*"Experiencia"\*\* (para perfiles senior).

2\. Añadir sección \*\*"Habilidades Técnicas"\*\* con: `AWS, Kubernetes, CRM (Salesforce)`.

3\. Reducir la sección \*\*"Sobre mí"\*\* a 3 líneas máximo.



\---



