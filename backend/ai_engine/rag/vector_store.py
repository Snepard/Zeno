import faiss
import numpy as np
import pickle
import logging
from storage.local_storage import ensure_job_directory

logger = logging.getLogger(__name__)

def stringify_chunk(chunk) -> str:
    """Formats agnostic dict/string chunks perfectly protecting Vector Embeddings from bad parsing"""
    if isinstance(chunk, dict):
        return chunk.get("text", str(chunk))
    return str(chunk)

def build_and_save_index(job_id: str, chunks: list):
    """
    Core vector creation pipeline natively executed background indexing asynchronously 
    immediately following structure parsing dynamically.
    """
    logger.info(f"Synthesizing RAG FAISS Index actively targeting Job {job_id}")
    job_dir = ensure_job_directory(job_id)
    faiss_path = job_dir / "faiss.index"
    chunks_path = job_dir / "embeddings.pkl"
    
    if not chunks:
        logger.warning(f"Aborting RAG index (empty chunks) for {job_id}")
        return
        
    from ai_engine.rag.embedder import generate_embeddings
    
    # 1. Transform raw parsed dicts/strings into vector math
    text_arrays = [stringify_chunk(c) for c in chunks]
    embeddings = generate_embeddings(text_arrays).astype('float32')
    
    # 2. Build explicit FlatL2 FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # 3. Store mapped index perfectly
    faiss.write_index(index, str(faiss_path))
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)
        
    logger.info(f"RAG Index saved flawlessly on memory drive via local execution.")

def load_index_and_chunks(job_id: str):
    """Safely retrieves Vector stores independently linked natively bypassing slow queries"""
    job_dir = ensure_job_directory(job_id)
    faiss_path = job_dir / "faiss.index"
    chunks_path = job_dir / "embeddings.pkl"
    
    if not faiss_path.exists() or not chunks_path.exists():
        raise FileNotFoundError(f"FAISS mapping not natively tracked covering Job {job_id}")
        
    index = faiss.read_index(str(faiss_path))
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks
