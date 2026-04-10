from fastapi import FastAPI

from orchestrator.routes import router as pipeline_router

app = FastAPI(title="Zeno AI Engine", version="1.0.0")


@app.get("/health")
async def health():
    return {"ok": True}


app.include_router(pipeline_router)
