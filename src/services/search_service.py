from src.repositories.idea_repository import IdeaRepository
from src.infrastructure.embedding_client import EmbeddingClient
from src.models.search_result import SearchResult
from typing import Dict, List, Any

class SearchService:
    def __init__(self, repo: IdeaRepository, embedding_client: EmbeddingClient):
        self.repo = repo
        self.embedding_client = embedding_client

    async def search(self, query: str, search_type: str, limit: int, status_filter=None):
        embedding = await self.embedding_client.embed(query)

        if search_type == "semantic":
            results = await self.repo.semantic_search(embedding, limit)

        elif search_type == "keyword":
            results = await self.repo.keyword_search(query, limit)

        else:  # hybrid (default)
            results = await self.repo.hybrid_search(
                embedding=embedding,
                query=query,
                limit=limit,
                status_filter=status_filter
            )

            results = self._diversify(results)

        return {
            "results": results,
            "count": len(results),
            "search_type": search_type,
            "debug": {
                "weights": {
                    "vector": 0.6,
                    "keyword": 0.3,
                    "recency": 0.1
                }
            }
        }
    
    from typing import List, Dict, Any
from src.models.search_result import SearchResult


class SearchService:

    def __init__(self, repo, embedding_client):
        self.repo = repo
        self.embedding_client = embedding_client

    async def search(
        self,
        query: str,
        search_type: str = "hybrid",
        limit: int = 10,
        status_filter: str | None = None,
    ) -> Dict[str, Any]:

        # 1. Generate embedding
        embedding = await self.embedding_client.embed(query)

        # 2. Fetch results
        if search_type == "semantic":
            results: List[SearchResult] = await self.repo.semantic_search(
                embedding, limit
            )

        elif search_type == "keyword":
            results: List[SearchResult] = await self.repo.keyword_search(
                query, limit
            )

        else:  # hybrid
            results: List[SearchResult] = await self.repo.hybrid_search(
                embedding, query, limit, status_filter
            )

        if not results:
            return {"results": [], "count": 0}

        # 3. Normalize scores
        results = self._normalize_scores(results)

        # 4. Combine scores (hybrid ranking)
        for r in results:
            r["final_score"] = (
                0.7 * r.get("vector_score", 0)
                + 0.3 * r.get("keyword_score", 0)
            )

        # 5. Sort by final score
        results.sort(key=lambda x: x.get("final_score", 0), reverse=True)

        # 6. Diversify results
        results = self._diversify(results)

        # 7. Limit results
        results = results[:limit]

        return {
            "results": results,
            "count": len(results),
        }

    # -------------------------
    # Helpers
    # -------------------------

    def _normalize_scores(self, results: List[SearchResult]) -> List[SearchResult]:
        max_vector = max((r.get("vector_score", 0) for r in results), default=1)
        max_keyword = max((r.get("keyword_score", 0) for r in results), default=1)

        for r in results:
            r["vector_score"] = r.get("vector_score", 0) / max_vector if max_vector else 0
            r["keyword_score"] = r.get("keyword_score", 0) / max_keyword if max_keyword else 0

        return results

    def _diversify(self, results: List[SearchResult]) -> List[SearchResult]:
        selected = []

        for r in results:
            if not any(
                abs(r.get("vector_score", 0) - s.get("vector_score", 0)) < 0.01
                for s in selected
            ):
                selected.append(r)

        return selected