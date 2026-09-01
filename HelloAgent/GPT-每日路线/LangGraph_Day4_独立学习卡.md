# HelloAgents × LangGraph｜Day 4 独立学习卡：ToolNode + tools_condition + ReAct Graph

**当前理论进度：** Tool Calling ✅ → ReAct ✅ → Plan-and-Solve ✅ → Reflection ✅；LangGraph Day 1–3 已完成基础图、State / Reducer、Persistence / Checkpointer。  
**当前代码进度：** 已能理解 StateGraph、Conditional Edge 和 State 数据流；Persistence 处于“概念基本通、后续继续手动验证”阶段。  
**今天：Day 4｜LangGraph ToolNode / tools_condition / ReAct Graph。**  
**今日模式：** 正常推进日；重点是 Tool Calling Workflow，不再继续学新的经典 Agent Pattern。  
**职业主线：** AI Agent 开发；测试开发能力主要作为 Debug、Case、Eval 等工程质量能力辅助。

---

## 0｜今天的主目标

前面学 ReAct 时，手写链路是：

```text
LLM
↓
Action Parser
↓
ToolExecutor
↓
Registry
↓
Tool
↓
Observation
↓
LLM
```

今天要看 LangGraph 怎么把这套东西重新组织成：

```text
LLM Node
↓
Conditional Routing
↓
ToolNode
↓
ToolMessage
↓
LLM Node
```

最终建立：

```text
用户问题
↓
State["messages"]
↓
LLM Node
↓
AIMessage
↓
是否包含 tool_calls？
├─ NO  → END
└─ YES → ToolNode
            ↓
        ToolMessage
            ↓
    写回 State["messages"]
            ↓
        LLM Node
            ↓
       Final Answer
            ↓
           END
```

# A｜白天 2–3 小时：理解 + 代码预演

## 1.【白天复习｜20–25 分钟】

先闭卷，不直接看答案。

### Q1
补全：

```text
Input
↓
State
↓
Node
↓
__________
↓
Reducer
↓
__________
↓
Conditional Edge
↓
Next Node
```

### Q2
为什么 `return {"result": "done"}` 通常叫 Partial State Update，而不是一个完整 State？

### Q3
解释 `logs: Annotated[list[str], operator.add]` 为什么可以累积多个 Node 的 logs。

### Q4
为什么 `add_messages` 不等于 `operator.add`？

### Q5
分别说出 `State / Checkpoint / Checkpointer / thread_id` 的职责。

### Q6
为什么不同 `thread_id` 可以维护独立状态线？

---

## 2.【白天今日原文】

继续围绕 **HelloAgents 第 6 章 → 6.5 LangGraph**。

### 必看
快速复习：
- State
- Node
- Edge
- Conditional Edge
- Cycle

### 重点
观察：
- State 怎么定义
- Node 如何读取 State
- Node 如何返回 Partial Update
- Graph 如何连接
- `compile / invoke / stream`

### 今天新增重点
- ToolNode
- tools_condition
- `LLM.bind_tools()`
- messages
- `AIMessage.tool_calls`
- ToolMessage

### 略看
- 复杂 Prompt
- 模型参数
- 工具业务细节

### 暂不看
- Multi-Agent
- 复杂 Memory
- Human-in-the-loop
- RAG
- Agent Eval
- 复杂持久化

---

## 3.【白天理解目标①】ToolNode 到底替代了什么？

```text
手写 ReAct                  LangGraph

LLM 调用                  → LLM Node
Tool Call                 → AIMessage.tool_calls
if 是否调用工具           → tools_condition
ToolExecutor              → ToolNode
Observation               → ToolMessage
History                   → State["messages"]
while Loop                → Graph Cycle
Final Answer              → END
```

关键句：

> ToolNode 是“工具执行节点”，不是“决定要不要使用工具的节点”。

---

## 4.【白天理解目标②】tools_condition

### tools_condition
职责：

```text
读取 State["messages"]
↓
找到最后一条 AIMessage
↓
判断有没有 tool_calls
↓
有 → tools
无 → END
```

它属于 **控制流 / Routing**。

### ToolNode
职责：

```text
读取 AIMessage 中的 tool_calls
↓
找到对应 Tool
↓
执行 Tool
↓
产生 ToolMessage
↓
更新 messages
```

它属于 **执行逻辑 / Execution**。

---

## 5.【白天理解目标③】为什么 ToolNode 后面还要回 LLM？

例子：

```text
User：
12 × 8 等于多少？
```

第一轮：

```text
LLM Node
↓
AIMessage
↓
tool_call:
Calculator(12*8)
```

ToolNode：

```text
12*8
↓
96
↓
ToolMessage("96")
```

这里通常不能直接 END，因为 `96` 只是 Tool Result。

还需要：

```text
ToolMessage
↓
写入 messages
↓
LLM Node
↓
模型读取工具结果
↓
Final Answer
```

因此形成：

```text
              ┌──────────────┐
              │              │
              ↓              │
START → LLM Node → ToolNode ─┘
          │
          ↓
         END
```

---

## 6.【白天理解目标④】Messages State

例如：

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

运行过程可能是：

```text
HumanMessage
↓
AIMessage(tool_call)
↓
ToolMessage(result)
↓
AIMessage(final answer)
```

所以 `messages` 同时承担了以前 ReAct 里的 History / Context 角色。

---

## 7.【工程思维】

如果 Agent 没有调用工具，按顺序检查：

