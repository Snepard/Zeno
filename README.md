# Zeno — AI Guruji

> A production-grade AI educational content engine that converts PDFs into animated video lectures, dual-speaker podcasts, PowerPoint decks, and an interactive RAG chatbot — powered by Groq LLMs, Manim, Edge-TTS, and FAISS.

---

## 🚀 Core Features

| Feature | Description |
|---|---|
| 🎬 **Long-Form Video (Manim)** | Generates fully animated lecture videos (10–60+ mins) with Manim scenes, color-coded equations, and dot-grid backgrounds |
| 🎙️ **Dual-Speaker AI Podcast** | Converts PDFs into structured two-host scripts narrated via Edge-TTS or Coqui-TTS fallback |
| 📊 **PPT Generation** | Produces slide-by-slide presentation scripts with bullet points and keywords via Groq |
| 🤖 **RAG Chatbot** | FAISS vector index over chunked content enables context-aware Q&A on any uploaded PDF |
| 🎭 **Avatar Lip-Sync** | Wav2Lip integration for animated talking-head avatar video |
| 🔐 **JWT Auth** | Stateless auth with bcrypt password hashing and OAuth2 bearer token flow |

---

## 🏛 System Architecture

### High-Level Service Topology

```mermaid
graph TB
    subgraph Client["🌐 Client (React + Vite)"]
        UI["Pages: Home / Generate / Video / Viewer"]
    end

    subgraph Backend["⚙️ FastAPI Backend  :8000"]
        API["API Router\n/api/v1/"]
        AUTH["auth.py\nLogin · Register"]
        GEN["generate.py\nPDF · PPT · Podcast · Video"]
        CHAT["chat.py\nRAG Q&A"]
        JOB["job.py\nStatus Polling"]
    end

    subgraph Workers["🔄 Worker Layer (Threaded Daemons)"]
        RUNNER["runner.py\nJob Dispatcher"]
        PPT_T["ppt_task.py"]
        POD_T["podcast_task.py"]
        VID_T["long_video_task.py"]
        AUD_T["audio_tasks.py"]
        LIP_T["lipsync_task.py"]
    end

    subgraph AIEngine["🧠 AI Engine"]
        LLM["LLM Cascade\nGroq (3-key fallback)"]
        TTS["TTS Manager\nEdge-TTS → Coqui"]
        MANIM["Manim Renderer\n+ Pillow Fallback"]
        RAG["RAG Pipeline\nFAISS + SentenceTransformers"]
        PDF["PDF Parser\nPyMuPDF"]
        AVATAR["Wav2Lip\nLip-Sync Engine"]
    end

    subgraph TTS_SVC["🗣️ TTS Microservice  :8001"]
        COQUI["Coqui-TTS\nLocal CUDA Inference"]
    end

    subgraph Storage["💾 Storage Layer"]
        FILES["JSON Job Store\n+ MP3 / MP4 / PDF"]
        FAISS_IDX["FAISS Index\n+ Chunk Pickle"]
    end

    subgraph DB["🗄️ PostgreSQL + Redis"]
        PG["Users / Jobs\n(SQLAlchemy async)"]
        RDS["Redis Queue\n(Upstash)"]
    end

    UI -- "REST API" --> API
    API --> AUTH & GEN & CHAT & JOB
    GEN --> RUNNER
    RUNNER --> PPT_T & POD_T & VID_T & LIP_T
    PPT_T & POD_T & VID_T --> LLM & TTS & MANIM & RAG & PDF
    LIP_T --> AVATAR
    TTS -- "fallback HTTP" --> TTS_SVC
    TTS_SVC --> COQUI
    RAG --> FAISS_IDX
    LLM & TTS & MANIM --> FILES
    CHAT --> RAG
    Backend --> PG & RDS
```

---

### Request Lifecycle — Long-Form Video Generation

