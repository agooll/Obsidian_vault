# testteller-agent RAG 流水线深度解析

## 模块目标
深入理解 testteller-agent 从查询输入 → 检索 → 策略路由 → Prompt 组装 → LLM 调用 → 质量门禁的完整 RAG 流水线，重点掌握双索引混合检索架构的设计取舍。

## 对话记录

### 01｜主线：RAG流水线总览

#### 我的疑惑
刚开始接触该项目，想知道 RAG 流水线如何串联。猜测 QueryAnalyzer 是通过 LLM 做语义分析来分类意图。

#### AI 的提问
观察架构图，猜 QueryAnalyzer 是如何判断用本地索引精确查找还是向量搜索语义匹配的？是否需要调用 LLM？

#### 我的回答
通过 LLM 的语义分析然后输出，接着根据 RAG 的向量检索进行判断。

#### AI 的反馈与纠正
完全相反。QueryAnalyzer 是纯规则引擎（Zero LLM），通过 if-elif 关键词匹配做意图分类，正则做信息提取。作者在代码注释中写明："Rule-based analyzer. Ambiguous Chinese questions deliberately fall back to vectors."

#### 最终理解
QueryAnalyzer 的 _classify_intent 就是"if '生成' in query → GENERATE"这种级别。提取信息也是正则（HTTP_METHOD_PATTERN、TEST_ID_PATTERN 等）。零 LLM 调用，微秒级。

#### 代码或证据
`testteller/core/retrieval/query_analyzer.py:L39-L50` — _classify_intent 方法

---

### 02｜插问：query_analyzer.py L39-L50 的代码意义

#### 插问内容
这段 _classify_intent 的代码每一行在做什么？

#### AI 的回答
这段代码是一个 if-elif 优先级链：
- L40：匹配 GENERATE 关键词 → "生成"、"测试用例"、"test case"
- L42：匹配 IMPACT 关键词 → "影响"、"调用链"
- L44：匹配 SIMILARITY 关键词 → "类似"、"相似"
- L46：匹配 ANALYSIS 关键词 → "风险"、"边界"、"分析"
- L48：匹配 LOCATE 关键词 → "在哪里"、"定位"
- L50：兜底返回 FACT_LOOKUP

顺序敏感、互斥、零 AI 成本。`_decide_strategy` 用这个意图值决定检索策略。

#### 与主线的关系
这是插问，详细解释了 _classify_intent 的每一行代码逻辑。

#### 对主线的影响
无影响，加深对意图分类器的理解。

---

### 03｜主线：FACT_LOOKUP 到 LLM 的调用链

#### 我的疑惑
到 FACT_LOOKUP（兜底）这一步就开始进行 LLM 的调用了吗？

#### AI 的回答
不，FACT_LOOKUP 只是决定了检索策略。整个检索层（QueryAnalyzer → HybridRetriever → LocalIndex/ChromaDB）全程不调 LLM。LLM 是在 Generator Agent 中，检索结果被填入 Prompt 的 {context} 之后才调用的。

#### 最终理解
检索层零 LLM → 拿到文档 → 填入 Prompt → 才调 LLM。Generator Agent 的 `generate_test_cases` 方法里调用 `llm_manager.generate_text_async(prompt)` 才是真正调 LLM 的地方。

#### 代码或证据
`testteller/generator_agent/agent/testteller_agent.py:L302-L354` — generate_test_cases 方法

---

### 04｜主线：检索为空不卡死

#### 我的疑惑
如果检索出来的文档太少不足以生成完整 Prompt，会不会卡住？

#### AI 的回答
不会。三个防御层：
1. CLI 入口预检集合是否为空，空则提示用户是否继续
2. 检索结果为空时 context 就是空字符串，依然发给 LLM
3. 质量门禁兜底：`_calculate_quality_score` 检查 TODO、步骤数、长度、Expected Result

偏好是"宁愿给次优结果也不让系统崩溃"。

#### 最终理解
检索零命中 → Prompt 只有 query → LLM 全靠通用知识硬编。质量差但不会崩。后续有 QualityGate 做双重评分（确定性规则 + AI 语义评审）。

---

### 05｜主线：LOCATE + not_found 边界情况

