#!/usr/bin/env bash
set -e
echo "=========================================================="
echo "  EcoWatt Twin - 5-Floor 3D Digital Twin VS Code Launcher"
echo "=========================================================="

(cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8001) &
(cd frontend && npm install && npm run dev) &
wait
