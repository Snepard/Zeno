# Zeno AI Learning Platform

Production-oriented microservices scaffold for converting PDFs into:

- AI lecture slides with narration
- AI podcast in dual-speaker format
- RAG flashcards

## Architecture

Three-layer service split with strict separation of concerns:

- `frontend/`: React + Tailwind UI only
- `backend/`: Auth, API routing, job creation, status APIs
- `ai-engine/`: FastAPI pipelines (LLM/TTS/RAG orchestration)
- `workers/`: Celery workers for async execution and retries
- `queue/`: Redis queue and caching design notes
- `storage/`: Generated assets and vector index persistence
- `shared/`: Cross-service schema/type contracts

System flow:

`Frontend -> Backend -> Redis Queue -> Workers -> AI Engine -> Storage -> Frontend`

## Folder Structure

```text
/project-root
  frontend/
  backend/
    api/
    auth/
    controllers/
    services/
    models/
    config/
  ai-engine/
    pipelines/
      lecture_pipeline/
      podcast_pipeline/
      ppt_pipeline/
      rag_pipeline/
    llm/
    tts/
    embeddings/
    orchestrator/
    utils/
  workers/
    lecture_worker.py
    podcast_worker.py
    ppt_worker.py
  queue/
  storage/
    audio/
    slides/
    lectures/
    vector_store/
  shared/
    schemas/
    types/
```

## Key Design Choices

- Non-blocking APIs: backend writes job metadata + enqueues in Redis, then returns immediately.
- Async processing: workers execute long AI operations through Celery.
- Parallel fan-out:
  - Lecture: per-slide TTS in parallel + PPT in parallel.
  - Podcast: per-turn audio synthesis in parallel.
- Progressive updates: workers update MongoDB status as `partial` before final completion.
- Caching:
  - AI engine caches lecture slides, podcast dialogue, and flashcards in Redis.
  - Embedding module supports FAISS index persistence under `storage/vector_store/`.
- Fallback-ready modules:
  - LLM fallback client in `ai-engine/llm/fallback_client.py`
  - TTS fallback chain in `ai-engine/tts/fallback_tts.py`

## API Endpoints

Auth:

- `POST /api/auth/register`
- `POST /api/auth/login`

Protected jobs:

- `POST /api/upload-pdf`
- `POST /api/generate-lecture`
- `GET /api/lecture/:id`
- `POST /api/generate-podcast`
- `POST /api/generate-flashcards`

All generation APIs return:

- `job_id`
- `status` (`pending`, `partial`, `complete`)

## Local Setup

### 1) Prerequisites

- Node.js 20+
- Python 3.11+
- Docker + Docker Compose (recommended)

### 2) Environment

```bash
cp .env.example .env
```

Set real secrets for production usage (`JWT_SECRET`, API keys).

### 3) Run with Docker Compose

```bash
docker compose up --build
```

Services:

- Backend: `http://localhost:4000`
- AI Engine: `http://localhost:8000`
- Frontend: run locally from `frontend/` (or add it to compose)

### 4) Frontend (local)

```bash
cd frontend
npm install
npm run dev
```

### 5) Backend (local)

```bash
cd backend
npm install
npm run dev
```

### 6) AI Engine (local)

```bash
cd ai-engine
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 7) Workers (local)

```bash
cd workers
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
celery -A celery_app.celery_app worker -l info -Q lecture,podcast,ppt,flashcards
python dispatcher.py
```

Run worker and dispatcher in separate terminals in local development.

## Example Request Flow

### Lecture generation (non-blocking)

1. Frontend calls `POST /api/generate-lecture` with `pdf_url` and title.
2. Backend creates Mongo job record (`pending`) and pushes to Redis `jobs:lecture`.
3. Dispatcher pops queue message and sends Celery task to `lecture_worker.process_lecture_job`.
4. Worker calls AI engine to generate slides and writes `partial` output immediately.
5. Worker fans out slide-level TTS tasks in parallel and triggers PPT generation in parallel.
6. Completion markers are merged and final status becomes `complete`.
7. Frontend polls `GET /api/lecture/:id` and progressively renders slides/audio.

### Podcast generation (streaming style)

1. Backend enqueues podcast job and returns `job_id` immediately.
2. Worker requests dialogue from AI engine and stores it as `partial`.
3. Worker fans out per-turn TTS tasks in parallel.
4. Frontend can start with dialogue instantly and progressively load turn audio URLs.

## Production Hardening Checklist

- Replace local storage with S3-compatible bucket + signed URLs.
- Add structured logs and distributed tracing (OpenTelemetry).
- Add idempotency keys for generation endpoints.
- Add per-user rate limits and abuse protection.
- Introduce API gateway and service-level mTLS.
- Add CI checks, tests, and container scanning.
- Tune Redis and Celery worker concurrency per pipeline type.

## Notes

This scaffold is intentionally modular and ready for provider-specific integrations.
AI logic is isolated from backend; backend remains a fast orchestration API.
