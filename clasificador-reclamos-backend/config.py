import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "quejas_limpias.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "models", "metrics.json")

CATEGORICAL_FEATURES = [
    "SECTOR",
    "TIPO_RECLAMACION",
    "PROCEDIMIENTO",
    "BIEN O SERV",
    "MEDIO INGRESO",
    "TIPO PROD",
    "MODALIDAD COMPRA",
    "MODALIDAD PAGO",
    "PROB ESPECIAL",
]

NUMERICAL_FEATURES = [
    "COSTO BIEN SERVICIO",
    "MONTO RECLAMADO",
    "MONTO RECUPERADO",
    "DIAS_RESOLUCION",
]

TARGET = "MOTIVO_RECLAMACION"

EXCLUDE_COLUMNS = ["ID_EXP", "PROVEEDOR", "FECHA_INGRESO", "FECHA_FIN", "FECHA DE CIERRE"]

MIN_CATEGORY_COUNT = 30
TEST_SIZE = 0.2
RANDOM_STATE = 42
