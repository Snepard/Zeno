# AI Guruji - Production Ecosystem Setup

This document serves as the comprehensive architectural guide for initializing, securing, and deploying the AI Guruji Machine Learning ecosystem combining strict RAG structures, parallel Audio/Video rendering, and asynchronous Backend APIs with a reactive Front-End.

---

## 🛠 Prerequisites

Ensure your host machine or deployment container possesses the following architectures available globally:
- **Python 3.10+** (System architecture dependency)
- **Node.js 18+ & npm** (For UI bootstrapping)
- **Docker & Docker Compose** (Primary PostgreSQL/Redis routing orchestrators)
- **FFmpeg** (Required for localized native `.mp4` and `.mp3` multiplexing securely on `$PATH`)
- Optional: NVIDIA CUDA Toolkit (Required only if executing HW-Accelerated Local Rendering natively utilizing `h264_nvenc` and `Wav2Lip`).

---

## 🔐 1. Environment Configurations

Before booting the system natively, you must duplicate and configure your local environments.

### Backend `.env`
Navigate inside the `/backend` folder. Copy the `.env.example` file securely to `.env`:
```bash
cd backend
cp .env.example .env
```
Ensure you provide real instances within your `.env`:
```env
# Database Hooks
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aiguruji
REDIS_URL=redis://localhost:6379/0

# ML Native Connectors
GROQ_API_KEY=your_groq_production_key
GROQ_MODEL=llama-3.3-70b-versatile
```

### Frontend `.env`
You can dynamically configure UI endpoints identically natively inside your `/frontend` directory via `.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 🚄 2. Infrastructure Initialization (Databases & Brokers)

The backend relies heavily on robust internal messaging structures via **Redis** (for Celery sequences) and **PostgreSQL** (for Job states & Authentication tracking).

Initialize these architectures natively traversing Docker configurations:
```bash
# If using the global docker-compose layout natively:
docker-compose up -d redis db
```
*(If you are running the entire backend via docker-compose rather than local dev, simply run `docker-compose up -d` completely natively bypassing manual startup sequences).*

---

## 🐍 3. Backend Generation Engine

Boot up the central Intelligence Nervous System executing native parallel python environments.

### Install Packages:
```bash
cd backend
pip install -r requirements.txt
```
*(Note for Windows: If `faiss-cpu` or native `TTS` strictly fails due to local PyTorch execution limits, you can gracefully omit `TTS` and the architecture will naturally fallback automatically onto `gTTS`)*.

### Migrate the Database:
Ensure Postgres schemas are formally mapped executing Alembic structures seamlessly:
```bash
alembic upgrade head
```

### Run APIs & Daemons:
You heavily require TWO independent local execution processes mapping cleanly across terminal windows!

**Terminal A (FastAPI Router):**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal B (Celery HW Native Render Worker):**
Windows natively maps threaded pool limits directly onto celery execution. Run Celery mapping natively avoiding standard bounds:
```bash
cd backend
celery -A workers.celery_app worker --loglevel=info --pool=solo
```

---

## ⚛️ 4. Frontend Launch Sequence

Map the Vite React Interface securely onto your local development environments decoupling logic cleanly natively. 

```bash
cd frontend
npm install
npm run dev
```

The application strictly locks local development bounds directly onto `http://localhost:5173`. Open the URL and begin executing Native ML generation securely!

---

## 🚀 5. Architecture Notes & Performance Boundaries

- **GPU Allocations:** Your Celery architecture securely limits intense renders (Video Processing & LipSync ML logic) dynamically onto `route: "gpu"`. If you are orchestrating globally natively across AWS/GCP, ensure hardware nodes intercept the gpu celery queues specifically protecting CPU-only servers.
- **Async FFmpeg Integration:** Make 100% sure `ffmpeg` is securely mapped directly into your system-wide variables. The backend does not implement FFMPEG via API, it natively calls CLI commands structurally mapping extremely low-latency limits natively.
