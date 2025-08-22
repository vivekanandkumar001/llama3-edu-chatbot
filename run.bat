@echo off
REM ===============================
REM EduBot Startup Script (Windows)
REM ===============================

echo [1/3] Activating virtual environment...
call venv\Scripts\activate

echo [2/3] Running data ingestion...
python -m app.ingest

echo [3/3] Starting server...
uvicorn app.server:app --host 127.0.0.1 --port 8000 --reload

pause
