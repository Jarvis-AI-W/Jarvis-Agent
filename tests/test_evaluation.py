from src.evaluation import mean_reciprocal_rank, recall_at_k


def test_retrieval_metrics_are_deterministic() -> None:
    retrieved, relevant = ["a.md", "evaluation.md"], {"evaluation.md"}
    assert recall_at_k(retrieved, relevant, 2) == 1.0
    assert mean_reciprocal_rank(retrieved, relevant) == 0.5

