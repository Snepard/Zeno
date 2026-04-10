from sentence_transformers import SentenceTransformer
import torch
import logging

logger = logging.getLogger(__name__)

# Delaying ML initialization sequentially preventing FastAPI deadlocks on startup purely caching globally
EMBEDDING_MODEL = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def get_embedder() -> SentenceTransformer:
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None:
        logger.info(f"Initializing SentenceTransformers Base Model ('all-MiniLM-L6-v2') natively scaling '{device.upper()}' ...")
        EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    return EMBEDDING_MODEL

def generate_embeddings(texts: list[str]):
    """Returns vector float arrays spanning absolute text context natively."""
    model = get_embedder()
    return model.encode(texts, convert_to_numpy=True)
