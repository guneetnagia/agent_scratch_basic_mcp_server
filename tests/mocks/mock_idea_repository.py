class MockIdeaRepository:

    async def hybrid_search(self, embedding, query, limit, status_filter=None):

        if "chatbot" in query.lower():
            return [
                {
                    "id": 1,
                    "title": "AI chatbot",
                    "vector_score": 0.95,
                    "keyword_score": 0.9
                },
                {
                    "id": 4,
                    "title": "Customer support bot",
                    "vector_score": 0.85,
                    "keyword_score": 0.8
                },
                {
                    "id": 2,
                    "title": "Inventory system",
                    "vector_score": 0.4,
                    "keyword_score": 0.3
                }
            ][:limit]

        elif "pricing" in query.lower():
            return [
                {
                    "id": 3,
                    "title": "Pricing engine",
                    "vector_score": 0.93,
                    "keyword_score": 0.88
                },
                {
                    "id": 5,
                    "title": "Dynamic pricing AI",
                    "vector_score": 0.9,
                    "keyword_score": 0.85
                },
                {
                    "id": 1,
                    "title": "AI chatbot",
                    "vector_score": 0.3,
                    "keyword_score": 0.2
                }
            ][:limit]

        else:
            return [
                {
                    "id": 2,
                    "title": "Inventory system",
                    "vector_score": 0.8,
                    "keyword_score": 0.7
                },
                {
                    "id": 1,
                    "title": "AI chatbot",
                    "vector_score": 0.5,
                    "keyword_score": 0.4
                }
            ][:limit]

    async def keyword_search(self, query, limit):
        return [
            {"id": 1, "title": "AI chatbot"},
            {"id": 2, "title": "Inventory system"},
        ][:limit]

    async def semantic_search(self, embedding, limit):
        return [
            {"id": 1, "title": "AI chatbot", "similarity": 0.92},
            {"id": 2, "title": "Inventory system", "similarity": 0.65},
            {"id": 3, "title": "Pricing engine", "similarity": 0.55},
        ][:limit]