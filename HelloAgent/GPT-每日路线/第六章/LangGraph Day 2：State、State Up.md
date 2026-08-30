# LangGraph Day 2：State、State Update、Reducer 与 MessagesState

> 学习阶段：LangGraph 第 2 天
> 主线目标：从“会搭图”进入“看懂 State 如何在图里流动”
> 对应 HelloAgents：**第六章 6.5 LangGraph**，重点复习 **6.5.1 LangGraph 的结构梳理**，主学 **6.5.2 三步问答助手中的全局状态与节点更新**
> 今日收口标准：**能脱离教程讲清 Node → State Update → Reducer → Conditional Edge 的完整数据流，并能手撸一个带循环的小型 StateGraph。**

***

## 0. Day 1 已完成内容

昨天已经掌握：

* Node
* Edge
* Conditional Edge
* 循环边
* `compile()`
* `invoke()`
* `stream()`

所以今天不再继续死磕“图怎么连”，而是进入 LangGraph 真正重要的第二层：

```text
图结构 = 控制流
State   = 数据流
```

今天最重要的一句话：

> **Edge 决定下一步去哪里；State 决定下一步能看到什么数据。**

***

# 1. 今天的学习地图

```text
State Schema
    ↓
Node 读取 State
    ↓
Node 返回 Partial State Update
    ↓
LangGraph 合并 Update
    ↓
Reducer 决定某些字段“怎么合并”
    ↓
下一个 Node 读取新 State
    ↓
Conditional Edge 根据 State 路由
    ↓
继续执行 / 循环 / END
```

今天按下面顺序学习：

1. State 到底是什么
2. `TypedDict` 为什么常用于 State Schema
3. Node 如何读取 State
4. Node 为什么返回“局部更新”
5. 默认更新规则：覆盖
6. Reducer：解决“怎么合并”
7. `Annotated`
8. `add_messages`
9. `MessagesState`

7.8.9、小结

名称	本质	在 LangGraph 的角色

Annotated	Python 标准库语法	给类型挂"元数据"，LangGraph 用第二个参数指定 Reducer

add\_messages	LangGraph 的 Reducer 函数	定义消息如何合并（追加 + id 去重 + 自动转换）

MessagesState	LangGraph 预置 State 类	已内置 Annotated\[list, add\_messages] 的 messages，继承即用

10. State + Conditional Edge
11. 手撸一个不接 LLM 的循环 Graph
12. 闭卷验收

***

# 2. State 到底是什么？

## 2.1 最简单的理解

LangGraph 中的 State 可以理解为：

> **整个工作流共同维护的一份共享数据。**

例如：

```python
from typing_extensions import TypedDict

class AgentState(TypedDict):
    task: str
    plan: str
    result: str
    passed: bool
```

假设当前 State：

```python
{
    "task": "学习 LangGraph",
    "plan": "",
    "result": "",
    "passed": False
}
```

不同 Node 可以分别负责不同字段：

```text
planner
    ↓
写入 plan

executor
    ↓
读取 plan
写入 result

checker
    ↓
读取 result
写入 passed
```

所以不要把 State 理解成“某一个 Node 的参数”。

它更像：

```text
整个 Graph 的共享白板
```

每个 Node：

```text
进来先看白板
→ 做自己的工作
→ 把新结果写回白板
→ 下一个 Node 再看更新后的白板
```

***

# 3. State Schema：为什么用 TypedDict？

最常见的写法：

```python
from typing_extensions import TypedDict

class AgentState(TypedDict):
    task: str
    plan: str
    result: str
    passed: bool
```

这里不是在真正创建 State 数据。

它是在定义：

> **这张图允许维护哪些字段，以及这些字段是什么类型。**

可以理解成数据库表结构：

```text
AgentState
├── task: str
├── plan: str
├── result: str
└── passed: bool
```

真正运行时的数据可能是：

```python
initial_state = {
    "task": "学习 LangGraph",
    "plan": "",
    "result": "",
    "passed": False
}
```

***

# 4. Node 如何读取 State？

Node 本质仍然是普通 Python 函数：

