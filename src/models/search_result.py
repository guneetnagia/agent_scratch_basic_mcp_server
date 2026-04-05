from typing import TypedDict


class SearchResult(TypedDict):
    id: int
    title: str
    vector_score: float
    keyword_score: float