import pytest

from src.services.search_service import SearchService
from tests.mocks.mock_idea_repository import MockIdeaRepository
from tests.mocks.mock_embedding_client import MockEmbeddingClient

@pytest.mark.asyncio
async def test_hybrid_search_returns_results():

    repo = MockIdeaRepository()
    embedding = MockEmbeddingClient()

    service = SearchService(repo, embedding)

    result = await service.search("AI chatbot", "hybrid", 5)

    assert len(result["results"]) > 0