# ConviveData · VIF Bogotá 2018-2025 · DataJam 2026

Repositorio del equipo **ConviveData** para Bogotá DataJam 2026.

Este proyecto analiza patrones territoriales de **violencia intrafamiliar (VIF)** en Bogotá durante el periodo **2018-2025**, integrando datos de VIF, lesiones personales y consumo abusivo de sustancias psicoactivas (SPA). El objetivo es apoyar la priorización territorial y explorar asociaciones estadísticas entre señales de convivencia, salud mental y seguridad.

> El análisis es exploratorio. No pretende establecer causalidad.

## Integrantes

- Luisa Fernanda Carbonell García
- Jeison Orlando Rodríguez Bohórquez
- Erika Julieth Samboni Hernández

Entidad: Secretaría Distrital de Seguridad, Convivencia y Justicia.

## Pregunta de análisis

¿En qué localidades de Bogotá coincide un índice VIF alto con un índice de contexto territorial alto (lesiones personales y consumo abusivo de SPA), y qué patrones de priorización territorial e interinstitucional se derivan de esa coincidencia durante el periodo 2018-2025?

El repositorio también incluye una capa territorial agregada por localidad y año para revisar coincidencias entre VIF, lesiones personales y consumo abusivo de SPA.

## Estructura del repositorio

```text
.
├── README.md
├── requirements.txt
├── index.html
├── data/
│   ├── raw/
│   │   ├── violencia_intrafamiliar.csv
│   │   ├── lesiones_personales.csv
│   │   └── consumo_abusivo_spa.xlsx
│   └── processed/
│       ├── base_resumen_localidad_2018_2025.csv
│       ├── base_localidad_anio_2018_2025.csv
│       ├── resultados_pruebas_estadisticas.csv
│       ├── resumen_fuentes.csv
│       └── spearman_por_anio.csv
├── notebooks/
│   ├── 00_ejecutar_pruebas_desde_github_colab.ipynb
│   ├── datajam_vif_notebook_documentado_final_EJECUTADO.ipynb
│   └── datajam_vif_2018_2025_notebook_reproducible_EJECUTADO.ipynb
├── scripts/
│   └── pruebas_estadisticas_datos_puros_datajam.py
├── dashboard/
│   └── index.html
├── docs/
│   └── formulario_caracterizacion_formulacion_problema.docx
└── outputs_limpieza/
```

## Cómo ejecutar el análisis

### Opción 1: Google Colab

Abrir el notebook:

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/00Jake00/convivedata-vif-bogota-2018-2025-Datajam/blob/main/notebooks/00_ejecutar_pruebas_desde_github_colab.ipynb)

Este notebook descarga el script desde GitHub Raw y ejecuta el análisis con las fuentes alojadas en `data/raw/`.

### Opción 2: ejecución local

```bash
git clone https://github.com/00Jake00/convivedata-vif-bogota-2018-2025-Datajam.git
cd convivedata-vif-bogota-2018-2025-Datajam
pip install -r requirements.txt
python scripts/pruebas_estadisticas_datos_puros_datajam.py
```

Los resultados se exportan en:

```text
data/processed/
outputs_limpieza/
```

## Fuentes utilizadas

1. Violencia intrafamiliar y de género en Bogotá D.C.
2. Lesiones personales / lesiones de causa externa.
3. Consumo abusivo o problemático de sustancias psicoactivas.

La integración entre fuentes se realiza a nivel territorial mediante **año** y **localidad**. No se cruzan registros individuales entre bases diferentes.

## Principales productos

- Base agregada por localidad para el periodo 2018-2025.
- Base localidad-año para pruebas exploratorias.
- Correlaciones Pearson, Spearman y Kendall.
- Prueba de sensibilidad excluyendo localidades centrales con posible efecto de población pequeña o flotante.
- Visualización territorial en HTML.
- Formulario de caracterización y formulación del problema.

## Nota metodológica

Las correlaciones entre VIF, lesiones personales y consumo abusivo de SPA se interpretan como asociaciones territoriales exploratorias. Una correlación significativa no implica causalidad. Los resultados deben leerse junto con conocimiento territorial, calidad de registro, subregistro posible y dinámicas urbanas particulares.
