# HelloAgents｜Day 8 独立学习卡：Tool Runtime + ReAct Loop 周六代码补债

**当前理论进度：** Tool Calling ✅ → ReAct ✅ → Plan-and-Solve ✅ → Reflection ✅ → LangGraph 第一阶段基本完成 → Agent Framework 核心抽象已开始预习。  
**当前代码进度：** 理论明显领先于代码；今天优先补 `Tool / Registry / ToolExecutor / ReAct Agent Loop / History / max_steps`，暂停继续推进新章节。  
**今天：Day 8｜把早期 Tool Calling + ReAct 理论真正闭卷落成一个 Mini Agent Runtime。**  
**今日模式：周六代码补债模式。** 白天以复习、代码预演为主，晚上完成核心闭环。  
**职业主线：** AI Agent 开发；今天训练的是 Agent Runtime、控制流、错误恢复和 Trace，而不是测试开发。

---

## 0｜今天为什么必须回头补代码

你现在已经知道 LangGraph 可以写：

```text
LLM
↓
tools_condition
↓
ToolNode
↓
LLM
```

但如果只会框架 API，而自己写不出底层：

```text
LLM
↓
Action Parser
↓
ToolExecutor
↓
Registry
↓
Tool.execute
↓
Observation
↓
History
↓
LLM
```

对 Agent 的理解还是容易停留在“会使用框架”。

所以今天暂时不继续冲第 7 章。

目标只有一个：

> **不依赖 LangGraph，自己写出一个最小 ReAct Agent Runtime。**

---

# A｜白天 2–3 小时

## 【白天复习｜20–30 分钟】

禁止先看旧代码。

闭卷回答：

```text
Q1

Tool
ToolRegistry
ToolExecutor

分别只负责什么？
```

```text
Q2

LLM 输出：

Action: Search[深圳天气]

之后到真正执行 Search，
中间至少经过哪些组件？
```

```text
Q3

为什么 Tool 报错：

TimeoutError

更适合变成：

Observation: Error: TimeoutError

而不是：

raise → Agent Crash
```

```text
Q4

ReAct Loop 为什么必须存在：

max_steps
```

```text
Q5

History / Trace 在：

LLM → Action → Tool → Observation → LLM

里面到底保存什么？
```

今天仍然不要先找标准答案。

---

# 【白天今日原文】

今天不推进 HelloAgents 新章节。

回看 **HelloAgents Tool Calling + ReAct 对应章节**，并结合你昨天已经预习的第 7 章 Tool Framework 思路。

### 【必看】

重新定位 Tool Calling 中：

```text
Tool
Tool description
Tool execute
Tool Registry / Tool management
Tool Calling execution flow
```

但不要逐行抄代码。

只追：

```text
LLM 怎么知道有哪些 Tool？

LLM 怎么表达“我要调用哪个 Tool”？

Runtime 怎么找到 Tool？

Tool Result 怎么重新返回 Agent？
```

### 【重点】

重新看 ReAct：

```text
Thought
↓
Action
↓
Observation
↓
Thought
```

重点不是 Prompt。

重点观察：

```text
谁负责循环？

谁负责解析 Action？

谁负责执行？

Observation 怎么进入下一轮？
```

### 【重点对照】

把早期实现和 LangGraph 放一起：

```text
手写 Runtime              LangGraph

while loop          ↔     Graph Cycle

Action Parser       ↔     tool_calls / routing

ToolExecutor        ↔     ToolNode

History             ↔     State["messages"]

if finish           ↔     Conditional Edge → END

max_steps           ↔     recursion / termination control
```

今天一定要形成这种映射。

### 【略看】

```text
Prompt 示例
复杂 Tool
第三方搜索 API
输出美化
```

### 【暂不看】

```text
Memory
RAG
Multi-Agent
Agent Eval
新的 Framework API
```

今天严格停止增加理论债。

---

# 【白天理解目标①】Tool Runtime 的职责边界

闭卷画：

```text
                 Tool Runtime

LLM Action
    ↓
Action Parser
    ↓
ToolExecutor
    ↓
Registry
    ↓
Tool
    ↓
execute()
    ↓
Result / Error
    ↓
Observation
```

然后自己补职责：

```text
Tool
负责：________

Registry
负责：________

ToolExecutor
负责：________

Parser
负责：________
```

