"""模型工具的最小契约，以及权限层消费的风险声明。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict


@dataclass(frozen=True)
class ToolRisk:
    action: Literal["read", "write", "network", "destructive"]
    scope: Literal["demo", "workspace", "external"]
    reversible: bool
    impact: Literal["low", "high"]


class Tool(ABC):
    spec: ToolSpec
    risk: ToolRisk

    @abstractmethod
    def preview(self, **arguments: object) -> str:
        """在真正执行前给用户看的可读说明。"""

    @abstractmethod
    def run(self, **arguments: object) -> str:
        """返回给 Agent 的观察结果。"""

