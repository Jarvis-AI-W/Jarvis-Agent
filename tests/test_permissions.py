from src.permissions import PermissionMode, PermissionPolicy
from src.tools import DraftNoteTool, ToolRisk


def test_smart_allows_scoped_reversible_workspace_write(tmp_path) -> None:
    assert PermissionPolicy().decide(DraftNoteTool(tmp_path).risk) == "allow"


def test_destructive_operation_still_asks_in_full_mode() -> None:
    danger = ToolRisk("destructive", "external", False, "high")
    assert PermissionPolicy(PermissionMode.FULL).decide(danger) == "ask"
