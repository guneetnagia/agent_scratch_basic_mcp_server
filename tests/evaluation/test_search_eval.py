import json
import pytest
from src.services.search_service import SearchService
from tests.evaluation.metrics import precision_at_k, recall_at_k, mrr

from src.repositories.idea_repository import IdeaRepository
from src.infrastructure.embedding_client import EmbeddingClient
from tests.mocks.mock_embedding_client import MockEmbeddingClient
from tests.mocks.mock_idea_repository import MockIdeaRepository

@pytest.mark.asyncio
async def test_search_quality():

    repo = MockIdeaRepository()
    embedding = MockEmbeddingClient()

    service = SearchService(repo, embedding)

    with open("tests/evaluation/data/search_eval_dataset.json") as f:
        dataset = json.load(f)

    precisions = []
    recalls = []
    mrr_scores = []

    for case in dataset:
        query = case["query"]
        relevant_ids = case["relevant_ids"]

        result = await service.search(case["query"], "hybrid", 5)
        results = result["results"]

        precisions.append(precision_at_k(results, relevant_ids, k=5))
        recalls.append(recall_at_k(results, relevant_ids, k=5))
        mrr_scores.append(mrr(results, relevant_ids))

    avg_precision = sum(precisions) / len(precisions)
    avg_recall = sum(recalls) / len(recalls)
    avg_mrr = sum(mrr_scores) / len(mrr_scores)

    print("\n=== SEARCH EVAL ===")
    print(f"Precision@5: {avg_precision:.3f}")
    print(f"Recall@5: {avg_recall:.3f}")
    print(f"MRR: {avg_mrr:.3f}")

    # Basic quality gate
    assert avg_precision > 0.3
    assert "results" in result