```mermaid
sequenceDiagram
    participant U as React Client
    participant A as FastAPI :8000
    participant W as Worker Thread
    participant L as Groq LLM
    participant T as TTS Manager
    participant M as Manim Renderer
    participant V as Video Merger

    U->>A: POST /api/v1/generate/video {topic, pdf}
    A->>A: create_job() → job_id
    A-->>U: 202 {job_id}
    A->>W: dispatch_long_video_job(job_id)

    note over W: Runs as daemon thread

    W->>L: process_pdf_to_script(pdf, topic)
    L-->>W: script JSON {sections[]}
    W->>W: update_job(progress=25%)

    W->>L: generate_scenes_from_script(sections)
    L-->>W: scenes[] {scene_id, text, equations, visuals}
    W->>W: update_job(progress=40%)

    loop For each scene
        W->>T: generate_audio_manager(text, job_id)
        T-->>W: scene_N.mp3
        W->>W: get_audio_duration(mp3) → actual_secs
        W->>M: render_scene_with_minim(scene, duration)
        M-->>W: scene_N.mp4
    end

    W->>W: build_timeline(scenes)
    W->>V: merge_timeline(timeline) → lecture.mp4
    W->>W: update_job(status=completed, progress=100%)
    U->>A: GET /api/v1/job/{job_id} → {video_url}
```

---

### AI Engine — Internal Module Map

```mermaid
graph LR
    subgraph llm["llm/"]
        GC["groq_client.py\ngenerate_class_completion\ngenerate_video_completion\ngenerate_podcast_completion"]
        JP["json_parser.py"]
        PR["prompts.py\nPPT_SYSTEM_PROMPT\nPODCAST_SYSTEM_PROMPT"]
        GC --> JP
    end

    subgraph pdf["pdf/"]
        PP["pdf_parser.py\nPyMuPDF extract_text"]
    end

    subgraph chunking["chunking/"]
        SC["script_chunker.py\nchunk_ppt_script\nchunk_podcast_script"]
    end

    subgraph rag["rag/"]
        EM["embedder.py\nSentenceTransformer\nall-MiniLM-L6-v2"]
        VS["vector_store.py\nbuild_and_save_index\nload_index_and_chunks\n(FAISS L2)"]
        RT["retriever.py\nretrieve_context(top_k=3)"]
        EM --> VS --> RT
    end

    subgraph context_engine["context_engine/"]
        CB["context_builder.py"]
        PB["prompt_builder.py\nbuild_rag_prompt"]
        RT --> CB --> PB
    end

    subgraph tts["tts/"]
        TM["tts_manager.py\nRoute: Edge → Coqui → gTTS"]
        ET["edge_tts_engine.py"]
        CT["coqui_tts_engine.py\n→ HTTP :8001"]
        GT["gtts_engine.py"]
        TM --> ET & CT & GT
    end

    subgraph video["video/"]
        MR["minim_renderer.py\nManim scenes\nDot-grid BG\nLaTeX equations"]
        AB["animation_builder.py\nPillow fallback\nMoviePy composite"]
        VM["video_merger.py\nconcatenate_videoclips"]
        FF["ffmpeg_utils.py\nmerge_audio_files"]
        LVP["long_video_pipeline.py\nprocess_pdf_to_script"]
        SG["scene_generator.py\ngenerate_scenes_from_script"]
        TL["timeline_manager.py\nbuild_timeline\nget_audio_duration"]
    end

    subgraph pipelines["pipelines/"]
        PPTP["ppt_pipeline.py"]
        PODP["podcast_pipeline.py"]
    end

    GC --> PPTP & PODP & LVP & SG
    PP --> LVP & PPTP
    SC --> PPTP & PODP
    PPTP --> VS
    PB --> GC
```

---

### TTS Routing Logic

```mermaid
flowchart TD
    A["generate_audio_manager(text, job_id, filename)"] --> B{TTS_MODE env}
    B -- edge --> C["edge_tts_engine.py\nasync edge_tts stream"]
    B -- coqui --> D["coqui_tts_engine.py\nHTTP POST :8001/synthesize"]
    B -- gtts --> E["gtts_engine.py\ngTTS → mp3"]
    B -- default --> C

    C -- success --> G["✅ audio/scene_N.mp3"]
    C -- fail --> D
    D -- success --> G
    D -- fail --> E
    E --> G

    subgraph TTS_SVC["TTS Microservice  :8001 (tts_venv)"]
        D2["Coqui TTS\ntts_models/en/ljspeech/tacotron2-DDC\nCUDA inference"]
    end

    D --> D2
```

