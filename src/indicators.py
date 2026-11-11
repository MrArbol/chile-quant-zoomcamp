import pandas as pd

def calculate_sma(df, window=20):
    """Calcula la Media Móvil Simple (SMA) para una ventana dada."""
    return df['Close'].rolling(window=window).mean()

def calculate_rsi(df, window=14):
    """Calcula el Índice de Fuerza Relativa (RSI)."""
    delta = df['Close'].diff()
    
    # Separar ganancias y pérdidas
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    # Promedios móviles de ganancias y pérdidas
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # Cálculo de RS y RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_all_indicators(df):
    """Aplica todos los indicadores técnicos estándar al DataFrame."""
    # Asegurar que la columna Close sea numérica y exista
    df = df.copy()
    if 'Close' in df.columns:
        df['Close'] = pd.to_numeric(df['Close'])
        
        # Calcular indicadores
        df['SMA_20'] = calculate_sma(df, 20)
        df['SMA_50'] = calculate_sma(df, 50)
        df['RSI_14'] = calculate_rsi(df, 14)
        
    return df