```python
def planner(state: AgentState):
    task = state["task"]

    plan = f"先理解 {task}，然后完成练习"

    return {
        "plan": plan
    }
```

数据流：

```text
当前 State
    ↓
planner(state)
    ↓
读取 state["task"]
    ↓
执行 planner 自己的逻辑
    ↓
return {"plan": ...}
```

注意：

```python
return {
    "plan": plan
}
```

这里没有把 `task`、`result`、`passed` 全部返回。

为什么？

因为 LangGraph 的 Node 推荐表达成：

```text
State → Partial State Update
```

也就是：

> Node 只告诉 Graph：“我这一步修改了哪些字段。”

***

# 5. 今天最重要的概念：State Update

假设进入 Node 前：

```python
state = {
    "task": "学习 LangGraph",
    "plan": "",
    "result": "",
    "passed": False
}
```

planner：

```python
def planner(state: AgentState):
    return {
        "plan": "先理解 State，再写代码"
    }
```

LangGraph 得到的不是一份“完整新 State”，而是一份：

```python
update = {
    "plan": "先理解 State，再写代码"
}
```

然后框架负责把 Update 应用到当前 State。

结果相当于：

```python
{
    "task": "学习 LangGraph",
    "plan": "先理解 State，再写代码",
    "result": "",
    "passed": False
}
```

所以你需要建立：

```text
Node Return
≠ 整个 Graph State

Node Return
= 对 State 的本次更新
```

***

# 6. 为什么不建议直接原地修改整个 state？

你可能会本能写：

```python
def planner(state):
    state["plan"] = "xxx"
    return state
```

学习阶段建议优先写成：

```python
def planner(state):
    return {
        "plan": "xxx"
    }
```

原因是后者的职责非常清晰：

```text
输入：当前 State
输出：本 Node 产生的 State Update
```

它让你更容易：

* 看出每个 Node 修改了什么
* 调试 State
* 使用 Reducer
* 处理并行 Node
* 理解 Checkpoint
* 理解后面的 Memory
* 理解 LangGraph 的执行模型

### 今天记忆：

```text
Node 不负责管理整份 State。
Node 负责产生自己的 Update。
LangGraph 负责把 Update 合并进 State。
```

***

# 7. 默认 State 更新：覆盖

先看：

```python
class State(TypedDict):
    count: int
```

Node A：

```python
def node_a(state):
    return {
        "count": 1
    }
```

Node B：

```python
def node_b(state):
    return {
        "count": 2
    }
```

在普通顺序更新中：

```text
count = 0
   ↓
Node A
   ↓
count = 1
   ↓
Node B
   ↓
count = 2
```

也就是说，对于没有 Reducer 的普通字段，新的更新通常表现为：

```text
旧值 → 被新值替换
```

这对下面字段很合理：

```python
current_step: str
final_answer: str
passed: bool
retry_count: int
```

因为它们通常只需要当前最新值。

***

# 8. 问题来了：List 怎么办？

假设：

```python
class State(TypedDict):
    logs: list[str]
```

初始：

```python
logs = ["START"]
```

Node A：

```python
return {
    "logs": ["planner finished"]
}
```

如果只是覆盖：

```text
原来：
["START"]

更新后：
["planner finished"]
```

`START` 没了。

但我们真正想要：

```python
[
    "START",
    "planner finished"
]
```

这就是 Reducer 要解决的问题。

***

# 9. Reducer 是什么？

一句话：

> **Reducer 决定某个 State 字段收到新 Update 时，旧值和新值应该怎么合并。**

逻辑：

```text
old_value
    +
new_value
    ↓
Reducer
    ↓
merged_value
```

Reducer 的核心可以理解成：

```python
def reducer(old_value, new_value):
    return merged_value
```

***

# 10. 第一个 Reducer：operator.add

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
    logs: Annotated[list[str], operator.add]
```

这里：

```python
Annotated[list[str], operator.add]
```

可以先粗暴理解为：

```text
logs 是 list[str]

并且：

每次 logs 收到新更新时，
使用 operator.add 合并旧值和新值。
```

例如：

```text
旧值：
["START"]