---

### RAG Pipeline — PDF → Answer

```mermaid
flowchart LR
    PDF["📄 PDF Upload"] --> PARSE["pdf_parser.py\nPyMuPDF → raw text"]
    PARSE --> CHUNK["script_chunker.py\nSplit into chunks[]"]
    CHUNK --> EMBED["embedder.py\nSentenceTransformer\nall-MiniLM-L6-v2\n→ float32 vectors"]
    EMBED --> BUILD["vector_store.py\nfaiss.IndexFlatL2\nbuild_and_save_index()"]
    BUILD --> DISK["💾 storage/{job_id}/\n  faiss.index\n  chunks.pkl"]

    USER["💬 User Question"] --> QEMBED["generate_embeddings(query)"]
    QEMBED --> SEARCH["index.search(query_vec, top_k=3)"]
    DISK --> SEARCH
    SEARCH --> CTX["context_builder.py\nTop-K chunks → context string"]
    CTX --> PROMPT["prompt_builder.py\nbuild_rag_prompt(query, context)"]
    PROMPT --> LLM["Groq LLM\ngenerate_chat_completion"]
    LLM --> ANS["📝 Answer"]
```

---

### LLM Cascade — 3-Key Quota Strategy

```mermaid
flowchart TD
    REQ["LLM Request"] --> K1{"API Key\nGROQ_API_KEY_CLASS\nllama-3.1-8b-instant"}
    K1 -- success --> OUT["✅ Response"]
    K1 -- RateLimitError --> K2{"Fallback Key\nGROQ_API_KEY_PODCAST\nllama-3.3-70b-versatile"}
    K2 -- success --> OUT
    K2 -- RateLimitError --> K3{"Fallback Key 2\nGROQ_API_KEY_VIDEO\nmeta-llama/llama-4-scout-17b-16e"}
    K3 -- success --> OUT
    K3 -- fail --> ERR["❌ Raise Exception"]

    style K1 fill:#4a9eff,color:#fff
    style K2 fill:#f0a500,color:#fff
    style K3 fill:#e05c5c,color:#fff
```

---

## 📁 Project Structure

```text
Zeno/
├── backend/                        # Core FastAPI service (:8000)
│   ├── main.py                     # App factory, CORS, lifespan
│   ├── requirements.txt
│   ├── api/
│   │   ├── router.py               # Aggregates all sub-routers
│   │   ├── deps.py                 # JWT auth dependency
│   │   └── routes/
│   │       ├── auth.py             # POST /login, /register
│   │       ├── generate.py         # POST /ppt, /podcast, /video, /lipsync
│   │       ├── chat.py             # POST /chat (RAG)
│   │       └── job.py              # GET /job/{id}
│   ├── ai_engine/
│   │   ├── llm/                    # Groq client + prompts + JSON parser
│   │   ├── pdf/                    # PyMuPDF text extractor
│   │   ├── chunking/               # Script splitter for RAG/TTS
│   │   ├── rag/                    # FAISS embedder + vector store + retriever
│   │   ├── context_engine/         # Context & prompt builder for chatbot
│   │   ├── tts/                    # Edge-TTS / Coqui / gTTS manager
│   │   ├── video/                  # Manim renderer, scene generator, merger
│   │   ├── pipelines/              # PPT & podcast orchestration pipelines
│   │   ├── chatbot/                # Chat handler
│   │   ├── memory/                 # Per-user memory store
│   │   └── avatar/                 # Wav2Lip lip-sync engine
│   ├── workers/
│   │   ├── runner.py               # Thread dispatcher
│   │   ├── celery_app.py           # Celery config (Redis broker)
│   │   └── tasks/
│   │       ├── ppt_task.py
│   │       ├── podcast_task.py
│   │       ├── long_video_task.py
│   │       ├── audio_tasks.py
│   │       ├── video_task.py
│   │       └── lipsync_task.py
│   ├── auth/                       # bcrypt hash + JWT creation
│   ├── config/                     # Pydantic settings from .env
│   ├── db/                         # SQLAlchemy async engine + job/user stores
│   ├── models/                     # ORM: User, Job (UUID, JSONB)
│   ├── schemas/                    # Pydantic request/response schemas
│   ├── services/                   # auth_service, job_service
│   ├── storage/                    # local_storage.py (save_json, ensure_dir)
│   └── tts_service/                # Coqui-TTS microservice (:8001)
│       ├── main_tts.py             # FastAPI inference endpoint
│       └── requirements_tts.txt
│
└── frontend/                       # React + Vite SPA
    └── src/
        ├── App.jsx                 # Router + global state
        ├── pages/
        │   ├── Home.jsx
        │   ├── Generate.jsx        # Upload PDF + trigger jobs
        │   ├── Video.jsx           # Video player + scene list
        │   └── Viewer.jsx          # PDF viewer + chat panel
        ├── components/             # Shared UI components
        ├── api/                    # Axios client wrappers
        ├── context/                # React context providers
        └── hooks/                  # Custom hooks
```

