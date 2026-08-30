# HelloAgents｜LangGraph Day 3 独立学习卡：Persistence / Checkpointer / thread_id

**当前理论进度：** Tool Calling 已完成 → ReAct 已完成 → Plan-and-Solve 第一阶段已完成 → Reflection 第一阶段已完成 → LangGraph Day 1 / Day 2 已完成  
**当前 LangGraph 进度：** Day 1 已理解 `Node / Edge / Conditional Edge / Cycle / compile / invoke / stream`；Day 2 已学习 `State / Partial Update / Reducer / MessagesState`  
**当前代码进度：** 已能理解并跟踪 Graph 数据流；今天先验收 Day 1 / Day 2，再进入 Persistence，晚上要求跑通一个最小 Checkpointer 闭环  
**今天主题：** LangGraph Day 3｜从“State 怎么变化”进入“State 怎么保存和恢复”  
**今日模式：** 周日「前置验收 + 新理论 + 最小代码闭环」模式；如果前测明显不过关，今天不继续扩大理论债

你 LangGraph Day 2 的核心已经从“Graph 怎么走”推进到了“Graph 每走一步，State 到底怎么变化”：

```text
State
↓
Partial Update
↓
Reducer
↓
New State
↓
Conditional Edge
```

Day 2 原计划的下一站就是：

```text
Persistence
↓
Checkpointer
↓
thread_id
↓
Checkpoint
↓
State 恢复
↓
Memory 与 State 的区别
```

---

# 一、今天先不学新内容：前置验收｜25～35 分钟

今天先正式检验前面到底掌握了多少。

**全程闭卷。**

不要看昨天的 Markdown，不要搜索 API。

把答案直接记下来，学完也可以发给我，我会按：

```text
真懂
大方向对但不够准确
概念混淆
```

逐题给你验收。

---

## 第一组｜经典 Agent Pattern

### Q1｜Tool Calling

LLM 输出：

```text
Action: Search[LangGraph]
```

从这个输出开始，到结果重新被 LLM 使用，中间的数据流是什么？

要求至少画到：

```text
LLM Response
↓
?
↓
?
↓
Tool
↓
?
↓
下一轮 LLM
```

---

### Q2｜ReAct

为什么：

```text
Tool Result
```

不能只是：

```python
print(result)
```

而通常需要成为：

```text
Observation
↓
History / Context
↓
下一轮 LLM
```

？

---

### Q3｜Plan-and-Solve

假设：

```text
Step 1：查询深圳天气
Step 2：根据天气给出穿衣建议
```

为什么 Executor 执行 Step 2 时需要 `context / previous_results`？

---

### Q4｜Reflection

下面两个流程有什么本质区别？

```text
A:
LLM → Answer
LLM → Answer
```

和：

```text
B:
Generator → Draft
Reflector → Feedback
Generator → Revision
```

---

# 二、LangGraph Day 1 / Day 2 前测

这部分更重要。

Day 2 的收口标准包括：

```text
能解释 State Schema
能解释 Partial Update
能解释 Reducer
能解释 Conditional Edge
能闭卷画出一个带循环的 Graph
```

---

## Q5｜State vs Edge

一句话分别解释：

```text
State
Edge
```

然后回答：

> Edge 会不会负责把 `result` 从 Node A 传给 Node B？

---

## Q6｜Partial State Update

看到：

```python
def node(state):
    return {"result": "done"}
```

回答三个问题：

1. Node 读取的是什么？
2. `{"result": "done"}` 是完整 State 吗？
3. LangGraph 接下来会怎么处理它？

---

## Q7｜Reducer

State：

```python
class State(TypedDict):
    logs: Annotated[list[str], operator.add]
```

当前：

```text
logs = ["planner"]
```

Node 返回：

```text
{"logs": ["executor"]}
```

最终 `logs` 应该是什么？

然后解释：

> 为什么不是直接覆盖？

---

## Q8｜Reducer 对比

解释：

```text
operator.add
```

和：

```text
add_messages
```

的区别。

提示：不要只回答“都是相加”。

Day 2 的核心区别是：

