# HelloAgents × LangGraph｜Day 5 独立学习卡：Tool Agent + Persistence

**当前理论进度：** Tool Calling ✅ → ReAct ✅ → Plan-and-Solve ✅ → Reflection ✅；LangGraph Day 1–4 已完成。  
**当前代码进度：** 已进入 LangGraph Tool Agent；`ToolNode + tools_condition + messages` 已完成第一轮，Persistence 需要和 Tool Agent 真正接通。  
**今天：LangGraph Day 5｜Tool Agent + Checkpointer + thread_id。**  
**今日模式：** 工作日代码闭环日；今天不继续增加新理论债。  
**主线目标：** 从“单次能调用工具”升级到“同一会话可以跨 invoke 延续状态”。

---

## 0｜今天需要的关键背景

昨天的 Agent 已经能完成：

```text
HumanMessage
↓
LLM Node
↓
AIMessage(tool_call)
↓
tools_condition
↓
ToolNode
↓
ToolMessage
↓
LLM Node
↓
Final Answer
↓
END
```

但这只解决：

> **一次 Graph 执行内部的数据流。**

今天解决：

```text
第一次 invoke
↓
保存 State
↓
第二次 invoke
↓
恢复之前 State
↓
继续 Agent
```

核心组合只有：

```text
Tool Agent
+
Checkpointer
+
thread_id
```

今天不要继续学 Multi-Agent、长期 Memory 或 RAG。

---

# A｜白天 2–3 小时

## 1｜【白天复习】20 分钟

禁止先翻笔记。

闭卷回答：

### Q1

昨天 LangGraph ReAct 中分别是谁负责：

```text
决策是否调用 Tool
路由
真正执行 Tool
保存 Tool Result
重新让 LLM 总结
```

### Q2

为什么：

```text
ToolNode
↓
ToolMessage
↓
LLM
```

而通常不是：

```text
ToolNode
↓
END
```

### Q3

解释：

```text
State
Checkpoint
Checkpointer
thread_id
```

四者之间的关系。

### Q4

如果：

```text
thread_id = "A"
```

执行两次 invoke，第二次为什么可能知道第一次发生了什么？

### Q5

如果换成：

```text
thread_id = "B"
```

为什么不应该读到 A 的历史？

---

## 2｜【白天今日原文】

继续 **HelloAgents 第 6 章框架开发实践 → LangGraph 部分**。

今天不追求再看大量章节。

### 【必看】

重新定位：

```text
State
Checkpoint
Checkpointer
thread_id
```

尤其观察：

```python
compile(checkpointer=...)
```

和：

```python
config = {
    "configurable": {
        "thread_id": "..."
    }
}
```

### 【重点】

带着三个问题读：

```text
① Graph 在什么时候保存 State？

② Checkpointer 保存的到底是什么？

③ 下一次相同 thread_id 的 invoke
   为什么可以继续之前的状态？
```

### 【略看】

```text
get_state()
checkpoint metadata
历史 checkpoint
```

今天知道能查看即可。

### 【暂不看】

```text
PostgresSaver
Redis
Store
Long-term Memory
Human-in-the-loop
Multi-Agent
```

不要因为看到 Memory 就顺手学下去。

---

## 3｜【白天理解目标①】State ≠ Checkpoint

今天必须讲清：

```text
State
=
Graph 当前正在流动的数据
```

例如：

```text
{
    "messages": [...]
}
```

而：

```text
Checkpoint
=
某个时刻保存下来的 State Snapshot
```

理解成：

```text
Graph 执行

State 0
↓
Node
↓
State 1
↓
Node
↓
State 2
```

Checkpointer 可以留下：

```text
Checkpoint(State 0)

Checkpoint(State 1)

Checkpoint(State 2)
```

所以：

> State 是当前状态；Checkpoint 是状态快照。

---

## 4｜【白天理解目标②】thread_id 不是 Memory 本身

例如：

```text
thread_id = "chat_001"
```

