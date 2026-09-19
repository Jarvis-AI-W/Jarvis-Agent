from src.rag import HybridRetriever


def test_hybrid_retriever_returns_evaluation_document() -> None:
    retriever = HybridRetriever({"evaluation.md": "Recall@K 和 MRR 用于检索回归测试。", "other.md": "工具权限控制写操作。"})
    assert retriever.retrieve("怎样做检索回归测试", top_k=1)[0].source == "evaluation.md"