尤其想清：

> 为什么 ToolExecutor 不应该自己写 Search、Calculator、Weather 的业务逻辑？

如果新增：

```text
GitHubTool
EmailTool
DatabaseTool
```

理想情况应该是：

```text
Registry.register(new_tool)
```

而不是修改整个 Agent Loop。

这就是你昨天第 7 章看到的**解耦与可扩展性**真正落地。

---

# 【白天理解目标②】真正理解 ReAct Loop

今天不要把 ReAct 理解成：

```text
一个 Prompt 模板
```

而应该理解成控制流：

```text
for step in range(max_steps):

    LLM
     ↓

    Response
     ↓

    Final Answer ?
       ├─ YES → return
       │
       └─ NO
           ↓
        Action Parser
           ↓
        ToolExecutor
           ↓
        Observation
           ↓
        History
           ↓
        下一轮 LLM
```

所以：

> **LLM 决定下一步做什么；Runtime 保证这个决策能够被执行并继续循环。**

---

# 【白天理解目标③】History 和 Trace 不完全是一回事

先自己思考：

```text
History
```

主要服务谁？

再思考：

```text
Trace
```

主要服务谁？

今天先形成这个直觉：

```text
History
→ Agent 下一轮推理需要的上下文

Trace
→ 开发者观察 Agent 到底发生了什么
```

它们可能保存相同信息，但目的不同。

例如：

```text
Step 1
Thought: ...
Action: Calculator[12*8]
Observation: 96

Step 2
Thought: ...
Final Answer: 96
```

既可以进入 Agent Context，也可以用于 Debug / Observability。

以后你学 Agent Eval 时还会回来用它。

---

# 【白天理解目标④】为什么一定需要 max_steps

考虑一个 Agent：

```text
LLM
↓
Search
↓
没找到
↓
LLM
↓
Search
↓
没找到
↓
LLM
↓
Search
...
```

如果没有：

```text
max_steps
```

可能出现：

```text
无限循环
Token 持续消耗
Tool API 持续调用
延迟不断增长
```

所以 `max_steps` 本质上属于：

> **Agent Runtime 的安全边界和资源控制。**

今天代码里必须真正实现它。

---

# 【工程思维｜Debug 顺序】

如果出现：

```text
Agent 一直调用同一个 Tool
```

不要第一时间只怪 LLM。

按顺序查：

```text
① LLM Response

到底输出了什么？

↓

② Parser

Action 有没有解析错？

↓

③ ToolExecutor

参数有没有正确传？

↓

④ Tool Result

工具结果本身对不对？

↓

⑤ Observation

有没有正确加入 History？

↓

⑥ 下一轮 Prompt / Messages

LLM 有没有真正看到 Observation？

↓

⑦ Termination

Final Answer / max_steps 判断有没有问题？
```

以后做真实 Agent，这个排查顺序很有用。

---

# 【Agent 开发面试表达｜15 分钟】

练习：

> 一个最小 ReAct Agent Runtime 是怎么工作的？

尝试在 60–90 秒内讲：

```text
LLM
Action Parser
Tool Registry
ToolExecutor
Observation
History
Loop
max_steps
Final Answer
```

不要讲代码 API。

讲**数据怎么流**。

---

# 【晚上代码预演｜20 分钟】

晚上真正写代码之前，在纸上闭卷写出：

```text
Tool
↓
Registry
↓
ToolExecutor
```

然后：

```text
LLM
↓
Parser
↓
Executor
↓
Observation
↓
History
↓
LLM
```

最后套：

```text
for step in range(max_steps):
```

如果这三张图画不出来，先不要开 IDE。

---

# B｜晚上约 2 小时

## 【晚上目标】闭卷写 Mini ReAct Agent Runtime

建议新建：

```text
react_runtime_rewrite.py
```

今天不要复制旧代码。

---

## 第一阶段｜Tool

闭卷实现最小：

```python
class Tool:
    ...
```

至少拥有：

```text
name
description
func
execute()
```

并加入：

```text
try / except
```

Tool 执行失败：

```text
Error executing tool ...
```

作为结果返回。

不要直接 Crash。

---

## 第二阶段｜ToolRegistry

实现：

```python
class ToolRegistry:
    ...
```

至少支持：

```text
register(tool)

find(name)
```

如果 Tool 不存在：