不要理解为：

> 这里保存了记忆。

更准确是：

> **告诉 Checkpointer：这次执行属于哪一条状态时间线。**

脑中画：

```text
Thread 001

Checkpoint 1
↓
Checkpoint 2
↓
Checkpoint 3
```

另一边：

```text
Thread 002

Checkpoint 1
↓
Checkpoint 2
```

因此：

```text
thread_id
=
定位哪条执行历史
```

---

## 5｜【白天理解目标③】Persistence 怎么接进昨天的 Tool Agent

昨天：

```text
HumanMessage
↓
LLM
↓
ToolNode
↓
ToolMessage
↓
LLM
↓
Final
```

今天增加：

```text
HumanMessage
↓
State
↓
LLM
↓
ToolNode
↓
ToolMessage
↓
LLM
↓
Final
↓
Checkpointer
↓
Checkpoint
```

下一次：

```text
same thread_id
↓
恢复已有 State
↓
加入新的 HumanMessage
↓
继续 Graph
```

核心结论：

> **Persistence 不负责 Agent 推理。**

它解决：

> **Graph State 跨执行保存和恢复。**

---

## 6｜【白天理解目标④】Short-term Memory 边界

今天第一次开始碰到“记忆”，但不要把所有东西混成 Memory。

现在做的是：

```text
同一个 thread

messages
↓
checkpoint
↓
下一次 invoke
↓
继续使用
```

这更接近：

> **会话级短期状态 / Thread-level persistence。**

以后真正学长期 Memory 时还会涉及：

```text
跨 thread
跨 conversation
用户长期信息
Store
检索
```

今天暂时不碰。

---

## 7｜【工程思维】

今天故意培养一个 Debug 顺序。

如果第二轮：

```text
刚才计算结果是多少？
```

Agent 回答：

```text
不知道
```

不要直接怪 LLM。

检查：

```text
① compile 有没有 checkpointer

↓

② invoke 有没有 config

↓

③ configurable 有没有 thread_id

↓

④ 两次是不是同一个 thread_id

↓

⑤ messages 有没有 add_messages

↓

⑥ get_state(config)
   能不能看到上一轮消息

↓

⑦ LLM 最终收到的 messages
   到底有哪些
```

这就是 Agent 开发里的状态链路排错。

---

## 8｜【Agent 开发面试表达】

今天练习 60 秒回答：

> LangGraph 怎么实现一个 Tool Agent 的多轮上下文？

你的回答至少应该自然出现：

```text
State
messages
Checkpointer
Checkpoint
thread_id
same thread
ToolMessage
```

重点仍然是：

> **讲数据流，不背 API。**

---

## 9｜【晚上代码预演】20 分钟

白天结束前，在纸上写：

```text
昨天 Tool Agent
↓
创建 Checkpointer
↓
compile(checkpointer)
↓
创建 config
↓
thread_id = A
↓
invoke 1
↓
保存 State
↓
invoke 2
↓
same thread
↓
恢复 State
```

然后回答：

```text
Checkpointer 在哪里创建？

什么时候传给 Graph？

thread_id 放在哪里？

same thread 如何测试？

different thread 如何测试？

怎么查看当前 State？
```

---

# B｜晚上约 2 小时

## 10｜【晚上目标】一个最小闭环

今天不要重写整个 Tool Agent。

直接在 Day 4 代码上加：

```text
InMemorySaver
+
checkpointer
+
thread_id
+
get_state
```

最终：

```text
Tool Agent
+
Persistence
```

---

## 11｜第一轮：允许查资料｜30 分钟

核心结构只需要恢复到：

```python
checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)
```

以及：

```python
config = {
    "configurable": {
        "thread_id": "001"
    }
}
```

API 拼写忘了可以查。

但是必须知道：

```text
checkpointer
→ compile
```

而：

```text
thread_id
→ invoke config
```

---

## 12｜第二轮：Same Thread Case｜25 分钟

第一次：

