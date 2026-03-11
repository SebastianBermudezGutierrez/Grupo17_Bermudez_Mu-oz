#!/usr/bin/env python3
import os
import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DivisasExtractor:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = os.getenv('BASE_URL')
        self.moneda_base = os.getenv('MONEDA_BASE', 'USD')
        self.monedas_objetivo = os.getenv('MONEDAS_OBJETIVO', '').split(',')

        if not self.api_key:
            raise ValueError("API_KEY no configurada en .env")

    def extraer_tasas(self):
        """Extrae todas las tasas desde la moneda base"""
        try:
            url = f"{self.base_url}/{self.api_key}/latest/{self.moneda_base}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('result') != 'success':
                logger.error(f"❌ Error en API: {data.get('error-type', 'desconocido')}")
                return None

            logger.info(f"✅ Tasas extraídas para base {self.moneda_base}")
            return data

        except Exception as e:
            logger.error(f"❌ Error en extracción: {str(e)}")
            return None

    def procesar_respuesta(self, data):
        """
        Convierte el JSON de la API a una lista de registros estructurados.
        Filtra solo las monedas que nos interesan.
        """
        try:
            tasas = data.get('conversion_rates', {})
            fecha_actualizacion = data.get('time_last_update_utc', '')
            proxima_actualizacion = data.get('time_next_update_utc', '')

            registros = []

            for moneda in self.monedas_objetivo:
                moneda = moneda.strip()
                if moneda in tasas:
                    registros.append({
                        'moneda_base': self.moneda_base,
                        'moneda_destino': moneda,
                        'tasa_cambio': tasas[moneda],
                        'fecha_actualizacion_api': fecha_actualizacion,
                        'proxima_actualizacion_api': proxima_actualizacion,
                        'fecha_extraccion': datetime.now().isoformat(),
                        # Dato calculado útil para análisis
                        'inversa': round(1 / tasas[moneda], 6) if tasas[moneda] != 0 else None
                    })
                else:
                    logger.warning(f"⚠️ Moneda {moneda} no encontrada en respuesta")

            logger.info(f"📊 {len(registros)} registros procesados")
            return registros

        except Exception as e:
            logger.error(f"Error procesando respuesta: {str(e)}")
            return []

    def ejecutar_extraccion(self):
        """Orquesta todo el proceso ETL de extracción"""
        logger.info("=" * 50)
        logger.info("INICIANDO EXTRACCIÓN DE TASAS DE CAMBIO")
        logger.info("=" * 50)

        # EXTRACT
        raw_data = self.extraer_tasas()
        if not raw_data:
            logger.error("Extracción fallida. Abortando.")
            return None

        # TRANSFORM
        registros = self.procesar_respuesta(raw_data)
        if not registros:
            logger.error("Transformación sin resultados. Abortando.")
            return None

        # LOAD - archivos locales
        self._guardar_json(raw_data, registros)
        df = self._guardar_csv(registros)

        self._mostrar_resumen(df)
        return df

    def _guardar_json(self, raw_data, registros_procesados):
        """Guarda tanto el raw como el procesado en JSON"""
        # Raw completo (útil para auditoría)
        with open('data/divisas_raw.json', 'w') as f:
            json.dump(raw_data, f, indent=2)

        # Procesado (solo monedas de interés)
        with open('data/divisas_procesado.json', 'w') as f:
            json.dump(registros_procesados, f, indent=2)

        logger.info("📁 JSON guardados en data/")

    def _guardar_csv(self, registros):
        """Guarda los datos en CSV y retorna el DataFrame"""
        df = pd.DataFrame(registros)

        # CSV principal (sobreescribe con última extracción)
        df.to_csv('data/divisas.csv', index=False)

        # CSV histórico (acumula todas las ejecuciones)
        historico_path = 'data/divisas_historico.csv'
        if os.path.exists(historico_path):
            df.to_csv(historico_path, mode='a', header=False, index=False)
        else:
            df.to_csv(historico_path, index=False)

        logger.info("📁 CSV guardados en data/")
        return df

    def _mostrar_resumen(self, df):
        """Imprime tabla resumen en consola"""
        print("\n" + "=" * 60)
        print("RESUMEN DE TASAS DE CAMBIO")
        print("=" * 60)
        print(df[['moneda_base', 'moneda_destino', 'tasa_cambio', 'inversa']].to_string(index=False))
        print("=" * 60)
        print(f"Extracción: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        extractor = DivisasExtractor()
        extractor.ejecutar_extraccion()
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}")