```text
Tool 是否定义正确？
↓
Tool 是否 bind 给 LLM？
↓
LLM 有没有生成 tool_calls？
↓
tools_condition 读取到了什么？
↓
Router 有没有进入 ToolNode？
↓
ToolNode 是否执行成功？
↓
ToolMessage 有没有进入 State？
↓
第二轮 LLM 是否读到了最新 messages？
```

---

## 8.【Agent 开发面试表达｜15 分钟】

闭卷尝试 45–60 秒回答：

> LangGraph 中一个带工具调用的 Agent Workflow 是怎么工作的？

要求至少包含：

```text
State
LLM Node
AIMessage.tool_calls
Conditional Routing
ToolNode
ToolMessage
Graph Cycle
END
```

重点讲数据怎么流，而不是 API 名怎么背。

---

## 9.【晚上代码预演｜20 分钟】

先画：

```text
              ┌───────────────┐
              │               │
START        ↓               │
  ↓       LLM Node            │
  │          ↓                │
  │     tools_condition       │
  │       ↙       ↘           │
  │    ToolNode    END        │
  │       ↓                   │
  └───────┴───────────────────┘
```

然后闭卷回答：

1. User Message 放在哪里？
2. LLM Node return 什么？
3. Tool Call 保存在哪里？
4. tools_condition 读取什么？
5. ToolNode return 什么？
6. Tool Result 怎么回到 LLM？

---

# B｜晚上约 2 小时：最小 Tool Agent

## 10.【晚上目标】最小 Tool Agent

只写：

```text
START
↓
LLM Node
↓
tool call?
↙       ↘
YES      NO
↓         ↓
ToolNode  END
↓
LLM Node
```

## 11.【第一轮｜30 分钟】允许看资料跑通

目标结构：
- ToolNode
- tools_condition
- StateGraph
- MessagesState
- bind_tools
- add_node
- add_edge
- add_conditional_edges
- compile
- invoke / stream

工具尽量简单，例如 calculator。

## 12.【第二轮｜30–40 分钟】关闭资料重写

只看 Graph：

```text
START
↓
chatbot
↓
tools_condition
↙       ↘
tools     END
↓
chatbot
```

自己恢复：
- 定义 Tool
- tools = [...]
- llm.bind_tools(tools)
- 定义 State
- 定义 chatbot / llm_node
- ToolNode(tools)
- StateGraph
- Conditional Routing
- tools → chatbot
- compile

API 名忘记可以定点查，但 Graph 结构不能照抄。

---

## 13.【验证】优先手动 Case

### Case A｜无需 Tool

```text
你好，你是谁？
```

预期：

```text
START
↓
LLM
↓
没有 tool_call
↓
END
```

### Case B｜需要 Tool

```text
12 * 8 等于多少？
```

预期：

```text
HumanMessage
↓
LLM
↓
AIMessage(tool_call)
↓
ToolNode
↓
ToolMessage("96")
↓
LLM
↓
AIMessage("12 × 8 = 96")
↓
END
```

### Case C｜错误 Tool 参数

观察：

```text
Tool Error
↓
ToolNode
↓
错误信息是否进入 messages？
↓
LLM 后续怎么处理？
```

今天不要求复杂错误恢复。

---

## 14.【Day 3 顺手复习｜10 分钟】

思考：

如果 `compile()` 时加入 Checkpointer，并设置：

```text
thread_id = "001"
```

那么 HumanMessage / AIMessage / ToolMessage 所在的 State 能不能随着 Graph 执行被保存成 checkpoint？

今天不要求实现，只先把：

```text
Tool Agent
+
Persistence
```

接起来。

---

## 15.【闭卷小测】

### Q1
`tools_condition` 和 `ToolNode` 最大区别是什么？

### Q2
为什么 ToolNode 执行后通常需要回到 LLM Node，而不是直接 END？

### Q3
以前 ReAct 中的 `Observation / History`，到了 LangGraph Tool Agent 中分别更接近什么？

### 流程题
把：

```text
LLM
↓
Action Parser
↓
ToolExecutor
↓
Observation
↓
LLM
```

转换成 LangGraph 版本，并标出：
- State
- LLM Node
- Conditional Edge
- ToolNode
- ToolMessage
- Cycle
- END

---

# 16.【今天完成标准】

## 理论过关
能闭卷解释：
- ToolNode
- tools_condition
- tool_calls
- ToolMessage
- messages
- 为什么 `LLM → ToolNode → LLM` 会形成 Cycle

## 代码过关
关闭资料后能够：
- 定义一个 Tool
- bind 给 LLM
- 创建 ToolNode
- 创建 Conditional Routing
- 形成 tools → LLM Cycle

并跑通：
- Case A：不需要工具
- Case B：需要工具

达到即：

> **LangGraph Day 4 第一阶段 ✅**

---

# 当前路线位置

```text
Tool Calling        ✅
ReAct               ✅
Plan-and-Solve      ✅
Reflection          ✅

LangGraph Day 1
Graph / Node / Edge / Cycle
✅

LangGraph Day 2
State / Update / Reducer
✅

LangGraph Day 3
Checkpoint / Checkpointer / thread_id
✅ 第一轮

LangGraph Day 4
ToolNode / tools_condition / ReAct Graph
← 今天

后续：
Persistence + Tool Agent
↓
Memory
↓
Human-in-the-loop
↓
完整 Agent Workflow
↓
第一个真实 Agent 项目 V1
```

---

## 状态反馈

完成后回复以下任一种：
- `完成`
- `未完成 + 卡点`
- `暂停`
- `今天忙 + 可用时间`
