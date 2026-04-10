from pathlib import Path
from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, storage_dir: str) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, chunks: List[str]) -> np.ndarray:
        vectors = self.model.encode(chunks, normalize_embeddings=True)
        return np.array(vectors, dtype=np.float32)

    def save_index(self, name: str, chunks: List[str]) -> str:
        vectors = self.embed(chunks)
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)

        index_path = self.storage_dir / f"{name}.faiss"
        faiss.write_index(index, str(index_path))

        text_path = self.storage_dir / f"{name}.txt"
        text_path.write_text("\n".join(chunks), encoding="utf-8")

        return str(index_path)
