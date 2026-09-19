"""三档全局权限策略：模式优先，工具风险声明驱动，无需为每个新工具配置规则。"""

from __future__ import annotations

from enum import StrEnum

from src.tools.base import ToolRisk


class PermissionMode(StrEnum):
    ASK = "ask"
    SMART = "smart"
    FULL = "full"


class PermissionPolicy:
    def __init__(self, mode: PermissionMode = PermissionMode.SMART) -> None:
        self.mode = mode

    def decide(self, risk: ToolRisk) -> str:
        """返回 allow 或 ask；高影响/不可逆操作永远不因“完全访问”而静默执行。"""
        if risk.action == "read":
            return "allow"
        if self.mode is PermissionMode.ASK:
            return "ask"
        if self.mode is PermissionMode.FULL:
            return "ask" if risk.action == "destructive" else "allow"
        # SMART：仅自动执行范围受限、可恢复、低影响的工作区写操作。
        if risk.action == "write" and risk.scope == "workspace" and risk.reversible and risk.impact == "low":
            return "allow"
        return "ask"