```text
thread_id = "001"

User：
计算 12 × 8
```

预期：

```text
LLM
↓
ToolNode
↓
96
↓
LLM
↓
Final
```

然后：

```text
thread_id = "001"

User：
把刚才的结果加 4
```

理想：

```text
读取之前 messages
↓
知道结果是 96
↓
再次 Tool Call
↓
100
```

这个 Case 是今天最重要的。

---

## 13｜第三轮：Thread Isolation｜20 分钟

现在只改：

```text
thread_id = "002"
```

问：

```text
把刚才的结果加 4
```

观察。

理想：

> Thread 002 不应该天然拥有 Thread 001 的上下文。

这就是：

```text
Thread Isolation
```

---

## 14｜第四轮：get_state｜15 分钟

调用：

```python
graph.get_state(config)
```

不要研究返回对象全部字段。

只找：

```text
messages
```

看看是否存在类似：

```text
HumanMessage
AIMessage(tool_call)
ToolMessage
AIMessage(final)
HumanMessage
AIMessage(tool_call)
ToolMessage
AIMessage(final)
```

然后自己解释：

> 为什么这些 Message 还在？

---

## 15｜【验证】今天不写 Pytest

完成三个手动 Case。

### Case A

```text
Thread A

12 × 8 等于多少？
↓
刚才结果是多少？
```

验证：

```text
same thread 可以延续
```

### Case B

```text
Thread B

刚才结果是多少？
```

验证：

```text
different thread 隔离
```

### Case C

```text
get_state(Thread A)
```

验证：

```text
上一轮 messages 确实存在
```

如果还有时间再跑：

```text
Thread A：

12 × 8
↓
把结果 + 4
↓
再乘 2
```

观察：

```text
96
↓
100
↓
200
```

---

## 16｜【闭卷小测】

### Agent 概念题 1

为什么：

```text
State ≠ Checkpoint
```

？

### Agent 概念题 2

为什么：

```text
thread_id
```

不能直接等同于：

```text
Memory
```

？

### Agent 概念题 3

为什么：

```text
Tool Agent + Checkpointer
```

可以跨 invoke 保留上下文，但：

```text
不同 thread_id
```

又能够隔离？

### 代码 / 流程题

闭卷补：

```text
User
↓
State
↓
LLM
↓
ToolNode
↓
New State
↓
________
↓
Checkpoint

下一次 invoke
↓
________
↓
恢复已有 State
↓
继续 Graph
```

并解释：

```text
Checkpointer
thread_id
```

分别应该出现在哪里。

---

# 17｜【今日完成标准】

今天必须达到：

### 理论

脱离原文能解释：

```text
State
Checkpoint
Checkpointer
thread_id
```

以及：

> Persistence 为什么能让 Agent 跨 invoke 延续状态。

### 代码

关闭完整教程后，能在 Day 4 Tool Agent 上自己补：

```text
InMemorySaver
compile(checkpointer=...)
configurable.thread_id
```

允许定点查询 API 名。

### 验证

必须跑通：

```text
Same Thread      ✅
Different Thread ✅
get_state        ✅
```

三项完成：

> **LangGraph Day 5 第一阶段过关。**

---

# 当前路线

```text
经典 Agent Pattern

Tool Calling                    ✅
ReAct                           ✅
Plan-and-Solve                  ✅
Reflection                      ✅

LangGraph

Day 1
Graph / Node / Edge / Cycle     ✅

Day 2
State / Partial Update / Reducer✅

Day 3
Checkpoint / Checkpointer       ✅

Day 4
ToolNode / tools_condition      ✅

Day 5
Tool Agent + Persistence        ← 今天

             ↓

后续
Memory 边界
↓
Human-in-the-loop
↓
完整 Agent Workflow
↓
Agent Eval
↓
真实 Agent 项目 V1
```

---

## 状态反馈

完成后回复以下任一种：

- `完成`
- `未完成 + 卡点`
- `暂停`
- `今天忙 + 可用时间`