新 Update：
["planner finished"]

operator.add

结果：
["START", "planner finished"]
```

所以 Node：

```python
def planner(state):
    return {
        "logs": ["planner finished"]
    }
```

不需要自己：

```python
state["logs"].append(...)
```

Reducer 会负责合并。

***

# 11. Annotated 到底是什么？

先不要把 Python 类型系统钻得太深。

今天你只需要理解：

```python
Annotated[字段类型, reducer]
```

LangGraph 会读取这个额外信息。

例如：

```python
logs: Annotated[list[str], operator.add]
```

拆开：

```text
list[str]
    ↓
字段的数据类型

operator.add
    ↓
这个字段收到 Update 时的合并规则
```

记忆：

```text
TypedDict = State 有哪些字段
Annotated = 某字段还有额外更新规则
Reducer   = 具体怎么合并
```

***

# 12. 普通字段 vs Reducer 字段

```python
class State(TypedDict):
    task: str
    retry_count: int
    logs: Annotated[list[str], operator.add]
```

可以这样理解：

| **字段**        | **更新思路**     |
| ------------- | ------------ |
| `task`        | 新值覆盖旧值       |
| `retry_count` | Node 算出新值后覆盖 |
| `logs`        | 新列表追加到旧列表    |

例如：

```python
return {
    "retry_count": state["retry_count"] + 1,
    "logs": ["retry + 1"]
}
```

假设之前：

```python
{
    "retry_count": 0,
    "logs": ["START"]
}
```

更新后：

```python
{
    "retry_count": 1,
    "logs": [
        "START",
        "retry + 1"
    ]
}
```

注意两种字段的更新策略不同。

***

# 13. 为什么 Agent 特别需要 Reducer？

Agent 中经常有：

```text
HumanMessage
AIMessage
ToolMessage
AIMessage
ToolMessage
AIMessage
...
```

这些历史消息一般不能每次覆盖。

否则：

```text
用户消息
   ↓
LLM 消息覆盖掉用户消息
   ↓
Tool 消息再覆盖掉 LLM 消息
```

最后模型就没有历史上下文了。

所以 Agent 的 messages 本质上特别适合：

```text
累积式 State
```

***

# 14. add\_messages：专门处理 Message 的 Reducer

LangGraph 提供了：

```python
from langgraph.graph.message import add_messages
```

State：

```python
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

Node：

```python
def chatbot(state):
    return {
        "messages": [
            ("assistant", "你好")
        ]
    }
```

`add_messages` 会把新消息合并进已有 messages。

***

# 15. add\_messages 不只是简单的 list +

为什么不直接：

```python
operator.add
```

而要：

```python
add_messages
```

因为 Message 有自己的语义。

当前 LangGraph 中，`add_messages` 会：

* 合并旧消息和新消息
* 通常将新消息追加进去
* 如果新消息与已有消息拥有相同 ID，则可以更新对应消息
* 处理 LangChain Message 类型/部分消息简写

所以：

```text
operator.add
```

更像：

```text
普通 List 拼接
```

而：

```text
add_messages
```

更像：

```text
懂 Message 语义的专用 Reducer
```

***

# 16. MessagesState

因为：

```python
messages: Annotated[list, add_messages]
```

实在太常用了，LangGraph 已经提供：

```python
from langgraph.graph import MessagesState
```

最简单：

```python
class State(MessagesState):
    retry_count: int
    passed: bool
```

它可以理解成你已经拥有：

```python
messages
```

这个字段，并且它已经配置好了 Message Reducer。

你再添加自己的业务字段：

```text
State
├── messages
├── retry_count
└── passed
```

***

# 17. 今天把 ReAct 和 LangGraph 串起来

你之前手撸 ReAct 时，大致是：

```text
用户问题
   ↓
LLM
   ↓
Action Parser
   ↓
ToolExecutor
   ↓
Observation
   ↓
再次回到 LLM
```

以前你可能通过：

```python
while ...
history.append(...)
if ...
```

维护上下文与循环。

换到 LangGraph：

