@echo off
echo.
echo ========================================
echo   SPILLOVER ANALYZER v2.0 - INICIANDO
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado.
    echo Ejecuta primero: python -m venv venv
    echo Luego: pip install -r requirements.txt
    pause
    exit /b 1
)

echo 1. Activando entorno virtual...
call venv\Scripts\activate.bat

echo 2. Verificando Streamlit...
python -c "import streamlit; print('✅ Streamlit disponible')" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit no esta instalado.
    echo Ejecutando: pip install streamlit
    pip install streamlit
)

echo 3. Iniciando aplicacion Streamlit...
echo.
echo 🚀 Aplicacion disponible en: 
echo    http://localhost:8501
echo.
echo 📖 Para detener la aplicacion: Ctrl+C
echo ========================================
echo.

streamlit run app.py

echo.
echo ========================================
echo   APLICACION CERRADA
echo ========================================
pause