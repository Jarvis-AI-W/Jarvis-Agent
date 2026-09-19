"""无需 LLM 裁判、可复现的检索回归指标。"""

from collections.abc import Sequence


def recall_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    if not relevant:
        raise ValueError("relevant 不能为空")
    return len(set(retrieved[:k]) & relevant) / len(relevant)


def mean_reciprocal_rank(retrieved: Sequence[str], relevant: set[str]) -> float:
    for index, source in enumerate(retrieved, start=1):
        if source in relevant:
            return 1 / index
    return 0.0