```text
messages State
      ↓
Agent Node
      ↓
Conditional Edge
   ↙           ↘
Tool Node      END
   ↓
messages State
   ↓
Agent Node
```

对应关系：

| **之前手撸 ReAct**     | **LangGraph**              |
| ------------------ | -------------------------- |
| `while`            | Graph Cycle                |
| `if`               | Conditional Edge           |
| history            | State / messages           |
| `history.append()` | Reducer / `add_messages`   |
| LLM 调用             | Agent Node                 |
| ToolExecutor       | Tool Node                  |
| Observation        | ToolMessage / State Update |
| 最大步长               | Graph 执行限制 / 自定义 State 控制  |

这就是为什么你之前手撸 ReAct 很重要。

你不是重新学一个完全不同的东西。

而是在学习：

> **LangGraph 如何把之前自己手写的 Agent Runtime 显式化、结构化。**

***

# 18. State + Conditional Edge

昨天你已经学了条件边。

今天需要升级理解：

> Conditional Edge 通常不是凭空判断，它读取的是 State。

例如：

```python
def route(state):
    if state["passed"]:
        return "end"
    else:
        return "retry"
```

数据流：

```text
checker
   ↓
return {"passed": True / False}
   ↓
LangGraph 更新 State
   ↓
route(state)
   ↓
读取新的 state["passed"]
   ↓
True  → END
False → executor
```

所以现在你应该把条件边理解为：

```text
State 驱动的控制流
```

***

# 19. 今天白天第一段练习：最简单 State Update

先不要接 LLM。

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    greeting: str


def greet(state: State):
    name = state["name"]

    return {
        "greeting": f"Hello, {name}"
    }


builder = StateGraph(State)

builder.add_node("greet", greet)

builder.add_edge(START, "greet")
builder.add_edge("greet", END)

app = builder.compile()

result = app.invoke({
    "name": "LangGraph",
    "greeting": ""
})

print(result)
```

你不要只看运行结果。

必须手动说一遍：

```text
1. invoke 创建初始 State
2. START
3. 进入 greet
4. greet 读取 name
5. greet 返回 greeting Update
6. LangGraph 将 greeting 写入 State
7. END
8. invoke 返回最终 State
```

### 验收

不看上面内容，自己讲一遍。

***

# 20. 第二段练习：Reducer

```python
import operator

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    logs: Annotated[list[str], operator.add]


def node_a(state: State):
    return {
        "logs": ["Node A finished"]
    }


def node_b(state: State):
    return {
        "logs": ["Node B finished"]
    }


builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

builder.add_edge(START, "A")
builder.add_edge("A", "B")
builder.add_edge("B", END)

app = builder.compile()

result = app.invoke({
    "logs": ["START"]
})

print(result)
```

你先不要运行。

先预测：

```python
{
    "logs": [
        "START",
        "Node A finished",
        "Node B finished"
    ]
}
```

然后再运行。

***

# 21. 思考题：去掉 Reducer 会发生什么？

把：

```python
logs: Annotated[list[str], operator.add]
```

改成：

```python
logs: list[str]
```

再次预测结果。

关键不是背答案，而是理解：

```text
有 Reducer：
旧 logs + 新 logs

没 Reducer：
新 logs 作为该字段的新值
```

***

# 22. 今日核心实战：Planner → Executor → Checker

今天晚上建议手撸这个，不接 LLM。

图：

```text
START
  ↓
planner
  ↓
executor
  ↓
checker
  ↓
conditional edge
 ↙             ↘
retry          END
  ↓
executor
```

这是一个非常小的：

```text
Plan → Execute → Check → Retry
```

Agent Workflow。

***

# 23. 完整代码

第一遍可以参考。

第二遍必须闭卷重写。

```python
import operator

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


# =========================
# 1. State
# =========================

class AgentState(TypedDict):
    task: str
    plan: str
    result: str
    retry_count: int
    passed: bool

    # 每个 Node 产生的新日志都会追加
    logs: Annotated[list[str], operator.add]


# =========================
# 2. Nodes
# =========================