---

## 🛠 Installation & Local Setup (Windows)

> **Important:** Two separate virtual environments are required due to NumPy binary conflicts between Manim (requires NumPy ≥2.x) and Coqui-TTS (requires NumPy 1.22.x).

### 1. Primary Backend (`backend/`)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. TTS Microservice (`backend/tts_service/`)

```powershell
cd backend\tts_service
python -m venv tts_venv
.\tts_venv\Scripts\activate
pip install -r requirements_tts.txt
```

### 3. Frontend (`frontend/`)

```powershell
cd frontend
npm install
npm run dev
```

---

## 📡 Environment Variables

Create `.env` inside `backend/` with the following:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aiguruji

# Redis (Upstash or local)
REDIS_URL=https://rare-dog-80406.upstash.io

# Groq API Keys — 3 separate keys to distribute daily rate-limit quotas
GROQ_API_KEY_CLASS=gsk_YOUR_FIRST_KEY
GROQ_API_KEY_PODCAST=gsk_YOUR_SECOND_KEY
GROQ_API_KEY_VIDEO=gsk_YOUR_THIRD_KEY

# LLM Models (fallback cascade)
GROQ_MODEL=llama-3.1-8b-instant
GROQ_FALLBACK_MODEL=llama-3.3-70b-versatile
GROQ_FALLBACK_MODEL_2=meta-llama/llama-4-scout-17b-16e-instruct

# TTS Mode: edge | coqui | gtts
TTS_MODE=edge
```

---

## 🚀 Running the System

### Terminal 1 — TTS Microservice

```powershell
cd backend\tts_service
.\tts_venv\Scripts\activate
uvicorn main_tts:app --port 8001
```

### Terminal 2 — Core Backend

```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 3 — React Frontend

```powershell
cd frontend
npm run dev
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **API Framework** | FastAPI + Uvicorn |
| **LLM Provider** | Groq (Llama 3.1 / 3.3 / Llama 4 Scout) |
| **Animation** | Manim Community + MoviePy + Pillow |
| **TTS (Primary)** | Microsoft Edge-TTS (async stream) |
| **TTS (Fallback)** | Coqui-TTS (local CUDA inference) |
| **TTS (Final)** | gTTS (Google) |
| **Vector Search** | FAISS (IndexFlatL2) |
| **Embeddings** | SentenceTransformers `all-MiniLM-L6-v2` |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Database** | PostgreSQL + SQLAlchemy async |
| **Job Queue** | Redis (Upstash) + Celery / Thread daemons |
| **Auth** | JWT (PyJWT) + bcrypt + OAuth2 |
| **Avatar** | Wav2Lip |
| **Frontend** | React 18 + Vite |

---

