import pytest
from src.infrastructure.embedding_client import EmbeddingClient


@pytest.mark.asyncio
async def test_embedding():
    client = EmbeddingClient()
    emb = await client.embed("AI chatbot")

    assert isinstance(emb, list)
    assert len(emb) > 0