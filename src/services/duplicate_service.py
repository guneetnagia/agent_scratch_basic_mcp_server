class DuplicateService:
    def __init__(self, repo, embedding_client):
        self.repo = repo
        self.embedding_client = embedding_client

    async def detect(self, title: str, description: str, threshold: float):
        query = f"{title} {description}"
        embedding = await self.embedding_client.embed(query)

        results = await self.repo.semantic_search(embedding, limit=10)

        duplicates = [
            r for r in results if r["similarity"] >= threshold
        ]

        return {
            "duplicates": duplicates,
            "count": len(duplicates)
        }