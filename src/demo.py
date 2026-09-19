"""一条命令演示摄取、混合检索、风险判定与指标计算。"""

from pathlib import Path

from src.evaluation import mean_reciprocal_rank, recall_at_k
from src.permissions import PermissionPolicy
from src.rag import HybridRetriever
from src.tools import DraftNoteTool


def main() -> None:
    docs = Path(__file__).parents[1] / "examples" / "docs"
    retriever = HybridRetriever.from_directory(docs)
    query = "如何进行 RAG 检索回归测试？"
    hits = retriever.retrieve(query)
    print(f"问题：{query}")
    for index, hit in enumerate(hits, 1):
        print(f"{index}. {hit.source}  score={hit.score:.3f}")
    sources = [hit.source for hit in hits]
    relevant = {"evaluation.md"}
    print(f"Recall@3={recall_at_k(sources, relevant, 3):.2f}  MRR={mean_reciprocal_rank(sources, relevant):.2f}")
    tool = DraftNoteTool(Path("/tmp/jarvis-demo-output"))
    print(f"工具 {tool.spec.name}：{PermissionPolicy().decide(tool.risk)}；{tool.preview(title='检索结论', content='示例内容')}")


if __name__ == "__main__":
    main()