#### AI 的提问
当用户查 "E2E_LOGIN_001 在哪里" 但本地索引没有时，系统直接返回 not_found，不走向量搜索。这个设计合理吗？

#### 我的回答
合理。因为精确查找没命中 → not_found。如果这时候走向量检索，返回的是一堆不相干的片段，组装成劣质 Prompt，LLM 花更多 token 生成低质量结果，质量门禁又花钱打回，白忙一场。提前切断比事后补救便宜得多。

#### AI 的反馈与纠正
分析完全正确，和作者的设计意图一致。这笔账算得很清楚。

#### 最终理解
`_decide_strategy` 第三分支：`exact_entity_requested=True` 且 `intent in {LOCATE, FACT_LOOKUP}` 但本地没找到 → not_found。用户指名道姓找精确 ID，精确索引说没有，那就是没有。不走向量搜索碰运气。

#### 代码或证据
`testteller/core/retrieval/hybrid_retriever.py:L51-L52` — not_found 分支

---

### 06｜主线：进入 diagnosis 阶段

#### AI 的提问
要不要进入下一阶段？（diagnosis：用具体查询测试理解，诊断盲区）

#### 我的回答
进入 diagnosis。

#### AI 的反馈与纠正
验证 evidence 通过，TRANSITION_APPROVED diagnosis。提出诊断测试题：

查询 1: "生成登录模块的测试用例" — 需要预测意图、提取信息、检索策略等。

#### 最终理解
用户同意进入 diagnosis，但随后要求先回到代码做完整复习再做题。

---

### 07｜插问：回到代码复习理解

#### 插问内容
刚才没有完整理解代码意义，请求拉回上下文重新学习。

#### AI 的回答
暂停诊断，保存分支，开始按流水线顺序逐模块拉取全部关键代码。

#### 与主线的关系
主线是诊断测试，这个插问是回到上一阶段做代码复习。

#### 对主线的影响
诊断测试暂停，转为代码深度复习。

---

### 08｜主线：全面拉取并逐模块解析

#### AI 的反馈与纠正
按流水线顺序拉取全部核心文件并行阅读：`retrieval_patterns.py`、`models.py`、`query_analyzer.py`、`local_index.py`、`chromadb_manager.py`、`testteller_agent.py`、`result_fusion.py`，并开始逐模块详解。

#### 最终理解
已完成 retrieval_patterns、models、query_analyzer 三个模块的逐行解析。

---

### 09｜插问：retrieval_patterns.py 各变量含义

#### 插问内容
L5-L19 每一段定义的是什么？变量名含义看不懂。

#### AI 的回答
详细解释了 13 个正则变量的含义，每个的作用、匹配示例和不匹配示例。

| 变量名 | 用途 |
|---|---|
| TEST_ID_PATTERN | 匹配 E2E/INT/TECH/MOCK 开头的测试 ID |
| API_PATH_PATTERN | 匹配 /api/ 开头的 API 路径 |
| HTTP_METHOD_PATTERN | 匹配 GET/POST/PUT 等 HTTP 方法 |
| PYTHON_CLASS_PATTERN | 从代码中提取 Python 类名 |
| PYTHON_FUNCTION_PATTERN | 从代码中提取 Python 函数名 |
| JS_TS_FUNCTION_PATTERN | 从代码中提取 JS/TS 函数/变量名 |
| QUALIFIED_SYMBOL_PATTERN | 提取 a.b.c 格式的全限定符号 |
| DATA_TESTID_PATTERN | 提取前端 data-testid 属性值 |
| ENV_* 三个 | 提取环境变量（分别对应 Python/Node/模板语法） |
| FILE_NAME_PATTERN | 匹配带扩展名的文件名 |
| TOKEN_PATTERN | 通用分词：英文字母词 + 中文多字词 |

#### 与主线的关系
正则引擎是所有检索层模块的基础。

#### 对主线的影响
无影响，加深对正则系统设计的理解。

---

### 10｜插问：正则表达式 TEST_ID_PATTERN 语法

#### 插问内容
正则表达式的语法不懂，看表格不理解为什么。

