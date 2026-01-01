@echo off
echo Starting English Learning Web App...

:: Start Backend in a new window
echo Starting Python Backend (FastAPI)...
start "Backend" cmd /k "cd backend && python main.py"

:: Start Frontend in a new window
echo Starting React Frontend (Vite)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================
echo Backend running at: http://localhost:8000
echo Frontend running at: http://localhost:5173
echo ======================================================
echo.
pause
