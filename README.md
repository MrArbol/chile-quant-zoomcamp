# 🇨🇱 Chile Quant Dashboard

Dashboard interactivo para el análisis cuantitativo y técnico de activos del mercado bursátil chileno (IPSA), desarrollado con **Streamlit**, **yfinance** y **Plotly**.

## 🚀 Características
- **Ingesta de Datos:** Descarga histórica directa desde Yahoo Finance para activos locales (`SQM-B.SN`, `BSANTANDER.SN`, `CENCOSUD.SN`, `CHILE.SN`).
- **Análisis Técnico Modular:**
  - Medias Móviles Simples: **SMA 20** y **SMA 50**.
  - Índice de Fuerza Relativa: **RSI 14** con niveles clave de sobrecompra (70) y sobreventa (30).
- **Visualización Interactiva:** Gráficos responsivos de dos paneles con soporte de zoom y tooltips mediante Plotly.

## 📁 Estructura del Proyecto
```text
chile-quant-zoomcamp/
├── data/                  # Datos históricos descargados
├── src/
│   ├── ingestion.py       # Módulo para descarga y obtención de datos
│   └── indicators.py      # Módulo para cálculo de indicadores técnicos
├── app.py                 # Aplicación principal en Streamlit
├── requirements.txt       # Librerías necesarias del proyecto
├── .gitignore             # Archivos excluidos del control de versiones
└── README.md              # Documentación del proyecto
```

## 🛠️ Instalación y Uso

### 1. Clonar el repositorio y entrar al directorio
```bash
git clone https://github.com/<TU_USUARIO>/chile-quant-zoomcamp.git
cd chile-quant-zoomcamp
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Dashboard
```bash
streamlit run app.py
```
