"""一个受范围约束的写入工具：只写入调用方指定的 demo 目录。"""

from pathlib import Path

from .base import Tool, ToolRisk, ToolSpec


class DraftNoteTool(Tool):
    spec = ToolSpec(
        name="save_draft_note",
        description="将整理内容保存为 demo 目录中的 Markdown 草稿，不覆盖已有文件。",
        parameters={"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}}, "required": ["title", "content"]},
    )
    risk = ToolRisk(action="write", scope="demo", reversible=True, impact="low")

    def __init__(self, output_dir: str | Path) -> None:
        self._root = Path(output_dir).resolve()

    def _target(self, title: str) -> Path:
        filename = "".join(char if char.isalnum() or char in "-_" else "-" for char in title).strip("-") or "untitled"
        target = (self._root / f"{filename}.md").resolve()
        if self._root not in target.parents:
            raise ValueError("拒绝写出 demo 目录")
        return target

    def preview(self, *, title: str, content: str, **_: object) -> str:
        return f"将在 demo 目录新建 {self._target(title).name}（{len(content)} 个字符，不覆盖已有文件）。"

    def run(self, *, title: str, content: str, **_: object) -> str:
        target = self._target(title)
        self._root.mkdir(parents=True, exist_ok=True)
        if target.exists():
            return f"未写入：{target.name} 已存在（默认不覆盖）。"
        target.write_text(f"# {title}\n\n{content.strip()}\n", encoding="utf-8")
        return f"已写入 demo 草稿：{target.name}"

