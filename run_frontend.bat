@echo off
title CIREMS Frontend Web App
echo ========================================================
echo Starting CIREMS React Frontend Web Application...
echo URL: http://localhost:5173
echo ========================================================

set "NODE_DIR=C:\Users\anant\AppData\Local\Programs\node-v20\node-v20.18.0-win-x64"
if exist "%NODE_DIR%" (
    set "PATH=%NODE_DIR%;%PATH%"
)

cd frontend
call npm run dev
pause
