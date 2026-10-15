@echo off
echo ==========================================================
echo   EcoWatt Twin - 5-Floor 3D Digital Twin VS Code Launcher
echo ==========================================================
echo.
echo [1/2] Starting Python FastAPI Backend on port 8001...
start cmd /k "cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8001"

echo [2/2] Starting React + Three.js 3D Frontend on port 5173...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Both servers are launching in separate windows!
echo Frontend: http://localhost:5173
echo Backend Docs: http://localhost:8001/docs
pause
