# -*- coding: utf-8 -*-
"""
ConviveData · DataJam Bogotá 2026
Pruebas estadísticas con datos puros de VIF, lesiones personales y consumo abusivo de SPA.

Este script está preparado para ejecutarse desde el repositorio, desde Google Colab o desde un entorno local.
Busca primero los archivos en data/raw/. Si no los encuentra, intenta descargarlos desde GitHub Raw.
"""

from __future__ import annotations

import unicodedata
import urllib.request
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats

# =============================
# Configuración general
# =============================

REPO_RAW = "https://raw.githubusercontent.com/00Jake00/convivedata-vif-bogota-2018-2025-Datajam/main"

ANIO_INICIO = 2018
ANIO_FIN = 2025
YEARS = list(range(ANIO_INICIO, ANIO_FIN + 1))
ANIOS_ANALISIS = len(YEARS)

BOGOTA_LOCS = [
    "USAQUEN", "CHAPINERO", "SANTA FE", "SAN CRISTOBAL", "USME",
    "TUNJUELITO", "BOSA", "KENNEDY", "FONTIBON", "ENGATIVA",
    "SUBA", "BARRIOS UNIDOS", "TEUSAQUILLO", "LOS MARTIRES",
    "ANTONIO NARINO", "PUENTE ARANDA", "LA CANDELARIA",
    "RAFAEL URIBE URIBE", "CIUDAD BOLIVAR", "SUMAPAZ",
]

# Denominadores usados en el visor validado.
# Las fuentes crudas no traen población, por eso se fija esta tabla de referencia.
POP_REF = {
    "BOSA": 673077,
    "CIUDAD BOLIVAR": 707569,
    "SAN CRISTOBAL": 404697,
    "LOS MARTIRES": 99119,
    "USME": 457302,
    "SANTA FE": 110048,
    "LA CANDELARIA": 24088,
    "KENNEDY": 1088443,
    "RAFAEL URIBE URIBE": 374246,
    "TUNJUELITO": 199430,
    "CHAPINERO": 139701,
    "PUENTE ARANDA": 258287,
    "FONTIBON": 394648,
    "SUBA": 1218513,
    "TEUSAQUILLO": 153025,
    "ENGATIVA": 887080,
    "SUMAPAZ": 6531,
    "ANTONIO NARINO": 109176,
    "USAQUEN": 501999,
    "BARRIOS UNIDOS": 243465,
}

ARCHIVOS = {
    "vif": "violencia_intrafamiliar.csv",
    "lesiones": "lesiones_personales.csv",
    "spa": "consumo_abusivo_spa.xlsx",
}


def encontrar_raiz_proyecto() -> Path:
    """Encuentra la raíz del proyecto buscando data/, README.md o .git."""
    actual = Path.cwd().resolve()
    for carpeta in [actual, *actual.parents]:
        if (carpeta / "data").exists() or (carpeta / "README.md").exists() or (carpeta / ".git").exists():
            return carpeta
    return actual


BASE_DIR = encontrar_raiz_proyecto()
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs_limpieza"

for carpeta in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR]:
    carpeta.mkdir(parents=True, exist_ok=True)


def obtener_archivo(nombre: str) -> Path:
    """Usa el archivo local; si no existe, lo descarga desde GitHub Raw."""
    filename = ARCHIVOS[nombre]
    local_path = RAW_DIR / filename
    url = f"{REPO_RAW}/data/raw/{filename}"

    if not local_path.exists():
        print(f"Descargando {filename} desde GitHub Raw...")
        urllib.request.urlretrieve(url, local_path)

    return local_path


