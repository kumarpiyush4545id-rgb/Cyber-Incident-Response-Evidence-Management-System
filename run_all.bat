@echo off
title Launch CIREMS System
echo ========================================================
echo Launching CIREMS (Backend + Frontend)
echo ========================================================

start "CIREMS Backend (Port 8000)" cmd /k "run_backend.bat"
timeout /t 2 /nobreak >nul
start "CIREMS Frontend (Port 5173)" cmd /k "run_frontend.bat"

echo.
echo Both services are starting!
echo Backend Docs: http://127.0.0.1:8000/docs
echo Frontend App: http://localhost:5173
echo.
pause
