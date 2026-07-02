# ConviveData · VIF Bogotá 2018-2025 · DataJam 2026

Repositorio del equipo **ConviveData** para Bogotá DataJam 2026.

Este proyecto analiza patrones territoriales de violencia intrafamiliar (VIF) en Bogotá durante el periodo 2018-2025, integrando datos de VIF, lesiones personales y consumo abusivo de sustancias psicoactivas (SPA). El objetivo es apoyar la priorización territorial y explorar asociaciones estadísticas entre señales de convivencia, salud mental y seguridad.

El análisis es exploratorio y no pretende establecer causalidad.

🔗 **Visualización interactiva:** [Ver tablero en Netlify](https://violenciaintrafamiliarbogota.netlify.app/)

---

## Integrantes

* Luisa Fernanda Carbonell García
* Jeison Orlando Rodríguez Bohórquez
* Erika Julieth Samboni Hernández

**Entidad:** Secretaría Distrital de Seguridad, Convivencia y Justicia.

---

## Pregunta de análisis

¿En qué localidades de Bogotá coincide un índice VIF alto con un índice de contexto territorial alto (lesiones personales y consumo abusivo de SPA), y qué patrones de priorización territorial e interinstitucional se derivan de esa coincidencia durante el periodo 2018-2025?

El análisis se desarrolla a nivel territorial agregado por localidad y año, con el fin de revisar coincidencias entre violencia intrafamiliar, lesiones personales y consumo abusivo de SPA.

---

## Estructura del repositorio

```text
.
├── README.md
├── requirements.txt
├── index.html
│
├── data/
│   ├── raw/
│   │   ├── violencia_intrafamiliar.csv
│   │   ├── lesiones_personales.csv
│   │   └── consumo_abusivo_spa.xlsx
│   │
│   └── processed/
│       ├── base_resumen_localidad_2018_2025.csv
│       ├── base_localidad_anio_2018_2025.csv
│       ├── resultados_pruebas_estadisticas.csv
│       ├── resumen_fuentes.csv
│       └── spearman_por_anio.csv
│
├── notebooks/
│   ├── datajam_vif_01_limpieza_desde_github.ipynb
│   └── datajam_vif_02_ejecucion_desde_github.ipynb
│
├── scripts/
│   └── pruebas_estadisticas_datos_puros_datajam.py
│
├── dashboard/
│   ├── index.html
│   └── README.md
│
├── docs/
│   └── formulario_caracterizacion_formulacion_problema.docx
│
└── outputs_limpieza/
```

El archivo `index.html` de la raíz y el archivo `dashboard/index.html` corresponden a la visualización territorial del proyecto. La versión publicada puede consultarse en Netlify.

---

## Cómo ejecutar el análisis

Los cuadernos están preparados para ejecutarse directamente en Google Colab. No requieren rutas locales ni descarga manual de archivos, ya que los datos se leen desde las carpetas del repositorio en GitHub.

### 1. Limpieza de datos

[![Abrir limpieza en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/00Jake00/convivedata-vif-bogota-2018-2025-Datajam/blob/main/notebooks/datajam_vif_01_limpieza_desde_github.ipynb)

Este cuaderno descarga las fuentes desde GitHub, realiza la limpieza inicial, normaliza los nombres de localidades, filtra el periodo 2018-2025 y genera las bases limpias del proyecto.

### 2. Ejecución del análisis y pruebas estadísticas

[![Abrir ejecución en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/00Jake00/convivedata-vif-bogota-2018-2025-Datajam/blob/main/notebooks/datajam_vif_02_ejecucion_desde_github.ipynb)

Este cuaderno construye las bases consolidadas, calcula indicadores territoriales, genera rankings, estima índices, ejecuta pruebas estadísticas exploratorias y exporta los productos finales del análisis.

---

## Ejecución local

También es posible ejecutar el proyecto localmente.

Clonar el repositorio:

```bash
git clone https://github.com/00Jake00/convivedata-vif-bogota-2018-2025-Datajam.git
cd convivedata-vif-bogota-2018-2025-Datajam
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el script principal:

```bash
python scripts/pruebas_estadisticas_datos_puros_datajam.py
```

Los resultados se exportan en:

```text
data/processed/
outputs_limpieza/
```

---

## Fuentes utilizadas

El proyecto integra tres fuentes principales:

1. **Violencia intrafamiliar y de género en Bogotá D.C.**
2. **Lesiones personales / lesiones de causa externa.**
3. **Consumo abusivo o problemático de sustancias psicoactivas.**

La integración entre fuentes se realiza a nivel territorial mediante **año** y **localidad**. No se cruzan registros individuales entre bases diferentes.

---

## Principales productos

* Base agregada por localidad para el periodo 2018-2025.
* Base localidad-año para pruebas exploratorias.
* Correlaciones Pearson, Spearman y Kendall.
* Prueba de sensibilidad excluyendo localidades centrales con posible efecto de población pequeña o flotante.
* Visualización territorial en HTML.
* Formulario de caracterización y formulación del problema.
* Cuadernos reproducibles para ejecución en Google Colab.
* Script de procesamiento y pruebas estadísticas.

---

## Visualización

La visualización territorial permite explorar los principales patrones de VIF, lesiones personales y consumo abusivo de SPA por localidad.

🔗 [Ver tablero interactivo en Netlify](https://violenciaintrafamiliarbogota.netlify.app/)

El tablero incluye:

* Indicadores generales de VIF.
* Comparación entre carga absoluta e intensidad relativa.
* Índice territorial de VIF.
* Índice de contexto.
* Brecha VIF-contexto.
* Ficha por localidad.
* Recomendaciones de lectura territorial.

---

## Nota metodológica

Las correlaciones entre VIF, lesiones personales y consumo abusivo de SPA se interpretan como asociaciones territoriales exploratorias. Una correlación significativa no implica causalidad.

Los resultados deben leerse junto con conocimiento territorial, calidad de registro, posible subregistro y dinámicas urbanas particulares. Las localidades con población residente baja o alta población flotante, como Los Mártires, Santa Fe y La Candelaria, requieren especial cautela en la interpretación de tasas.

---

## Reproducibilidad

El repositorio está organizado para permitir la revisión y ejecución del análisis desde Google Colab o desde un entorno local.

* Los datos fuente se encuentran en `data/raw/`.
* Los datos procesados se encuentran en `data/processed/`.
* Los cuadernos reproducibles están en `notebooks/`.
* El script principal está en `scripts/`.
* La visualización está en `dashboard/` y publicada en Netlify.
* Las salidas automáticas de limpieza y ejecución se conservan en `outputs_limpieza/`.

---

## Alcance del análisis

Este proyecto permite identificar patrones territoriales y asociaciones estadísticas exploratorias entre violencia intrafamiliar, lesiones personales y consumo abusivo de SPA. Sus resultados pueden apoyar la priorización inicial de localidades y la formulación de preguntas para análisis institucional más detallado.

El análisis no estima efectos causales ni reemplaza la lectura territorial de los equipos técnicos e institucionales.

