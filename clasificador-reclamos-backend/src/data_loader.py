import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DATA_PATH, TARGET, MIN_CATEGORY_COUNT

EXPECTED_COLUMNS = [
    "ID_EXP", "FECHA_INGRESO", "FECHA_FIN", "FECHA DE CIERRE", "PROVEEDOR",
    "SECTOR", "TIPO_RECLAMACION", "MOTIVO_RECLAMACION", "COSTO BIEN SERVICIO",
    "MONTO RECLAMADO", "MONTO RECUPERADO", "PROCEDIMIENTO", "BIEN O SERV",
    "MEDIO INGRESO", "TIPO PROD", "MODALIDAD COMPRA", "MODALIDAD PAGO", "PROB ESPECIAL",
]


def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    validate_columns(df)
    return df


def validate_columns(df: pd.DataFrame) -> None:
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en el dataset: {missing}")


def eda_report(df: pd.DataFrame) -> None:
    print(f"\n{'='*60}")
    print(f"  REPORTE EDA BASICO")
    print(f"{'='*60}")
    print(f"\nTotal de registros: {len(df)}")

    print(f"\nDistribucion de '{TARGET}':")
    counts = df[TARGET].value_counts()
    for cat, count in counts.items():
        pct = count / len(df) * 100
        print(f"  {cat}: {count} ({pct:.1f}%)")

    print(f"\nPorcentaje de valores nulos por columna:")
    null_pct = df.isnull().mean() * 100
    for col, pct in null_pct.items():
        if pct > 0:
            print(f"  {col}: {pct:.2f}%")
    if null_pct.sum() == 0:
        print("  (sin valores nulos)")

    low_count = counts[counts < MIN_CATEGORY_COUNT]
    if len(low_count) > 0:
        print(f"\nCategorias con menos de {MIN_CATEGORY_COUNT} registros:")
        for cat, count in low_count.items():
            print(f"  {cat}: {count}")
    else:
        print(f"\nTodas las categorias tienen >= {MIN_CATEGORY_COUNT} registros.")


def filter_low_count_categories(df: pd.DataFrame, min_count: int = MIN_CATEGORY_COUNT) -> pd.DataFrame:
    counts = df[TARGET].value_counts()
    low_cats = counts[counts < min_count].index.tolist()
    if low_cats:
        print(f"\nAgrupando {len(low_cats)} categorias con < {min_count} registros bajo 'Otros':")
        for cat in low_cats:
            print(f"  - {cat} ({counts[cat]} registros)")
        df[TARGET] = df[TARGET].apply(lambda x: "Otros" if x in low_cats else x)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dupes = df.duplicated(subset=["ID_EXP"], keep="first").sum()
    if dupes > 0:
        print(f"\nEliminando {dupes} registros duplicados por ID_EXP.")
        df = df.drop_duplicates(subset=["ID_EXP"], keep="first").reset_index(drop=True)
    else:
        print("\nSin registros duplicados por ID_EXP.")
    return df


def load_and_prepare(filepath: str = DATA_PATH) -> pd.DataFrame:
    df = load_data(filepath)
    eda_report(df)
    df = remove_duplicates(df)
    df = filter_low_count_categories(df)
    print(f"\nDataset final: {len(df)} registros, {df[TARGET].nunique()} categorias.")
    return df


if __name__ == "__main__":
    df = load_and_prepare()
