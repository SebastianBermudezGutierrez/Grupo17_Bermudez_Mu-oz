import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Monitor de Divisas", page_icon="💱", layout="wide")

st.title("💱 Monitor de Tasas de Cambio")
st.markdown("Datos en tiempo real desde PostgreSQL")

def conectar():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'divisas_db'),
        user=os.getenv('DB_USER', 'etl_user'),
        password=os.getenv('DB_PASSWORD', 'etl1234')
    )

@st.cache_data(ttl=60)
def cargar_datos():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM tasas_cambio ORDER BY fecha_extraccion DESC", conn)
    conn.close()
    return df

df = cargar_datos()

# Métricas principales
st.subheader("Tasas actuales (1 USD = X moneda)")
cols = st.columns(4)
for i, row in df.iterrows():
    cols[i % 4].metric(
        label=row['moneda_destino'],
        value=f"{row['tasa_cambio']:.4f}",
        delta=f"Inversa: {row['inversa']:.6f}"
    )

# Gráficas
st.subheader("Visualización")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.bar(df['moneda_destino'], df['tasa_cambio'], color='#4ecdc4')
    ax.set_title('1 USD = X moneda')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.bar(df['moneda_destino'], df['inversa'], color='#ff6b6b')
    ax.set_title('Valor en USD de cada moneda')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Tabla completa
st.subheader("Datos completos")
st.dataframe(df, use_container_width=True)