def norm_text(value) -> str:
    """Normaliza textos de localidad: mayúsculas, sin tildes y con alias."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    s = str(value).strip().upper()
    s = " ".join(s.split())
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

    aliases = {
        "MARTIRES": "LOS MARTIRES",
        "LOS MARTIRES": "LOS MARTIRES",
        "CANDELARIA": "LA CANDELARIA",
        "LA CANDELARIA": "LA CANDELARIA",
        "RAFAEL URIBE": "RAFAEL URIBE URIBE",
        "RAFAEL URIBE URIBE": "RAFAEL URIBE URIBE",
        "CIUDAD BOLIVAR": "CIUDAD BOLIVAR",
        "SAN CRISTOBAL": "SAN CRISTOBAL",
        "ANTONIO NARINO": "ANTONIO NARINO",
        "USAQUEN": "USAQUEN",
        "ENGATIVA": "ENGATIVA",
        "FONTIBON": "FONTIBON",
    }
    return aliases.get(s, s)


def leer_csv_seguro(path: Path, sep: str = ";") -> pd.DataFrame:
    """Lee CSV probando codificaciones comunes."""
    for encoding in ["utf-8-sig", "utf-8", "latin1", "cp1252"]:
        try:
            return pd.read_csv(path, sep=sep, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"No se pudo leer el archivo con codificaciones comunes: {path}")


def preparar_vif_lesiones(path: Path, nombre_fuente: str) -> pd.DataFrame:
    df = leer_csv_seguro(path, sep=";")
    df = df.copy()
    df["localidad_norm"] = df["LOCALIDAD"].apply(norm_text)
    df["anio"] = pd.to_numeric(df["ANIO"], errors="coerce").astype("Int64")
    df["cantidad"] = pd.to_numeric(df["CANTIDAD"], errors="coerce").fillna(0)
    df["fuente"] = nombre_fuente
    df = df[df["anio"].isin(YEARS)]
    df = df[df["localidad_norm"].isin(BOGOTA_LOCS)]
    return df


def preparar_spa(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df = df.copy()
    df["localidad_norm"] = df["NOMBRELOCALIDADRESIDENCIA"].apply(norm_text)
    df["anio"] = pd.to_numeric(df["ANO"], errors="coerce").astype("Int64")
    df["cantidad"] = pd.to_numeric(df["CASOS"], errors="coerce").fillna(0)
    df["fuente"] = "spa"
    df = df[df["anio"].isin(YEARS)]
    df = df[df["localidad_norm"].isin(BOGOTA_LOCS)]
    return df


def agregar_localidad_anio(df: pd.DataFrame, nombre_columna: str) -> pd.DataFrame:
    return (
        df.groupby(["localidad_norm", "anio"], as_index=False)["cantidad"]
        .sum()
        .rename(columns={"cantidad": nombre_columna})
    )


def construir_bases(df_vif: pd.DataFrame, df_lesiones: pd.DataFrame, df_spa: pd.DataFrame):
    base_index = pd.MultiIndex.from_product([BOGOTA_LOCS, YEARS], names=["localidad_norm", "anio"]).to_frame(index=False)

    vif_agg = agregar_localidad_anio(df_vif, "vif_casos")
    lesiones_agg = agregar_localidad_anio(df_lesiones, "lesiones_casos")
    spa_agg = agregar_localidad_anio(df_spa, "spa_casos")

    base_anio = (
        base_index
        .merge(vif_agg, on=["localidad_norm", "anio"], how="left")
        .merge(lesiones_agg, on=["localidad_norm", "anio"], how="left")
        .merge(spa_agg, on=["localidad_norm", "anio"], how="left")
        .fillna(0)
    )

    base_anio["poblacion_ref"] = base_anio["localidad_norm"].map(POP_REF)
    base_anio["vif_tasa"] = base_anio["vif_casos"] / base_anio["poblacion_ref"] * 100_000
    base_anio["lesiones_tasa"] = base_anio["lesiones_casos"] / base_anio["poblacion_ref"] * 100_000
    base_anio["spa_tasa"] = base_anio["spa_casos"] / base_anio["poblacion_ref"] * 100_000
    base_anio = base_anio.rename(columns={"localidad_norm": "localidad"})

    base_loc = (
        base_anio.groupby("localidad", as_index=False)[["vif_casos", "lesiones_casos", "spa_casos"]]
        .sum()
    )
    base_loc["poblacion_ref"] = base_loc["localidad"].map(POP_REF)
    base_loc["vif_tasa"] = base_loc["vif_casos"] / ANIOS_ANALISIS / base_loc["poblacion_ref"] * 100_000
    base_loc["lesiones_tasa"] = base_loc["lesiones_casos"] / ANIOS_ANALISIS / base_loc["poblacion_ref"] * 100_000
    base_loc["spa_tasa"] = base_loc["spa_casos"] / ANIOS_ANALISIS / base_loc["poblacion_ref"] * 100_000

    return base_loc, base_anio


def correlation_summary(df: pd.DataFrame, x_col: str, y_col: str) -> dict:
    x = df[x_col].astype(float).values
    y = df[y_col].astype(float).values
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    kendall = stats.kendalltau(x, y)
    return {
        "n": len(df),
        "pearson_r": pearson.statistic,
        "pearson_p": pearson.pvalue,
        "spearman_rho": spearman.statistic,
        "spearman_p": spearman.pvalue,
        "kendall_tau": kendall.statistic,
        "kendall_p": kendall.pvalue,
    }


def generar_pruebas(base_loc: pd.DataFrame, base_anio: pd.DataFrame) -> pd.DataFrame:
    comparisons = [
        ("VIF casos vs lesiones casos", "vif_casos", "lesiones_casos"),
        ("VIF casos vs SPA casos", "vif_casos", "spa_casos"),
        ("Lesiones casos vs SPA casos", "lesiones_casos", "spa_casos"),
        ("VIF tasa vs lesiones tasa", "vif_tasa", "lesiones_tasa"),
        ("VIF tasa vs SPA tasa", "vif_tasa", "spa_tasa"),
        ("Lesiones tasa vs SPA tasa", "lesiones_tasa", "spa_tasa"),
    ]

    rows = []
    for nivel, data, nota in [
        ("localidad_total_2018_2025", base_loc, "20 localidades, agregadas 2018-2025"),
        ("localidad_anio_2018_2025", base_anio, "160 observaciones localidad-año"),
    ]:
        for label, x_col, y_col in comparisons:
            res = correlation_summary(data, x_col, y_col)
            rows.append({"nivel": nivel, "relacion": label, **res, "nota": nota})

    excluidas = {"LOS MARTIRES", "SANTA FE", "LA CANDELARIA"}
    filtrada = base_loc[~base_loc["localidad"].isin(excluidas)].copy()
    for label, x_col, y_col in [
        ("VIF tasa vs lesiones tasa", "vif_tasa", "lesiones_tasa"),
        ("VIF tasa vs SPA tasa", "vif_tasa", "spa_tasa"),
    ]:
        res = correlation_summary(filtrada, x_col, y_col)
        rows.append({
            "nivel": "sin_los_martires_santa_fe_la_candelaria",
            "relacion": label,
            **res,
            "nota": "Sensibilidad excluyendo localidades centrales con población pequeña/flotante",
        })

    return pd.DataFrame(rows)


def generar_spearman_por_anio(base_anio: pd.DataFrame) -> pd.DataFrame:
    comparisons = [
        ("VIF casos vs lesiones casos", "vif_casos", "lesiones_casos"),
        ("VIF casos vs SPA casos", "vif_casos", "spa_casos"),
        ("Lesiones casos vs SPA casos", "lesiones_casos", "spa_casos"),
        ("VIF tasa vs lesiones tasa", "vif_tasa", "lesiones_tasa"),
        ("VIF tasa vs SPA tasa", "vif_tasa", "spa_tasa"),
        ("Lesiones tasa vs SPA tasa", "lesiones_tasa", "spa_tasa"),
    ]
    rows = []
    for year in YEARS:
        data_y = base_anio[base_anio["anio"] == year]
        for label, x_col, y_col in comparisons:
            res = stats.spearmanr(data_y[x_col], data_y[y_col])
            rows.append({
                "anio": year,
                "relacion": label,
                "n": len(data_y),
                "spearman_rho": res.statistic,
                "p_valor": res.pvalue,
            })
    return pd.DataFrame(rows)


def exportar(df: pd.DataFrame, nombre: str):
    for carpeta in [PROCESSED_DIR, OUTPUT_DIR]:
        df.to_csv(carpeta / nombre, index=False, encoding="utf-8-sig")


def main():
    print("BASE_DIR:", BASE_DIR)
    print("RAW_DIR:", RAW_DIR)
    print("OUTPUT_DIR:", OUTPUT_DIR)

    vif_path = obtener_archivo("vif")
    lesiones_path = obtener_archivo("lesiones")
    spa_path = obtener_archivo("spa")

    df_vif = preparar_vif_lesiones(vif_path, "vif")
    df_lesiones = preparar_vif_lesiones(lesiones_path, "lesiones")
    df_spa = preparar_spa(spa_path)

    resumen_fuentes = pd.DataFrame([
        {"fuente": "VIF", "filas_filtradas": len(df_vif), "total_2018_2025_20_localidades": df_vif["cantidad"].sum()},
        {"fuente": "Lesiones personales", "filas_filtradas": len(df_lesiones), "total_2018_2025_20_localidades": df_lesiones["cantidad"].sum()},
        {"fuente": "Consumo abusivo SPA", "filas_filtradas": len(df_spa), "total_2018_2025_20_localidades": df_spa["cantidad"].sum()},
    ])

    base_loc, base_anio = construir_bases(df_vif, df_lesiones, df_spa)
    resultados = generar_pruebas(base_loc, base_anio)
    spearman_anio = generar_spearman_por_anio(base_anio)

    exportar(resumen_fuentes, "resumen_fuentes.csv")
    exportar(base_loc, "base_resumen_localidad_2018_2025.csv")
    exportar(base_anio, "base_localidad_anio_2018_2025.csv")
    exportar(resultados, "resultados_pruebas_estadisticas.csv")
    exportar(spearman_anio, "spearman_por_anio.csv")

    print("\n=== Validación rápida ===")
    print(resumen_fuentes.to_string(index=False))

    print("\n=== Resultados clave ===")
    clave = resultados[
        (resultados["nivel"] == "localidad_total_2018_2025")
        & (resultados["relacion"].isin(["VIF tasa vs lesiones tasa", "VIF tasa vs SPA tasa", "VIF casos vs lesiones casos"]))
    ][["relacion", "n", "pearson_r", "spearman_rho", "spearman_p"]]
    print(clave.to_string(index=False))

    print("\nArchivos exportados en:")
    print("-", PROCESSED_DIR.resolve())
    print("-", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()
