import numpy as np
from ai_engine.rag.embedder import generate_embeddings
from ai_engine.rag.vector_store import load_index_and_chunks
import logging

logger = logging.getLogger(__name__)

def retrieve_context(job_id: str, query: str, top_k: int = 3):
    """
    Natively polls FAISS L2 indexing explicitly searching optimized string representations 
    bounding extreme latency speeds effectively natively.
    """
    try:
        index, chunks = load_index_and_chunks(job_id)
        
        # Format Query into Math
        query_embedding = generate_embeddings([query]).astype('float32')
        
        # Calculate Natively across memory
        distances, indices = index.search(query_embedding, top_k)
        
        relevant_chunks = []
        for idx in indices[0]:
            if idx != -1 and idx < len(chunks):
                relevant_chunks.append(chunks[idx])
                
        return relevant_chunks
    except Exception as e:
        logger.error(f"Retriever crashed completely protecting upstream layers natively: {e}")
        return []