def planner(state: AgentState):
    task = state["task"]

    plan = f"执行任务：{task}"

    return {
        "plan": plan,
        "logs": [f"planner: 生成计划 -> {plan}"]
    }


def executor(state: AgentState):
    plan = state["plan"]
    retry_count = state["retry_count"]

    # 模拟第一次执行失败，第二次成功
    if retry_count == 0:
        result = "执行失败：结果不完整"
    else:
        result = f"执行成功：已完成 {plan}"

    return {
        "result": result,
        "logs": [f"executor: {result}"]
    }


def checker(state: AgentState):
    result = state["result"]

    passed = "执行成功" in result

    update = {
        "passed": passed
    }

    if passed:
        update["logs"] = ["checker: 检查通过"]
    else:
        update["retry_count"] = state["retry_count"] + 1
        update["logs"] = ["checker: 检查失败，retry_count + 1"]

    return update


# =========================
# 3. Conditional Router
# =========================

def route_after_check(state: AgentState):
    if state["passed"]:
        return "end"

    if state["retry_count"] >= 2:
        return "end"

    return "retry"


# =========================
# 4. Build Graph
# =========================

builder = StateGraph(AgentState)

builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.add_node("checker", checker)

builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", "checker")

builder.add_conditional_edges(
    "checker",
    route_after_check,
    {
        "retry": "executor",
        "end": END
    }
)

app = builder.compile()


# =========================
# 5. Invoke
# =========================

initial_state = {
    "task": "学习 LangGraph State",
    "plan": "",
    "result": "",
    "retry_count": 0,
    "passed": False,
    "logs": []
}

result = app.invoke(initial_state)

print("\n最终 State：")
print(result)
```

***

# 24. 不运行代码，先自己追一次数据流

初始：

```python
retry_count = 0
passed = False
logs = []
```

### 第一步 planner

返回：

```python
{
    "plan": "...",
    "logs": ["planner..."]
}
```

新的 State：

```text
plan 更新
logs 追加
```

***

### 第二步 executor

读取：

```text
plan
retry_count = 0
```

所以第一次模拟失败：

```python
result = "执行失败：结果不完整"
```

***

### 第三步 checker

读取：

```text
result = 执行失败
```

所以：

```python
passed = False
retry_count = 1
```

然后：

```text
Conditional Edge
      ↓
route_after_check
      ↓
passed == False
retry_count < 2
      ↓
retry
      ↓
executor
```

***

### 第二次 executor

读取：

```text
retry_count = 1
```

所以成功：

```text
执行成功
```

checker：

```text
passed = True
```

route：

```text
end
↓
END
```

这就是一个真正的循环 Graph。

***

# 25. 用 stream 看 State Update

Day 1 你已经学过 `stream()`。

今天要换一个观察角度：

昨天：

> 我在看 Node 按什么顺序运行。

今天：

> 我要看每一个 Node 对 State 做了什么 Update。

可以先直接：

```python
for event in app.stream(initial_state):
    print(event)
```

观察：

```text
planner 返回了什么？
executor 返回了什么？
checker 返回了什么？
为什么又回 executor？
```

### 你应该重点盯这几个字段：

```text
plan
result
retry_count
passed
logs
```

***

# 26. 今天的 Debug 方法

以后遇到 LangGraph 错误，不要第一反应盯着 LLM。

先沿着 State 查：

```text
① 当前进入的是哪个 Node？
        ↓
② Node 读了 State 的哪些字段？
        ↓
③ 这些字段当前值是什么？
        ↓
④ Node 返回了什么 Update？
        ↓
⑤ Reducer 如何合并？
        ↓
⑥ 合并后的 State 是什么？
        ↓
⑦ Conditional Edge 读取了哪个字段？
        ↓
