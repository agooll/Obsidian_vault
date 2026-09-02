# HelloAgents × LangGraph｜Day 6 独立学习卡：Persistence 验收 + LangGraph 章节收口

**当前理论进度：** Tool Calling ✅ → ReAct ✅ → Plan-and-Solve ✅ → Reflection ✅；LangGraph Day 1–4 已过关，Day 5 已进入 Tool Agent + Persistence。  
**当前代码进度：** `ToolNode + tools_condition` 已完成第一阶段；`Checkpointer + thread_id + Tool Agent` 尚未收到“完成”验收，因此今天先把它真正跑稳。  
**今天：LangGraph Day 6｜Persistence 闭环验收 + HelloAgents 6.5 LangGraph 收口。**  
**今日模式：** 恢复/收口 + 少量理论，不开启新章节，不继续扩大代码债。  
**职业主线：** AI Agent 开发；今天重点培养 State、Trace、会话隔离和 Workflow 设计能力。

---

## 0｜今天为什么不直接冲 Memory

你现在已经认识了：

```text
State
Node
Edge
Conditional Edge
Reducer
ToolNode
tools_condition
Checkpoint
Checkpointer
thread_id
```

但如果这些还只是“每个词都听过”，而没有真正串成一个 Agent：

```text
User
↓
LLM
↓
Tool
↓
State
↓
Checkpoint
↓
下一轮继续
```

那继续学 Memory 只会把概念越堆越多。

今天做两件事：

```text
① 把 Day 5 Persistence 代码真正验收掉
② 把 HelloAgents 6.5 LangGraph 章节收口
```

---

# A｜白天实习空闲 2–3 小时

## 1.【白天复习｜20–25 分钟】

今天先闭卷，不要看昨天笔记。

### Q1

把下面链路补完整：

```text
HumanMessage
↓
State["messages"]
↓
LLM Node
↓
AIMessage(tool_call)
↓
__________
↓
ToolNode
↓
__________
↓
State["messages"]
↓
LLM Node
↓
Final
```

### Q2

分别用一句话解释：

```text
State
Checkpoint
Checkpointer
thread_id
```

不能互相用定义套定义。

### Q3

为什么：

```text
thread_id = "A"
```

第二次 `invoke()` 可以延续第一次的上下文，而：

```text
thread_id = "B"
```

应该是另一条状态线？

### Q4

`ToolNode` 和 `Checkpointer` 谁负责：

```text
执行工具？
保存状态？
```

为什么不能混为一谈？

### Q5

为什么：

```text
add_messages
```

对一个多轮 Tool Agent 特别重要？

如果没有它，最容易发生什么？

### Q6

闭卷画：

```text
LLM → Tool → LLM
```

以及：

```text
invoke 1 → 保存 → invoke 2 → 恢复
```

两条循环分别解决什么问题？

---

## 2.【白天今日原文】

今天严格按 HelloAgents 第 6 章收尾。

### 【必看】6.5.2 三步问答助手后半部分

重点定位：

> **第 6 章 → 6.5 框架四：LangGraph → 6.5.2 三步问答助手**

今天读的时候不要再逐行看。

只回答这 5 个问题：

```text
① SearchState 有哪些字段？
② 每个 Node 读取了哪些 State？
③ 每个 Node 更新了哪些 State？
④ Edge 为什么这样连接？
⑤ InMemorySaver 在整个 Workflow 中是什么角色？
```

建议：**30–40 分钟。**

### 【重点】6.5.3 LangGraph 的优势与局限

今天必须看。

把它压成：

```text
LangGraph 为什么适合：

复杂流程
可控 Agent
需要循环
需要审计 / Trace
需要人工介入

LangGraph 为什么不一定适合：

极简单问答
只需要一次 LLM Call
完全自由对话型协作
```

建议：**20–30 分钟。**

### 【重点练习】第 6 章 Exercises 中的 LangGraph 题

在：

```text
Understand → Search → Answer
```

基础流程上增加：

```text
Reflection Node
```

当 Answer 质量不足时：

```text
重新 Search
或
重新 Generate
```

形成循环。

### 【略看】

```text
AutoGen / AgentScope / CAMEL 的对比细节
其他框架的全部练习题
```