#### AI 的回答
逐字符拆解 `\b(?:E2E|INT|TECH|MOCK)_[A-Z0-9_]+\b`：
- `\b`：单词边界，防止部分匹配
- `(?:...)`：非捕获组，四选一
- `_`：字面下划线
- `[A-Z0-9_]+`：字符类，大写字母/数字/下划线至少 1 个
- `re.IGNORECASE`：大小写不敏感

用多个正例和反例做测试验证。

#### 与主线的关系
正则语法是理解所有 pattern 的基础。

#### 对主线的影响
无影响，基础语法查漏补缺。

---

### 11｜主线：local_index.py 写入+查询全流程

#### AI 的反馈与纠正
详解 LocalIndex：

**写入时**（add_documents → _build_entry）：
- 用正则从文档原文中提取 test_ids、api_paths、api_methods、keywords、symbols、config_keys
- 写入 local_documents 表存原文 + content_hash（去重）
- 展平为 (term, term_type, chunk_id) 写入 local_terms 表

**查询时**（search）：
- collect() 按优先级分组查询 local_terms 表
- 每种实体类型有不同权重：test_id/api_key=1.00, api_path=0.88, keyword=0.45
- 累加 scores[chunk_id] → 取原文 → 降序排序 → 截取 limit 条
- 返回 LocalSearchResult(items, match_type, unique, exact_entity_requested)

#### 最终理解
LocalIndex 是 ChromaDB 的伴生 SQLite 索引。写入时同步提取实体，查询时精确/部分匹配获得权重分数，为 HybridRetriever 的策略路由提供基础数据。

#### 代码或证据
`testteller/core/retrieval/local_index.py`
`testteller/core/vector_store/chromadb_manager.py:L203-L208` — 写入协同

---

### 12｜落盘完成

#### AI 的回答
已完成所有笔记落盘。

#### 最终理解
本次学习到此为止。下次继续从 chromadb_manager.py → hybrid_retriever.py → result_fusion.py 推进。

---

## 模块总结

已完成 RAG 流水线前段（检索层）的深入学习：

| 模块 | 状态 | 核心要点 |
|---|---|---|
| `retrieval_patterns.py` | ✅ 完成 | 13 个正则变量集中管理，TOKEN_PATTERN 同时处理中英文 |
| `models.py` | ✅ 完成 | QueryAnalysis → LocalSearchResult → RetrievalResult 三层数据流转 |
| `query_analyzer.py` | ✅ 完成 | 纯规则意图分类，if-elif 链，中文二元组轻量分词 |
| `local_index.py` | ✅ 完成 | SQLite 双表，读写分离，权重体系，幂等去重 |
| `chromadb_manager.py` | ⬜ 待学 | 向量库 + LocalIndex 写入协同 |
| `hybrid_retriever.py` | ⬜ 待学 | 4 种策略路由决策 |
| `result_fusion.py` | ⬜ 待学 | RRF 融合公式 |
| `testteller_agent.py` + `prompts.py` | ⬜ 待学 | Prompt 组装 + LLM + QualityGate |

## 容易再次混淆的地方

1. **QueryAnalyzer 调不调 LLM**：零 LLM，纯规则，作者强调"Rule-based analyzer"
2. **FACT_LOOKUP 和 LLM 的关系**：FACT_LOOKUP 只是意图分类结果，检索层全程不调 LLM。LLM 在 Generator Agent 里才调用
3. **not_found 何时触发**：精确实体请求（test_id/api_path/symbols）+ 本地索引没找到，直接返回空，不走向量
4. **写入和查询的协同**：写入时 ChromaDB 先写向量 → 同步写 LocalIndex；查询时 HybridRetriever 先查 SQLite 再决定是否查向量

## 待复习问题

1. `_decide_strategy` 的 4 个分支对应的触发条件是什么？
2. `MatchType.EXACT` 和 `unique=True` 分别在什么条件下成立？
3. RRF 融合（result_fusion.py）如何让精确结果排在语义结果之前？
4. ChromaDB 写入时 Embedding 失败会怎样（看 chromadb_manager.py L147）？
5. `TOKEN_PATTERN` 中 `[\u4e00-\u9fff]{2,}` 为什么要求至少 2 个中文？不能 3 个吗？

## 复习记录
- 2026-07-19：完成本模块第一次学习并落盘