⑧ 为什么跳到这个 Node？
```

这套排错思路比：

```text
“为什么 Agent 又跑错了？”
```

有用得多。

***

# 27. 今天暂时不要深挖的内容

以下内容今天只需要知道名字：

* Checkpointer
* thread\_id
* InMemorySaver
* Persistence
* Human-in-the-loop
* ToolNode
* `tools_condition`
* Command
* Send
* Subgraph
* 并行 Graph
* Durable Execution

原因：

今天的核心依赖还没有打牢：

```text
State
→ Update
→ Reducer
```

如果现在同时碰 Memory / Checkpoint，很容易混成：

```text
State = Memory
```

这是错误的。

明天再区分：

```text
State
≠ Checkpoint
≠ Long-term Memory
```

***

# 28. 今天你必须会回答的 8 个问题

## Q1：State 是干什么的？

自己回答后再看：

> State 是 Graph 各节点共享的数据结构，用于保存执行过程中需要被后续节点读取和更新的信息。

***

## Q2：Edge 会不会负责传递业务数据？

核心：

> Edge 主要负责控制执行流向；Node 通过共享 State 获取和更新数据。

***

## Q3：Node 应该返回整个 State 吗？

更推荐的理解：

> Node 返回本次产生的 Partial State Update，由 LangGraph 将更新应用到 State。

***

## Q4：没有 Reducer 时更新通常是什么效果？

> 新 Update 成为该字段的新值，也就是更接近覆盖语义。

***

## Q5：Reducer 是什么？

> Reducer 定义旧值和新 Update 如何合并。

公式：

```text
Reducer(old_value, new_value)
        ↓
    merged_value
```

***

## Q6：为什么 messages 需要 Reducer？

> 因为 Agent 通常需要保留 HumanMessage、AIMessage、ToolMessage 等历史，而不是每一步都覆盖前面的消息。

***

## Q7：`operator.add` 和 `add_messages` 有什么区别？

```text
operator.add
→ 通用的数据拼接/累积

add_messages
→ 专门理解 Message 语义的消息 Reducer
```

***

## Q8：Conditional Edge 和 State 是什么关系？

> 条件边通常读取当前 State，根据其中的字段决定下一步执行哪个 Node。

***

# 29. 闭卷代码验收

今天晚上不要追求写复杂 Agent。

闭卷完成：

```text
State
 ↓
planner
 ↓
executor
 ↓
checker
 ↓
Conditional Edge
 ↙        ↘
retry     END
```

必须自己写出：

```python
TypedDict

Annotated
operator.add

StateGraph
START
END

add_node()
add_edge()
add_conditional_edges()

compile()
invoke()
stream()
```

但注意：

> 不要求把 API 参数位置一个字不差地背下来。

真正要求的是：

```text
你知道为什么需要它。
```

***

# 30. Day 2 收口标准

今天满足下面 5 条即可收口。

## Level 1：概念

看到：

```python
class State(TypedDict):
```

能说：

> 这是 Graph 的 State Schema。

***

## Level 2：数据流

看到：

```python
def node(state):
    return {"x": xxx}
```

能说：

> Node 读取当前 State，然后产生 `x` 字段的 Update。

***

## Level 3：Reducer

看到：

```python
logs: Annotated[list[str], operator.add]
```

能说：

> logs 的新 Update 不直接覆盖旧 logs，而是通过 reducer 合并。

***

## Level 4：路由

看到：

```python
def route(state):
```

能指出：

```text
route 读取 State
→ 返回路由结果
→ Conditional Edge 决定下一个 Node
```

***

## Level 5：闭卷手撸

不看教程可以写出：

```text
START
↓
Node A
↓
Node B
↓
Checker
↓
Conditional Edge
↙        ↘
循环      END
```

并能用 `stream()` 解释每一轮 State 是怎么变化的。

达到这里：

> **LangGraph Day 2 正式收口。**

***

# 31. 今天建议的学习节奏

## 白天：概念 + 代码预演

### 任务 A：10–15 分钟

复习 Day 1：

* Node
* Edge
* Conditional Edge
* Cycle
* compile
* invoke
* stream

不要重新学，只口述。

***

### 任务 B：40–60 分钟

重点学：

```text
State
State Schema
State Update
```

验收：

不看笔记解释：

```text
Node 为什么只 return 部分字段？
```

***

### 任务 C：40–60 分钟

重点学：

```text
Reducer
Annotated
operator.add
add_messages
MessagesState
```

验收：

自己举出：

```text
一个适合覆盖的字段
一个适合 reducer 的字段
```

例如：

```text
passed → 覆盖
logs → 累积
messages → add_messages
```

***

### 任务 D：30 分钟

把 Planner → Executor → Checker 的代码：

```text
只看
+
手动画数据流
```

白天不要求闭卷写完。

***

# 32. 晚上：代码债清零

## 第一轮：跟着写

完成：

```text
planner
executor
checker
conditional edge
```

跑通。

***

## 第二轮：关掉笔记

新建文件：

```text
langgraph_day2.py
```

闭卷重写。

如果卡住：

```text
先想结构
→ 再想 API
```

不要一忘 API 就立刻看答案。

***

## 第三轮：必须做一次修改

任选一个：

### 方案 A

增加：

```python
error_message: str
```

失败时记录原因。

### 方案 B

把：

```python
max_retry = 2
```

放进 State。

### 方案 C

新增：

```python
reviewer
```

形成：

```text
planner
↓
executor
↓
checker
↓
reviewer / retry
```

### 方案 D

把 `logs` 删除 Reducer，亲自观察区别。

推荐：

> **方案 D 必做，A/B/C 三选一。**

***

# 33. 今天不要追求“背代码”

今天真正要形成的是这一条脑内执行链：

```text
Graph 收到 Input
       ↓
