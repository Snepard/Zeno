# Zeno AI Guruji

A production-grade Python/FastAPI backend system for dynamically converting PDFs into structured AI lectures, podcasts, and long-form Manim-animated educational videos.

## 🚀 Core Features
1. **Long-Form Video Orchestration (Manim)**
   - Generates automated video lectures (10-60+ mins) via `Manim` (Minim rendering).
   - Seamless degradation fallback to `Pillow/MoviePy` if underlying system binaries fail.
2. **Dual-Speaker AI Podcasts**
   - Transcribes entire PDFs into structured dynamic scripts.
   - Leverages `Edge-TTS` and a secondary fallback local CUDA microservice (`Coqui-TTS`).
3. **Advanced LLM Pipeline Cascade**
   - Fully isolated 3-tier fallback engine directly connected to `Groq`.
   - Dedicated isolated API keys for independent quotas (Classroom, Podcast, Video).
4. **Vector Memory RAG Chatbot**
   - Interactive local assistant answering context-specific PDF doubts.

---

## 🏛 Architecture

To resolve fatal C-binding binary conflicts on Windows (`NumPy 2.x` vs `NumPy 1.22`), the architecture employs a pure **Sub-Service Node** structure:

```text
D:\Projects\Zeno\
├── backend\                      # Primary Pipeline Engine
│   ├── api\                      # FastAPI Endpoint Handlers
│   ├── ai_engine\
│   │   ├── video\
│   │   │   ├── minim_renderer.py # Manim Video Generator
│   │   │   └── animation_builder.py # Pillow/MoviePy Fallback
│   │   ├── tts\
│   │   │   └── tts_manager.py    # Sub-service request Router
│   │   └── llm\
│   │       └── groq_client.py    # 3-tier API Cascade Engine
│   ├── storage\                  # Output video, mp3, pdf targets
│   └── workers\
│       ├── runner.py             # Parallel threaded daemon processing
│       └── tasks\                # Discrete worker actions
│
└── backend\tts_service\          # Coqui-TTS Microservice
    ├── main_tts.py               # Local FastAPI inference node
    └── tts_venv\                 # Independent Python Environment
```

---

## 🛠 Installation & Local Setup (Windows)

Because of explicit `NumPy` constraints between the newest version of `Manim` and the older ML logic of `Coqui-TTS`, you **must** use two distinct Virtual Environments.

### 1. Primary Backend setup (`backend\`)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. TTS Microservice setup (`backend\tts_service\`)
```powershell
cd backend\tts_service
python -m venv tts_venv
.\tts_venv\Scripts\activate
pip install -r requirements_tts.txt
```

---

## 📡 Environment Variables

Create `.env` inside `backend/` and supply your **3 separate Groq API keys** to distribute your daily rate-limit quotas:

```env
# Database Hooks
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aiguruji
REDIS_URL=https://rare-dog-80406.upstash.io

# Groq API Nodes
GROQ_API_KEY_CLASS=gsk_YOUR_FIRST_KEY
GROQ_API_KEY_PODCAST=gsk_YOUR_SECOND_KEY
GROQ_API_KEY_VIDEO=gsk_YOUR_THIRD_KEY

# Models
GROQ_MODEL=llama-3.1-8b-instant
GROQ_FALLBACK_MODEL=llama-3.3-70b-versatile
GROQ_FALLBACK_MODEL_2=meta-llama/llama-4-scout-17b-16e-instruct
```

---

## 🚀 Running the System

You must start both the Primary Node and the TTS Sub-Node independently.

**Terminal 1: TTS Inference Engine**
```powershell
cd backend\tts_service
.\tts_venv\Scripts\activate
uvicorn main_tts:app --port 8001
```

**Terminal 2: Core Backend**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
