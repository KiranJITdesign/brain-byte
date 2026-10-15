# EcoWatt Twin

A full-stack campus energy digital twin featuring a 3D campus view, energy analytics, a FastAPI service, and webcam-based YOLO people detection.

## Manual setup

Use two terminals from this directory.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

### Frontend

```powershell
cd frontend
npm ci
npm run dev
```

Open <http://localhost:5173/>. The frontend Vite proxy targets the backend at `http://127.0.0.1:8001` by default. Override it with `VITE_BACKEND_URL` if needed. API docs are at <http://localhost:8001/docs>.

The CCTV tab uses the browser webcam after permission is granted. YOLO downloads its `yolov8n.pt` weights on first detection. Set `GEMINI_API_KEY` in `backend/.env` to enable Gemini responses; the rest of the demo works without it.
