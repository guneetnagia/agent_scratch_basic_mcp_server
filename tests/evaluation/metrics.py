def precision_at_k(results, relevant_ids, k=5):
    retrieved_ids = [r["id"] for r in results[:k]]
    relevant_set = set(relevant_ids)

    hits = sum(1 for r in retrieved_ids if r in relevant_set)

    return hits / k


def recall_at_k(results, relevant_ids, k=5):
    retrieved_ids = [r["id"] for r in results[:k]]
    relevant_set = set(relevant_ids)

    hits = sum(1 for r in retrieved_ids if r in relevant_set)

    return hits / len(relevant_set)


def mrr(results, relevant_ids):
    for i, r in enumerate(results):
        if r["id"] in relevant_ids:
            return 1 / (i + 1)
    return 0