```text
operator.add
→ 通用累积

add_messages
→ 理解 Message 语义的消息 Reducer
```

---

## Q9｜Conditional Edge

```python
def route(state):
    if state["passed"]:
        return "end"
    return "retry"
```

回答：

> `route()` 属于执行业务逻辑的普通 Node，还是控制流逻辑？

以及：

> Conditional Edge 最关键依赖的是什么？

---

## Q10｜完整数据流

闭卷把下面补完整：

```text
Input
↓
State Schema
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
Next Node / END
```

如果这一题能顺畅回答，说明 Day 2 主线基本是真的通了。

---

# 三、前测判定

不用追求 10 / 10。

今天这样判断：

```text
8～10 题比较确定
→ Day 2 收口，正常进入 Day 3

6～7 题
→ 可以学 Day 3，但晚上必须先重写 Day 2 Graph

≤5 题
→ 今天暂停 Day 3
→ 先恢复 State / Update / Reducer / Routing
```

尤其以下四题属于核心题：

```text
Q5 State vs Edge
Q6 Partial Update
Q7 Reducer
Q9 Conditional Edge
```

这四个如果混乱，即使总分高，也不能算 Day 2 完全收口。

---

# 四、【白天今日原文】LangGraph Day 3

## HelloAgents 定位

继续：

> HelloAgents 第 6 章 → 6.5「框架四：LangGraph」

前面已经学过：

> 6.5.1 LangGraph 的结构梳理

以及：

> 6.5.2 三步问答助手

这两个部分是 Day 1 / Day 2 的主要落点。今天不再重复精读。

---

## 今天的新主线

```text
Persistence
↓
Checkpointer
↓
Checkpoint
↓
thread_id
↓
恢复同一个 Thread 的 State
↓
State / Checkpoint / Memory 区分
```

建议：

> HelloAgents 6.5：继续跟着相关 LangGraph 案例走。

同时用 LangGraph Persistence 官方文档补这个概念，因为这一块 API 和命名比经典 Pattern 更容易随着版本变化。

学习时抓住这个核心：

```text
Graph 编译时加入 checkpointer
↓
执行过程中保存 Graph State 的 checkpoint
↓
checkpoint 按 thread 组织
↓
调用带 checkpointer 的 Graph 时，通过配置提供 thread_id
```

---

# 五、【今天必看】

今天只吃透：

```text
Persistence
Checkpointer
Checkpoint
thread_id
InMemorySaver
StateSnapshot（知道是什么即可）
```

重点观察：

```text
Graph 执行

Node A
↓
State A
↓
Checkpoint

Node B
↓
State B
↓
Checkpoint

Node C
↓
State C
↓
Checkpoint
```

---

# 六、【今天暂不深挖】

今天不要扩散到：

```text
PostgresSaver
SqliteSaver 工程配置
Store
长期用户画像
Time Travel 具体 API
Human-in-the-loop
Interrupt
Durable Execution
复杂 Memory 架构
```

这些以后会再次出现。

今天的目标不是“学会所有持久化”。

而是：

> 第一次真正理解 Graph 为什么运行结束以后还能找回之前的 State。

---

# 七、【白天理解目标 1】State ≠ Checkpoint

这个是今天最容易混淆的地方。

不要记成：

```text
State = Memory
```

今天要真正把它拆开：

```text
State
≠
Checkpoint
≠
Long-term Memory
```

---

## State

可以先理解成：

> Graph 当前运行这一刻，各 Node 共享和更新的数据。

例如：

```text
messages
plan
result
retry_count
```

---

## Checkpoint

可以先理解成：

> 某一个执行时刻的 State Snapshot。

也就是：

```text
运行中的 State
       ↓
某个时间点拍一张快照
       ↓
Checkpoint
```

---

## Checkpointer

负责：

```text
State
↓
保存 Checkpoint

以及：

thread_id
↓
找到对应 Checkpoint
↓
恢复 State
```

---

# 八、【白天理解目标 2】thread_id

这是今天最重要的新变量。

假设：

