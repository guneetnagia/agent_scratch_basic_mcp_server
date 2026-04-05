from typing import List
from src.infrastructure.database import get_db
from src.models.search_result import SearchResult


class IdeaRepository:

    async def semantic_search(
        self,
        embedding,
        limit: int,
        status_filter=None
    ) -> List[SearchResult]:

        db = await get_db()

        sql = """
        SELECT 
            id,
            title,
            description,
            1 - (vector_embedding <=> $1) AS vector_score
        FROM ideas
        ORDER BY vector_score DESC
        LIMIT $2
        """

        rows = await db.fetch(sql, embedding, limit)

        return [
            {
                "id": r["id"],
                "title": r["title"],
                "vector_score": r["vector_score"],
                "keyword_score": 0.0,  # ensure contract consistency
            }
            for r in rows
        ]

    async def keyword_search(
        self,
        query: str,
        limit: int
    ) -> List[SearchResult]:

        db = await get_db()

        sql = """
        SELECT 
            id,
            title,
            description,
            ts_rank(
                to_tsvector('english', title || ' ' || description),
                plainto_tsquery('english', $1)
            ) AS keyword_score
        FROM ideas
        ORDER BY keyword_score DESC
        LIMIT $2
        """

        rows = await db.fetch(sql, query, limit)

        return [
            {
                "id": r["id"],
                "title": r["title"],
                "vector_score": 0.0,
                "keyword_score": r["keyword_score"],
            }
            for r in rows
        ]

    async def hybrid_search(
        self,
        embedding,
        query: str,
        limit: int,
        status_filter=None
    ) -> List[SearchResult]:

        db = await get_db()

        sql = """
        SELECT 
            id,
            title,
            description,

            -- vector similarity
            1 - (vector_embedding <=> $1) AS vector_score,

            -- keyword score
            ts_rank(
                to_tsvector('english', title || ' ' || description),
                plainto_tsquery('english', $2)
            ) AS keyword_score

        FROM ideas
        ORDER BY vector_score DESC
        LIMIT $3
        """

        rows = await db.fetch(sql, embedding, query, limit)

        return [
            {
                "id": r["id"],
                "title": r["title"],
                "vector_score": r["vector_score"],
                "keyword_score": r["keyword_score"],
            }
            for r in rows
        ]

    async def get_by_id(self, idea_id: int):
        db = await get_db()

        row = await db.fetchrow(
            "SELECT * FROM ideas WHERE id=$1", idea_id
        )

        return dict(row) if row else None