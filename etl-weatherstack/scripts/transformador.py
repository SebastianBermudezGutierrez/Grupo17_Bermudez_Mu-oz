import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

INPUT_CSV = "data/clima.csv"
OUTPUT_CSV = "data/clima_limpio.csv"

def transformar():
    df = pd.read_csv(INPUT_CSV)

    if df.empty:
        logger.error("❌ CSV vacío, no hay datos para transformar")
        return

    # Limpieza básica
    df = df.dropna()
    df.columns = df.columns.str.lower()

    df.to_csv(OUTPUT_CSV, index=False)
    logger.info("✅ Datos transformados y guardados")

if __name__ == "__main__":
    transformar()