```text
用户 A 的会话
thread_id = "A"

用户 B 的会话
thread_id = "B"
```

Checkpointer 保存：

```text
A
↓
Checkpoint 1
Checkpoint 2
Checkpoint 3

B
↓
Checkpoint 1
Checkpoint 2
```

所以：

> thread_id 不是 State 本身。

它更像：

> “我要读取 / 保存哪一条执行线程的 State 历史？”

---

# 九、【白天理解目标 3】Persistence 到底解决什么？

思考以前：

```python
result = graph.invoke(...)
```

程序执行结束。

如果没有 Persistence：

```text
下一次 invoke
↓
新的执行
```

Graph 本身不会凭空知道：

> “上次这个用户聊到哪里了？”

引入：

```text
Checkpointer
+
thread_id
```

之后开始能够建立：

```text
第一次调用

thread_id = 001
↓
State
↓
Checkpoint


第二次调用

thread_id = 001
↓
找到之前的 Checkpoint
↓
继续使用这条 Thread 的状态
```

这开始为：

```text
多轮 Agent
Memory
Human-in-the-loop
失败恢复
```

提供基础。

---

# 十、【工程思维】Memory 到底是什么？

今天不要直接说：

```text
Memory = State
```

先建立三层：

```text
State
当前 Workflow 的数据

        ↓ 保存

Checkpoint
某时刻 State 的快照

        ↓ 按 thread_id 组织

Persistence
让 State 可以跨执行恢复
```

现代 LangGraph 还进一步区分：

```text
Checkpointer
→ Thread 范围的状态持久化

Store
→ 跨 Thread 的长期信息
```

例如用户偏好、事实等更适合 Store，而不是简单塞进当前线程 checkpoint。

今天只知道这个边界，不写 Store。

---

# 十一、【Agent 开发面试表达】15 分钟

闭卷回答：

> LangGraph 的 Checkpointer 是干什么的？

不允许回答：

> “保存数据。”

要求至少说到：

```text
Graph State
Checkpoint
thread_id
恢复
多轮执行
```

然后再回答：

> State 和 Memory 是一回事吗？

要求能够区分：

```text
当前执行状态
vs
被持久化保存 / 跨执行使用的信息
```

---

# 十二、【晚上代码预演】15 分钟

先在纸上设计：

```text
State:
messages
```

然后：

```text
START
↓
chat_node
↓
END
```

第一次：

```text
thread_id = "001"

Human:
你好，我叫小明
```

第二次：

```text
thread_id = "001"

Human:
我叫什么？
```

然后再想：

```text
thread_id = "002"
```

重新问：

```text
我叫什么？
```

为什么结果应该和 `"001"` 不同？

今天先把这个实验想明白。

---

# 十三、【晚上目标】约 2 小时

今天分两关。

## 第一关｜Day 2 闭卷验收｜30～40 分钟

从空文件写一个：

```text
START
↓
planner
↓
executor
↓
checker
↓
Conditional Edge
↙          ↘
retry       END
```

State 至少：

```text
plan
result
retry_count
passed
logs
```

要求自己出现：

```text
TypedDict
Annotated
Reducer
Partial Update
add_conditional_edges
stream
```

不需要背 API 参数顺序。

---

## 第二关｜Day 3 最小 Persistence｜45～60 分钟

只写最小：

```text
StateGraph
↓
chat_node
↓
END
```

然后加入：

```text
InMemorySaver
```

Graph 编译时配置 checkpointer，并在调用时给：

```python
config = {
    "configurable": {
        "thread_id": "001"
    }
}
```

目标不是 LLM 答得多聪明。

而是观察：

```text
第一次 invoke
↓
Checkpoint

第二次 invoke
↓
相同 thread_id
↓
State 能继续
```

写代码前，按你本地安装的 LangGraph 版本确认导入路径和示例写法；本学习卡只强调今天必须掌握的控制流和状态恢复关系。

---

# 十四、【验证】今天最值得做的 3 个 Case

## Case 1｜同一个 thread

```text
thread_id = "001"

invoke #1
↓
加入 message A

invoke #2
↓
加入 message B
```

