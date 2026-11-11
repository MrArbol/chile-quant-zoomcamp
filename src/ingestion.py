# Módulo de ingesta de datos financieros
import pandas as pd
import yfinance as yf

def fetch_chilean_stock_data(ticker="SQM-B.SN", start_date="2024-01-01"):
    """
    Descarga datos históricos de activos de la Bolsa de Santiago desde Yahoo Finance.
    """
    print(f"Descargando datos para: {ticker} desde {start_date}...")
    df = yf.download(ticker, start=start_date, threads=False)
    
    # Manejo de compatibilidad con versiones recientes de yfinance (MultiIndex)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    if 'Close' in df.columns:
        df['Close'] = pd.to_numeric(df['Close'])
        
    return df

def compute_technical_indicators(ticker="SQM-B.SN", start_date="2024-01-01"):
    """
    Función de prueba para descargar y calcular indicadores en consola.
    """
    df = fetch_chilean_stock_data(ticker=ticker, start_date=start_date)

    # 1. Medias Móviles Simples (SMA 20 y 50)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # 2. RSI (14 periodos)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    print(df[['Close', 'SMA_20', 'SMA_50', 'RSI_14']].tail(10))
    
    output_filename = f"data/{ticker.replace('.SN', '')}_indicators.csv"
    df.to_csv(output_filename)
    print(f"Datos con indicadores guardados en {output_filename}")
    
    return df

if __name__ == "__main__":
    compute_technical_indicators("SQM-B.SN")
