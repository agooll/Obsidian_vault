# RAG 流水线总览

## 结论
testteller-agent 的 RAG 采用**双索引混合检索架构**：SQLite 本地确定性索引 + ChromaDB 向量语义索引，由 HybridRetriever 根据查询意图和本地匹配结果动态路由。

## 流水线步骤

```
数据摄取 → QueryAnalyzer(纯规则) → LocalIndex(SQLite) + ChromaDB(向量) 
→ _decide_strategy(策略路由) → fuse_results(RRF融合) → 组装Prompt → LLM调用 → QualityGate
```

## 关键设计

### 1. 查询分析零 LLM
- `QueryAnalyzer` 全部使用正则 + 关键词匹配，不调用任何 LLM
- 输出 `QueryAnalysis`（intent, test_ids, api_paths, api_methods, symbols, keywords）

### 2. 四种检索策略
由 `HybridRetriever._decide_strategy()` 决定：
- `local_exact` — 纯本地精确匹配（最快，零 Embedding）
- `hybrid` — 本地 + 向量混合（RRF 融合）
- `vector` — 纯向量搜索
- `not_found` — 精确查询没命中，直接返回空

### 3. 写入同步双索引
- `ChromaDBManager.add_documents()` 写入 ChromaDB 后立即同步写 `LocalIndex.add_documents()`
- LocalIndex 从文档原文中提取：test_ids, api_paths, symbols, keywords, config_keys 等

### 4. 质量门禁兜底
- 确定性检查：TODOs、步骤数、长度、Expected Results
- AI 语义评审（可配置）

## 验证
- source: `testteller/core/retrieval/hybrid_retriever.py`
- source: `testteller/core/retrieval/query_analyzer.py`
- source: `testteller/core/vector_store/chromadb_manager.py`
- evidence-id: evidence-0001

## 迁移场景
在其他项目中构建 RAG 系统时，可借鉴此架构：非语义查询走精确索引节省成本，语义模糊查询走向量搜索兜底。

## 下一次复习提示
- `_decide_strategy` 的 4 个分支对应的触发条件是什么？
- RRF 如何在融合时让精确结果排在语义结果之前？