检查第二次 State 是否包含前面的信息。

---

## Case 2｜不同 thread

```text
thread_id = "002"
```

重新运行。

检查：

> `"002"` 为什么不能自动继承 `"001"` 的 State？

---

## Case 3｜查看状态

如果当前版本 API 顺畅，可以尝试：

```text
graph.get_state(config)
```

观察最新 State Snapshot。

不要求今天深入 `get_state_history()`。

---

# 十五、【今天的 Debug 路线】

以后 Persistence 出错，不要先怀疑 LLM。

按：

```text
① compile 时有没有 checkpointer？
↓
② invoke 时有没有 config？
↓
③ thread_id 是什么？
↓
④ 两次调用 thread_id 是否一致？
↓
⑤ State 字段是否正确 Update？
↓
⑥ Reducer 是否正确合并？
↓
⑦ Checkpoint 中到底保存了什么？
```

这已经非常接近真实 Agent 工程 Debug 思路。

---

# 十六、【今日闭卷小测】

今天结束后再答。

## Agent 概念题 1

为什么：

```text
State ≠ Checkpoint
```

？

---

## Agent 概念题 2

`thread_id` 是 Agent State 的某个普通业务字段吗？它主要解决什么问题？

---

## Agent 概念题 3

为什么 Checkpointer 能为多轮 Agent / Human-in-the-loop / 错误恢复提供基础？

---

## 代码 / 流程题

有：

```text
thread_id = A
```

执行：

```text
State 0
↓
Node 1
↓
State 1
↓
Node 2
↓
State 2
```

请自己画出：

```text
Checkpoint
Checkpointer
thread_id
```

分别应该出现在什么位置。

再增加：

```text
thread_id = B
```

解释 A 和 B 的 State 为什么不会混在一起。

---

# 十七、【今日完成标准】

## 前面内容验收

今天如果能够比较稳地回答：

```text
Tool Calling 数据流
ReAct Observation
Plan-and-Solve Context
Reflection Feedback
State
Partial Update
Reducer
Conditional Edge
```

说明前面的知识已经开始连成体系。

---

## LangGraph Day 2 收口

要求：

```text
能解释 State Schema
+
能解释 Partial Update
+
能解释 Reducer
+
能解释 operator.add / add_messages
+
能解释 Conditional Edge 如何读 State
+
能手画一个 Cycle
```

达到：

> LangGraph Day 2 正式收口

---

## LangGraph Day 3 收口

今天不要求生产级 Persistence。

达到：

```text
不看笔记能解释：

State
Checkpoint
Checkpointer
thread_id

+
跑通相同 thread_id 的两次 invoke

+
换 thread_id 后状态隔离

+
知道 State ≠ Checkpoint ≠ Long-term Memory
```

即可：

> LangGraph Day 3 第一阶段完成

---

# 十八、接下来路线

```text
LangGraph Day 1
Graph 怎么走
已完成

↓

LangGraph Day 2
Graph 每一步的数据怎么变
已完成

↓

LangGraph Day 3
Graph 的 State 怎么保存和恢复
← 今天

↓

下一阶段

ToolNode
↓
tools_condition
↓
LLM Node
↓
Tool Node
↓
Tool Result 回写 messages
↓
真正用 LangGraph 重构 ReAct

↓

再往后

Memory
Human-in-the-loop
Agent Eval
Multi-Agent
真实项目 V1
```

你现在已经开始接近一个很重要的节点：

> 前面手写 ReAct 时，你是在理解 Agent 为什么会循环；  
> LangGraph Day 1 / Day 2 是理解这个循环如何被 Graph 和 State 管理；  
> Day 3 开始理解 Agent 为什么可以跨多次执行继续运行。

今天先把最上面的 Q1～Q10 闭卷前测做掉。你可以直接把答案按 `1～10` 发出来，后续验收时只逐题判断，不直接重讲整章，重点找出是真懂还是“看代码时觉得懂”的位置。

**状态反馈：** `完成` / `未完成 + 卡点` / `暂停` / `今天忙 + 可用时间`
