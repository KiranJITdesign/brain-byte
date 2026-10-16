# EcoWatt Twin

A full-stack campus energy digital twin featuring a 3D campus view, energy analytics, a FastAPI service, and webcam-based YOLO people detection.

## Manual setup

Use three terminals from this directory.

### Mail service

The mail service uses Express and Nodemailer, and reads the SMTP credentials from `backend/.env` so the Gmail App Password is stored only once.

```powershell
cd mail-service
npm install
npm start
```

It listens only on `127.0.0.1:8025` and accepts authenticated requests from the FastAPI backend. Keep it running while using email delivery.

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

### Approval email demo

Create a Gmail App Password while signed into the Gmail account configured in `MAIL_USER` (Google requires 2-Step Verification). It must be created for that same account; a password from another Gmail account will fail with `535 5.7.8`. Use an App Password, never the normal account password. See [Google's App Password help](https://support.google.com/mail/answer/185833).

Copy `backend/.env.example` to `backend/.env` and set `MAIL_PASS` to the 16-character App Password without spaces. Replace `MAIL_SERVICE_TOKEN` with a long random value; both services read it from this same file. The sender, Gmail host, port 465, mail service URL, and localhost approval URL are prefilled. Keep `.env` private. Set `EMPTY_SECONDS=20` for a quick demo; approval links expire after 30 minutes and rejection cooldowns also default to 30 minutes.

Restart the mail service and backend after editing `.env`:

```powershell
cd .kilo/sustaniable-energy/mail-service
npm start
```

```powershell
cd .kilo/sustaniable-energy/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

From another terminal, run the frontend:

```powershell
cd .kilo/sustaniable-energy/frontend
npm install
npm run dev
```

Open <http://localhost:5173/> and use **Admin Settings** to add, disable, or remove up to four admins. Click **Send test email**; `/api/email/test` returns Nodemailer SMTP error details if Gmail rejects authentication or disconnects. Add the intended admin addresses there. FastAPI forwards each message to the local Express mail service, which uses Nodemailer. The service logs whether SMTP settings are present but never prints the App Password.

For a direct one-off message, the local `POST http://127.0.0.1:8025/send` endpoint accepts a Bearer token and JSON fields `to`, `subject`, and `text` or `html`. Use the `MAIL_SERVICE_TOKEN` from `backend/.env`; the endpoint is bound to loopback and is intended for local use.

To demo without a camera, select a room and click **Simulate 0 people**. This creates the same expiring approval request and emails active admins. For the live flow, select a room under **CCTV & YOLOv8 Vision**, allow webcam access, and leave the camera running until the configured empty interval passes. A GET on an email link only opens a confirmation page; the admin must press the confirmation button. The first decision wins. Approval switches eligible room fixtures off, the twin syncs by polling, and a follow-up email is queued. CCTV, electrical panels, and server equipment are excluded.

Approval status and history are visible in **Admin Settings**. For admins approving from phones, `PUBLIC_BASE_URL=http://localhost:8001` is insufficient: localhost links work only on the same computer. Use the backend's reachable LAN IP, ngrok, or cloudflared URL and make sure the backend port is accessible. The frontend API uses port 8001 by default; see `frontend/vite.config.js` if you change it.