```text
unknown_tool
```

不要让整个程序直接崩。

---

## 第三阶段｜ToolExecutor

实现：

```python
class ToolExecutor:
    ...
```

数据流：

```text
tool_name
tool_input
↓
registry.find()
↓
tool.execute()
↓
result
```

注意：

> Executor 负责调度执行，不负责具体 Tool 业务。

---

## 第四阶段｜Action Parser

不用追求复杂 Regex。

今天只支持：

```text
Action: Calculator[12*8]
```

解析：

```text
tool_name = Calculator

tool_input = 12*8
```

同时识别：

```text
Final Answer:
```

今天重点是 Runtime，不是 Parser 技巧。

---

## 第五阶段｜ReAct Agent Loop

核心：

```text
history = []

for step in range(max_steps):

    response = llm(...)

    history.append(...)

    if final:
        return answer

    action = parser(...)

    observation = executor(...)

    history.append(observation)
```

必须让：

```text
Observation
```

进入下一轮 LLM Context。

这是今天最核心的验收点。

---

# 【验证｜全部手动 Case】

今天不写 Pytest。

## Case A｜正常 Tool

输入：

```text
12 × 8 是多少？
```

期望 Trace：

```text
Step 1

Thought
↓
Action: Calculator[12*8]
↓
Observation: 96

Step 2

Thought
↓
Final Answer: 96
```

---

## Case B｜不存在 Tool

模拟：

```text
Action: UnknownTool[test]
```

期望：

```text
Registry
↓
Not Found
↓
Error Observation
↓
LLM
```

Agent 不 Crash。

---

## Case C｜Tool 内部异常

让一个 Tool 主动：

```python
raise ValueError(...)
```

期望：

```text
Tool.execute
↓
catch exception
↓
Error Observation
↓
LLM
```

---

## Case D｜max_steps

让 Mock LLM 永远返回：

```text
Action: Calculator[1+1]
```

验证：

```text
step == max_steps
↓
Agent 停止
```

不能无限跑。

---

## Case E｜Trace

最终至少能打印：

```text
Step 1
Response
Action
Observation

Step 2
Response
Final
```

如果你能从 Trace 定位 Agent 卡在哪一步，今天的工程目标就达到了。

---

# 【闭卷重写｜30 分钟】

第一版跑通以后：

```text
关闭旧代码
```

重新建一个文件，只写骨架：

```text
Tool

ToolRegistry

ToolExecutor

ActionParser

ReActAgent
```

要求自己恢复核心方法和调用关系。

语法/API 忘了允许定点查询。

**数据流不允许照抄。**

---

# 【闭卷小测】

### 概念题 1

为什么：

```text
ToolExecutor
```

不应该同时承担：

```text
Tool Registry
+
具体 Tool 业务逻辑
```

？

### 概念题 2

为什么 Observation 必须进入下一轮 LLM Context？

### 概念题 3

`max_steps` 除了“防死循环”，从生产 Agent 的角度还控制了哪些东西？

### 代码 / 流程题

闭卷补完整：

```text
User
↓
LLM
↓
Response
↓
________
↓
tool_name + tool_input
↓
________
↓
Registry
↓
Tool
↓
execute
↓
________
↓
History
↓
LLM
```

然后在整个流程外面补上：

```text
________
```

控制循环次数。

---

# 【今天完成标准】

今天属于**代码日**。

不是“看懂”就算过。

至少需要脱离原文写出：

```text
Tool
ToolRegistry
ToolExecutor
ActionParser
ReAct Loop
History
max_steps
```

核心骨架。

并手动通过：

```text
正常 Tool       ✅
Unknown Tool    ✅
Tool Exception  ✅
max_steps       ✅
Trace           ✅
```

最后能闭卷画出：

```text
LLM
↓
Parser
↓
Executor
↓
Registry
↓
Tool
↓
Observation
↓
History
↓
LLM
```

达到这些标准后：

> **Day 1 Tool Calling Runtime 代码债 + Day 2 ReAct Agent Loop 核心代码债，可以视为完成第一轮清偿。**

明天周日再继续处理 **Plan-and-Solve / Reflection 最小实现 + 本周闭卷周测**，今天不要提前冲新理论。

**状态反馈：** `完成` / `未完成 + 卡点` / `暂停` / `今天忙 + 可用时间`。