创建 / 初始化 State
       ↓
进入 Node
       ↓
Node 读取 State
       ↓
Node 做自己的工作
       ↓
Node 返回 Partial Update
       ↓
Reducer 合并需要累积的字段
       ↓
形成新的 State
       ↓
Edge / Conditional Edge 决定下一 Node
       ↓
下一个 Node 读取新的 State
       ↓
循环直到 END
```

如果这一条能闭眼讲出来：

> 今天比多背 10 个 LangGraph API 更有价值。

***

# 34. 和 Agent 开发岗位真正相关的理解

面试里如果问：

> “LangGraph 的 State 有什么作用？”

不要只回答：

```text
“用于存数据。”
```

可以回答成：

> LangGraph 使用共享 State 作为节点之间的数据上下文。Node 读取当前 State 并返回局部状态更新，框架根据字段对应的更新策略或 Reducer 合并这些更新。控制流则由普通边或条件边根据当前 State 决定，因此业务数据流和执行控制流能够被显式拆开。

如果再问：

> “为什么 messages 要用 reducer？”

可以回答：

> 因为 Agent 的对话、工具调用与工具返回通常需要保留历史。如果直接覆盖会丢失上下文，因此 messages 通常使用 LangGraph 的 `add_messages` reducer 合并消息；它还可以根据消息 ID 更新已有消息，而不只是简单列表拼接。

这两个回答已经比：

```text
“我会 add_node/add_edge”
```

更接近真正使用 LangGraph 的开发者。

***

# 35. Day 3 预告

Day 2 收口以后，下一步：

```text
Persistence / Checkpointer
        ↓
thread_id
        ↓
Checkpoint
        ↓
同一个会话如何恢复 State
        ↓
Memory 与 State 到底有什么区别
```

你到时候会开始真正理解：

> 为什么 LangGraph 不只是一个“画流程图的库”。

***

# 36. 今日一句话总结

```text
Day 1：
我学会 Graph 怎么走。

Day 2：
我要学会 Graph 每走一步，数据到底怎么变。
```

今天抓住：

```text
State
→ Partial Update
→ Reducer
→ New State
→ Conditional Edge
```

LangGraph 的底层执行逻辑就开始真正连起来了。

***

# 参考定位

* **HelloAgents：第六章 6.5「框架四：LangGraph」**
  * `6.5.1 LangGraph 的结构梳理`
  * `6.5.2 三步问答助手`
* **LangGraph Python Reference**
  * `StateGraph`
  * `add_messages`
  * `MessagesState`

> 版本提示：LangGraph 仍在持续更新。学习时优先抓稳定概念——**共享 State、Partial State Update、Reducer、Graph Control Flow**；如果教程代码与当前 API 写法不同，以当前官方 Reference 为准。
