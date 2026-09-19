---
title: "Jarvis Agent Demo"
tags: ["Agent", "RAG", "工具调用", "权限控制", "评测"]
date: 2026-09-20
author: "Jarvis"
description: "用于面试展示的脱敏最小闭环，包含混合检索、工具风险声明、三档权限策略和确定性检索评测。"
---

# Jarvis Agent Demo

一个面向面试审阅的、可独立运行的 Agent 技术切片，而非个人助理的完整产品。

它展示四个工程决策：

- **RAG**：资料摄取与可解释的混合召回接口；
- **工具调用**：统一工具契约，模型看到 `spec`，权限层读取 `risk`；
- **权限控制**：请求批准 / 智能批准 / 完全访问三档模式，按风险而非工具名单判定；
- **评测**：无需 LLM 裁判的 Recall@K 与 MRR，适合作为检索回归检查。

## 运行

```bash
python -m src.demo
python -m pytest
```

只使用 `examples/` 中的虚构资料，不包含任何个人知识库、真实 API Key、本地绝对路径或完整产品配置。

## 结构

```text
src/rag/          # 摄取与轻量混合检索
src/tools/        # ToolSpec、ToolRisk 与受限写入示例
src/permissions/  # 三档风险自适应策略
src/evaluation/   # Recall@K、MRR
tests/            # 可复现的行为测试
examples/         # 虚构样例资料
```

生产版会接入持久化索引、嵌入模型、重排器、Agent 续作与完整评测流水线；这些依赖个人资料或部署环境的部分有意不在本仓库公开。
