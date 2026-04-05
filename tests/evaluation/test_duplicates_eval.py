import pytest

from src.services.duplicate_service import DuplicateService
from tests.mocks.mock_idea_repository import MockIdeaRepository
from tests.mocks.mock_embedding_client import MockEmbeddingClient

@pytest.mark.asyncio
async def test_duplicate_detection():

    repo = MockIdeaRepository()
    embedding = MockEmbeddingClient()

    service = DuplicateService(repo, embedding)

    result = await service.detect(
        "AI chatbot",
        "AI chatbot for support",
        threshold=0.8
    )

    assert result is not None