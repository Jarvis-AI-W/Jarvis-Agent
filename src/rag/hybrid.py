"""轻量、可复现的 Hybrid RAG：词项召回 + 字符 n-gram 召回 + 融合重排。"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import sqrt
import re
from pathlib import Path

_WORDS = re.compile(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]+")


def tokenize(text: str) -> list[str]:
    """中英文兼容的最小切词：英文按词，中文保留词串并补充双字切片。"""
    result: list[str] = []
    for part in _WORDS.findall(text.lower()):
        result.append(part)
        if any("\u4e00" <= char <= "\u9fff" for char in part):
            result.extend(part[index:index + 2] for index in range(len(part) - 1))
    return result


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    text: str
    score: float


class HybridRetriever:
    """无外部服务的演示检索器；生产系统可替换为向量库和 cross-encoder。"""

    def __init__(self, documents: dict[str, str]) -> None:
        self._documents = documents
        self._terms = {name: Counter(tokenize(text)) for name, text in documents.items()}
        self._doc_freq = Counter(term for terms in self._terms.values() for term in terms)

    @classmethod
    def from_directory(cls, directory: str | Path) -> "HybridRetriever":
        root = Path(directory)
        docs = {path.name: path.read_text(encoding="utf-8") for path in sorted(root.glob("*.md"))}
        if not docs:
            raise ValueError(f"没有在 {root} 找到 Markdown 示例资料")
        return cls(docs)

    def retrieve(self, query: str, *, top_k: int = 3) -> list[RetrievedChunk]:
        query_terms = Counter(tokenize(query))
        if not query_terms:
            return []
        lexical = {name: self._cosine(query_terms, terms) for name, terms in self._terms.items()}
        # 稀有词更有区分力；这是与向量相似度并列的第二个、可解释的信号。
        rarity = {
            name: sum(query_terms[term] * terms[term] / self._doc_freq[term]
                      for term in query_terms if self._doc_freq[term])
            for name, terms in self._terms.items()
        }
        max_rarity = max(rarity.values(), default=1.0) or 1.0
        scored = [
            RetrievedChunk(name, self._documents[name], 0.65 * lexical[name] + 0.35 * rarity[name] / max_rarity)
            for name in self._documents
        ]
        return sorted(scored, key=lambda hit: (-hit.score, hit.source))[:top_k]

    @staticmethod
    def _cosine(left: Counter[str], right: Counter[str]) -> float:
        numerator = sum(left[token] * right[token] for token in left.keys() & right.keys())
        left_norm = sqrt(sum(value * value for value in left.values()))
        right_norm = sqrt(sum(value * value for value in right.values()))
        return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0

