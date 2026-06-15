@echo off
echo ==============================================
echo Menjalankan Aplikasi Chatbot RAG PMB Itenas
echo ==============================================

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment tidak ditemukan di folder .venv
    pause
    exit /b
)

start "Backend - FastAPI" cmd /k "call .venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
start "Frontend - Streamlit" cmd /k "call .venv\Scripts\activate.bat && streamlit run eval_ui.py"

echo - FastAPI berjalan di port 8000
echo - Streamlit berjalan di port 8501 (atau port terbuka lainnya)
pause
