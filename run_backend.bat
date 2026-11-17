@echo off
title CIREMS Backend Service
echo ========================================================
echo Starting CIREMS Python FastAPI Backend Server...
echo API Docs will be available at: http://127.0.0.1:8000/docs
echo ========================================================
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