### 【今天暂不看】

```text
第 7 章 从零构建 Agent Framework
第 8 章 Memory / RAG
Human-in-the-loop 深入实现
Multi-Agent
```

---

## 3.【白天理解目标①】Persistence 的完整数据流

今天必须从单词升级到链路：

```text
第一次 invoke
│
├─ thread_id = A
│
↓
HumanMessage
↓
State["messages"]
↓
LLM Node
↓
Tool Call
↓
ToolNode
↓
ToolMessage
↓
LLM Node
↓
Final
↓
New State
↓
Checkpointer
↓
Checkpoint
```

第二轮：

```text
第二次 invoke
│
├─ thread_id = A
│
↓
找到同一条 Thread
↓
恢复已有 State
↓
加入新的 HumanMessage
↓
继续 Graph
```

重点：

> **Checkpointer 不负责推理。**

> **thread_id 不负责存数据。**

> **State 才是当前数据，Checkpoint 是保存下来的快照。**

---

## 4.【白天理解目标②】两个“循环”不能混

### 第一种：Graph 内部 Cycle

```text
LLM
↓
ToolNode
↓
LLM
```

解决：

> **一次任务中，LLM 和环境/工具反复交互。**

对应以前 ReAct：

```text
Action
↓
Observation
↓
Next Decision
```

### 第二种：跨 invoke 状态延续

```text
invoke 1
↓
Checkpoint
↓
invoke 2
```

解决：

> **这次会话结束后，下次调用还能继续之前的状态。**

这不是 ReAct Loop，而是 **Persistence**。

---

## 5.【白天理解目标③】LangGraph 为什么适合生产 Agent

例如：

```text
用户提交代码
↓
生成代码
↓
运行测试
↓
测试通过？
├─ YES → END
└─ NO
   ↓
错误分析
↓
重新生成
↓
再次测试
```

如果用 Graph：

```text
generate
↓
test
↓
Conditional Edge
├─ pass → END
└─ fail → fix
            ↓
          test
```

这种显式状态、条件分支和循环正是 LangGraph 的优势。

---

## 6.【白天工程思维】Agent 出问题到底查哪里

假设：

> 第二轮 Agent 忘记第一次工具结果。

检查：

```text
层 1：LLM
最终输入 messages 有历史吗？

↓

层 2：State
ToolMessage 是否真正进入 State？

↓

层 3：Reducer
messages 有没有正确合并？

↓

层 4：Persistence
Checkpointer 有没有挂到 compile？

↓

层 5：Thread
两次是不是同一个 thread_id？

↓

层 6：Routing
Tool Call 有没有正确进入 ToolNode？
```

---

## 7.【Agent 开发面试表达｜15 分钟】

### 面试题 A

> 为什么 LangGraph 比单纯 while 循环更适合复杂 Agent Workflow？

尝试包含：

```text
State
Node
Edge
Conditional Routing
Cycle
Trace
可控性
模块化
```

### 面试题 B

> LangGraph 中 Tool Agent 怎么实现多轮会话？

至少出现：

```text
messages
Checkpointer
Checkpoint
thread_id
same thread
```

---

## 8.【晚上代码预演｜15–20 分钟】

晚上开代码之前先在纸上写：

```text
Day4 Tool Agent
+
Day5 Persistence
```

完整架构：

```text
Tool
↓
LLM.bind_tools
↓
MessagesState
↓
LLM Node
↓
tools_condition
↙           ↘
ToolNode     END
↓
LLM Node

+

InMemorySaver
↓
compile(checkpointer=...)

+

config
↓
thread_id
```

---

# B｜晚上约 2 小时：今天以代码验收为主

## 9.【晚上目标①】闭卷重建最小骨架｜35 分钟

新开文件，例如：

```text
langgraph_day6_persistence_rewrite.py
```

闭卷写结构：

```text
1. Tool
2. tools
3. LLM.bind_tools
4. MessagesState
5. llm_node
6. ToolNode
7. StateGraph
8. START → llm_node
9. tools_condition
10. tools → llm_node
11. InMemorySaver
12. compile(checkpointer)
13. config(thread_id)
14. invoke
```

