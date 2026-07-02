# Dashboard · Visor territorial VIF Bogotá 2018-2025

Esta carpeta contiene la visualización interactiva del proyecto **ConviveData · Violencia intrafamiliar en Bogotá 2018-2025**, desarrollada para Bogotá DataJam 2026.

El tablero permite explorar de forma territorial los patrones de violencia intrafamiliar en Bogotá, integrando indicadores de VIF, lesiones personales y consumo abusivo de sustancias psicoactivas.

🔗 **Visualización publicada:** https://violenciaintrafamiliarbogota.netlify.app/

---

## Contenido de la carpeta

```text
dashboard/
│
├── index.html
└── README.md
```

El archivo principal de la visualización es:

```text
index.html
```

Este archivo contiene la estructura HTML, los estilos CSS, la lógica JavaScript y los datos necesarios para mostrar el visor territorial.

---

## Qué muestra el tablero

La visualización presenta una lectura territorial de la violencia intrafamiliar en Bogotá para el periodo 2018-2025.

Incluye:

* Indicadores generales de violencia intrafamiliar.
* Ranking de localidades según carga de casos.
* Comparación entre carga absoluta e intensidad relativa.
* Índice territorial de VIF.
* Índice de contexto asociado a lesiones personales y consumo abusivo de SPA.
* Brecha entre VIF y contexto territorial.
* Ficha interactiva por localidad.
* Recomendaciones de lectura para apoyar la priorización territorial.

---

## Objetivo del tablero

El objetivo del visor es facilitar la lectura territorial del fenómeno y apoyar la identificación de localidades que requieren una revisión prioritaria.

El tablero no busca establecer causalidad entre violencia intrafamiliar, lesiones personales y consumo abusivo de SPA. Su propósito es presentar patrones descriptivos y asociaciones territoriales exploratorias que orienten preguntas de análisis y posibles decisiones de focalización.

---

## Cómo visualizarlo localmente

Para abrir el tablero de forma local:

1. Descargar o clonar el repositorio.
2. Entrar a la carpeta `dashboard/`.
3. Abrir el archivo `index.html` en un navegador web.

También puede abrirse directamente desde la versión publicada en Netlify:

[Ver tablero interactivo](https://violenciaintrafamiliarbogota.netlify.app/)

---

## Publicación

La visualización fue publicada en Netlify para facilitar su consulta sin necesidad de instalar software adicional.

URL pública:

```text
https://violenciaintrafamiliarbogota.netlify.app/
```

---

## Relación con el proyecto principal

Este tablero es uno de los productos del proyecto ConviveData. El procesamiento de datos, las pruebas estadísticas exploratorias, las bases procesadas y el notebook reproducible se encuentran en las demás carpetas del repositorio principal.

Repositorio del proyecto:

https://github.com/00Jake00/convivedata-vif-bogota-2018-2025-Datajam

---

## Nota metodológica

La visualización se basa en datos agregados por localidad para el periodo 2018-2025. Los resultados deben interpretarse como una herramienta de exploración y priorización territorial, no como una prueba causal.

Las localidades con poblaciones pequeñas o con alta población flotante, como Los Mártires, Santa Fe y La Candelaria, requieren una lectura cuidadosa de sus tasas e indicadores.
