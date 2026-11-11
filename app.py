import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Configuración de la página (debe ser el primer comando de Streamlit)
st.set_page_config(page_title="Chile Quant Dashboard", layout="wide")

# 2. Importar módulos locales de arquitectura modular
from src.ingestion import fetch_chilean_stock_data
from src.indicators import add_all_indicators

st.title("🇨🇱 Chile Quant Dashboard: Análisis Técnico")
st.markdown("Visualización interactiva de precios, medias móviles e indicador RSI con arquitectura modular.")

# --- BARRA LATERAL DE CONTROL ---
st.sidebar.header("Parámetros del Activo")
ticker = st.sidebar.selectbox(
    "Selecciona un activo (IPSA):", 
    ["SQM-B.SN", "BSANTANDER.SN", "CENCOSUD.SN", "CHILE.SN"]
)
start_date = st.sidebar.date_input("Fecha de inicio", value=pd.to_datetime("2024-01-01"))

# --- PIPELINE MODULAR DE CARGA Y PROCESAMIENTO ---
@st.cache_data
def load_data_pipeline(symbol, start):
    # 1. Ingesta desde src/ingestion.py
    df = fetch_chilean_stock_data(ticker=symbol, start_date=str(start))
    
    # 2. Cálculo de indicadores técnicos desde src/indicators.py
    df_enriched = add_all_indicators(df)
    
    return df_enriched

df = load_data_pipeline(ticker, start_date)

# --- VISUALIZACIÓN INTERACTIVA CON PLOTLY ---
if not df.empty and 'Close' in df.columns:
    # Crear figura con 2 filas (Panel 1: Precios y SMA | Panel 2: RSI)
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05, 
        row_heights=[0.7, 0.3],
        subplot_titles=(f"Precio y Medias Móviles ({ticker})", "Índice de Fuerza Relativa (RSI 14)")
    )

    # Panel Superior: Precio de Cierre y Medias Móviles
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Cierre', line=dict(color='royalblue', width=1.5)), row=1, col=1)
    
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange', width=1)), row=1, col=1)
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='crimson', width=1)), row=1, col=1)

    # Panel Inferior: RSI
    if 'RSI_14' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI_14'], name='RSI', line=dict(color='purple', width=1.2)), row=2, col=1)
    
    # Líneas de referencia de sobrecompra (70) y sobreventa (30)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1, annotation_text="Sobrecompra (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1, annotation_text="Sobreventa (30)")

    # Ajustes estéticos del layout
    fig.update_layout(
        height=650,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Renderizar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabla resumen de los últimos datos
    st.subheader("Últimos Registros con Indicadores")
    cols_to_show = [col for col in ['Close', 'SMA_20', 'SMA_50', 'RSI_14'] if col in df.columns]
    st.dataframe(df[cols_to_show].tail(10), use_container_width=True)
else:
    st.warning("No se pudieron cargar los datos históricos para este activo.")
