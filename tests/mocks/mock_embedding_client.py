class MockEmbeddingClient:
    async def embed(self, text: str):
        return [0.1] * 384  # fake embedding