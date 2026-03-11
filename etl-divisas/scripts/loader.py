#!/usr/bin/env python3
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DivisasLoader:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'divisas_db'),
            user=os.getenv('DB_USER', 'etl_user'),
            password=os.getenv('DB_PASSWORD', 'etl1234')
        )
        logger.info("Conexion a PostgreSQL exitosa")

    def cargar_datos(self, csv_path='data/divisas.csv'):
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"{len(df)} registros leidos desde {csv_path}")

            registros = [
                (
                    row['moneda_base'],
                    row['moneda_destino'],
                    row['tasa_cambio'],
                    row['inversa'],
                    row['fecha_actualizacion_api'],
                    row['fecha_extraccion']
                )
                for _, row in df.iterrows()
            ]

            cursor = self.conn.cursor()
            execute_values(cursor, """
                INSERT INTO tasas_cambio 
                (moneda_base, moneda_destino, tasa_cambio, inversa,
                 fecha_actualizacion_api, fecha_extraccion)
                VALUES %s
            """, registros)

            self.conn.commit()
            cursor.close()
            logger.info(f"{len(registros)} registros insertados en PostgreSQL")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error cargando datos: {str(e)}")
            raise

    def cerrar(self):
        self.conn.close()
        logger.info("Conexion cerrada")

if __name__ == "__main__":
    loader = DivisasLoader()
    loader.cargar_datos()
    loader.cerrar()
