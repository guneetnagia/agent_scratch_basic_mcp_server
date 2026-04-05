"""
Embedding Client

Handles text → vector conversion using Sentence Transformers.
Designed to be async-friendly and production-ready.
"""

import asyncio
from typing import List, Union
from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    # -------------------------
    # Single text embedding
    # -------------------------
    async def embed(self, text: str) -> List[float]:
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            None,
            self.model.encode,
            text
        )
        return embedding.tolist()

    # -------------------------
    # Batch embedding (IMPORTANT)
    # -------------------------
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            self.model.encode,
            texts
        )
        return [e.tolist() for e in embeddings]