API 参数记不住可以查；Graph 结构记不住则今天不算过关。

---

## 10.【晚上目标②】Same Thread｜20 分钟

```text
thread_id = "day6-A"
```

第一轮：

```text
计算 12 * 8
```

第二轮：

```text
把刚才的结果再加 4
```

理想数据流：

```text
12 * 8
↓
Tool
↓
96
↓
Checkpoint

第二轮
↓
加载 History
↓
96 + 4
↓
Tool
↓
100
```

---

## 11.【晚上目标③】Different Thread｜15 分钟

换：

```text
thread_id = "day6-B"
```

直接问：

```text
把刚才的结果加 4
```

观察并解释：

> B 属于另一条 thread，它不应该依赖 A 的 State History。

---

## 12.【晚上目标④】Trace State｜15 分钟

至少使用一个：

```text
stream()
```

或者：

```text
get_state(config)
```

观察：

```text
HumanMessage
AIMessage(tool_call)
ToolMessage
AIMessage(final)
```

并自己回答：

```text
这条 Message 是谁产生的？
什么时候进入 State？
哪个 Node 之后出现？
```

---

## 13.【验证】今天手动 Case

今天仍然不要求 Pytest。

### Case 1｜无 Tool

```text
你好
```

预期：

```text
LLM
↓
END
```

### Case 2｜一次 Tool

```text
12 * 8
```

预期：

```text
LLM
↓
ToolNode
↓
LLM
↓
END
```

### Case 3｜Same Thread

```text
Thread A

12 * 8
↓
刚才结果 + 4
```

预期：

```text
96
↓
100
```

### Case 4｜Different Thread

```text
Thread B

刚才结果是多少？
```

验证：

```text
A/B 状态隔离
```

---

## 14.【额外 20 分钟】把 Reflection 搬进 LangGraph

今天不要求写完整代码。

只画：

```text
START
↓
Generate
↓
Check Quality
↓
passed?
├─ YES → END
└─ NO
   ↓
Reflect
↓
Feedback
↓
Revise
↓
Check Quality
```

然后回答：

```text
哪些是 Node？
哪个是 Conditional Edge？
哪个字段需要存在 State？
为什么需要 max_rounds？
```

---

## 15.【闭卷小测】

### Q1

Graph 内部：

```text
LLM → ToolNode → LLM
```

和跨调用：

```text
invoke → Checkpoint → invoke
```

本质区别是什么？

### Q2

为什么：

```text
thread_id
```

不是 State，也不是 Checkpoint？

### Q3

LangGraph 为什么特别适合：

```text
生成
↓
检查
↓
不通过
↓
修正
↓
再次检查
```

这种 Agent？

### Q4｜代码 / 流程题

闭卷画出完整：

```text
HumanMessage
↓
State
↓
LLM
↓
Conditional Edge
↙            ↘
ToolNode      END
↓
ToolMessage
↓
LLM
↓
New State
↓
Checkpointer
↓
Checkpoint

第二次 invoke
↓
thread_id
↓
恢复 State
```

要求自己标：

```text
控制流
数据流
执行层
持久化层
```

---

## 16.【今天完成标准】

### 理论过关

脱离资料能说清：

```text
State
Reducer
Conditional Edge
ToolNode
Checkpoint
Checkpointer
thread_id
```

并能解释它们之间不是一回事。

### 代码过关

脱离完整教程可以写出：

```text
Tool Agent
+
InMemorySaver
+
thread_id
```

核心骨架。

### 手动 Case 过关

至少跑通：

```text
普通 LLM 路径       ✅
Tool 路径           ✅
Same Thread         ✅
Different Thread    ✅
```

### HelloAgents 第 6 章 LangGraph 收口

最后再满足：

```text
能画 6.5.2 三步问答 Workflow
能说 LangGraph 3 个优势
能说 LangGraph 2 个局限
能设计一个 Conditional Edge Cycle
```

达到这些：

> **LangGraph Day 6 ✅**

同时：

> **HelloAgents 6.5 LangGraph 第一阶段 ✅ 正式收口**

---

## 状态反馈

完成后回复以下任一种：

- `完成`
- `未完成 + 卡点`
- `暂停`
- `今天忙 + 可用时间`
