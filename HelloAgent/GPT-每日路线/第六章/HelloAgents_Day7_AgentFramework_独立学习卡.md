# HelloAgents｜Day 7 独立学习卡：Agent Framework 抽象预习日

**当前理论进度：** Tool Calling ✅ → ReAct ✅ → Plan-and-Solve ✅ → Reflection ✅ → LangGraph 基础 / Tool Agent / Persistence 已进入收口阶段。  
**当前代码进度：** LangGraph `ToolNode + tools_condition` 已有基础；Persistence 仍需闭卷验收；早期 Tool Runtime / ReAct Loop 仍属于周末代码债。  
**今天：Day 7｜HelloAgents 第 7 章 Agent Framework 核心抽象：Message / Agent / Tool / Registry / Function Calling。**  
**今日模式：周五理论预习模式。** 白天允许推进重要概念；晚上只做 20–40 分钟轻量预演，不扩大代码债。  
**周末约束：** 明天开始优先偿还代码债；如果周末核心代码仍未补齐，下周一暂停新理论。

今天不是继续背 LangGraph API，而是开始回答一个更重要的问题：**如果不用现成框架，一个 Agent Framework 到底应该由哪些模块组成？**

```text
                Agent
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
       LLM      History    Tools
                             │
                        Tool Registry
                             │
                          Execute
                             │
                          Result
                             │
                          Message
```

## 【白天复习｜20 分钟】

先完全不看笔记，主动回答下面问题。今天不给答案，晚上再自己核对。

```text
Q1
Tool、ToolRegistry、ToolExecutor
三者分别应该负责什么？
为什么不能全部塞进一个类？

Q2
ReAct Agent 和 Function Calling Agent
在“LLM → Tool”这一步最大的区别是什么？

Q3
HumanMessage / AIMessage / ToolMessage
为什么不能简单全部换成普通 str？

Q4
如果让你自己设计 Agent 基类，
ReActAgent、ReflectionAgent、PlanSolveAgent
有哪些东西应该共用？

Q5
LangGraph State["messages"]
和 Agent Framework 中的 History
有什么联系，又为什么不能直接认为完全一样？
```

目标不是答得标准，而是暴露你现在的知识断点。

---

# 【白天今日原文】

今天进入 **HelloAgents 第 7 章「构建你的 Agent 框架」**，但只看框架骨架，不追求把第 7 章学完。

## 【必看】7.1 框架设计理念

重点理解为什么要做模块解耦、统一接口和能力抽象。

```text
为什么不能：

def run():
    调 LLM
    解析结果
    找 Tool
    执行 Tool
    保存 History
    再调 LLM
    ...
```

全部写死在一起？

## 【重点】Message / Agent 抽象相关部分

看 `Message` 为什么需要 `role/content/metadata` 这类统一结构，再看 Agent 基类为什么会抽出 `llm`、`history`、`system_prompt`、`run()` 等公共能力。

## 【重点】Tool + ToolRegistry

这一部分要和你 Day 1 的 Tool Runtime 知识直接对照着看，不是重新学一遍 Tool Calling。

## 【重点扫读】FunctionCallAgent

今天只理解 Native Function Calling 和早期 Prompt-based ReAct Parser 的区别。

## 【略看】

- 配置系统
- 异常类
- 日志辅助代码
- 大量工程样板代码

## 【暂不看】

- Memory / RAG
- 复杂异步 Tool
- Multi-Agent
- 第 8 章后面的实现

---

# 【白天理解目标①】Message 为什么是 Agent 基础设施

不要只把：

```text
HumanMessage
AIMessage
ToolMessage
```

理解成 LangGraph 的几个类。

从框架角度看：

```text
User
↓
Message(role=user)

LLM
↓
Message(role=assistant)

Tool
↓
Message(role=tool)
```

它实际上在解决：

> **不同组件之间用什么统一格式交换信息？**

今天重点思考三个问题：

```text
为什么 Agent 内部到处传 str 会越来越难维护？

Tool Result 为什么最好也进入统一 Message 系统？

metadata 可以拿来保存哪些 Agent 工程信息？
```

自己尝试举例：

```python
metadata = {
    "tool_name": ?,
    "latency": ?,
    "step": ?,
    "token_usage": ?
}
```

这会开始连接到你以后必须掌握的 **Trace / Observability**。

---

# 【白天理解目标②】Agent Base Class

你已经学过：

```text
ReAct
Plan-and-Solve
Reflection
```

以前它们像三个独立知识点。

现在换一个框架视角：

```text
                 Agent
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
   ReActAgent  PlanSolve   Reflection
```

它们可能共同拥有：

```text
LLM
System Prompt
History
Tools
Config
run()
```

但 `run()` 内部完全不同。

例如：

```text
ReActAgent.run()

Reason
↓
Action
↓
Observation
↓
Loop
```

而：

```text
ReflectionAgent.run()

Generate
↓
Evaluate
↓
Reflect
↓
Revise
```

今天真正要理解的是：

> **Agent Pattern 可以不同，但 Framework 可以给它们统一生命周期和接口。**

---

# 【白天理解目标③】Tool / Registry / Executor

把 Day 1 再升级一次。

```text
LLM
↓
tool_name + arguments
↓
ToolExecutor
↓
Registry.find(tool_name)
↓
Tool
↓
execute(arguments)
↓
Result
```

尝试自己划责任：

```text
Tool
负责：________

Registry
负责：________

ToolExecutor
负责：________
```

再思考一个非常重要的工程问题：

> 如果明天新增 50 个 Tool，为什么 Agent 主循环最好完全不需要修改？

如果你能回答这个问题，就开始真正理解 Registry 和解耦了。

---

# 【白天理解目标④】ReAct Parser vs Native Function Calling

这是今天最值得理解的概念之一。

你以前实现的是：

```text
LLM

"Thought: ...
 Action: Search[深圳天气]"

↓
ActionParser
↓
tool_name = Search
tool_input = 深圳天气
```

而 Native Function Calling 更接近：

```text
LLM
↓
结构化 tool_call
↓
{
  name: ...,
  arguments: ...
}
↓
Tool Runtime
```

今天不要急着判断谁“更高级”。

思考：

```text
Parser 路线为什么容易解析失败？

Native Function Calling 为什么更稳定？

既然有 Native Function Calling，
ReAct 的 Reason → Act → Observe 思想是不是就没用了？
```

最后一个问题非常重要。

---

# 【白天工程思维】

假设你的 Agent 报错：

```text
Tool "search_user" not found
```

不要直接改 Prompt。

尝试按层定位：

```text
LLM 层
↓
模型输出的 tool_name 是什么？

Schema 层
↓
模型看到的 Tool Description / Schema 对吗？

Parser / Protocol 层
↓
tool_call 是否正确解析？

Registry 层
↓
search_user 是否注册？

Executor 层
↓
是否正确 find？

Tool 层
↓
execute() 是否真正执行？
```

今天形成一个意识：

> Agent Debug 经常不是“模型聪不聪明”，而是组件之间的协议断了。

---

# 【Agent 开发面试表达】

今天在公司可以口头练两个 60 秒问题。

### 面试题 1

> 为什么 Agent Framework 需要统一的 Message、Agent 和 Tool 抽象？

回答时尝试自然出现：

```text
统一接口
模块解耦
可扩展
可维护
Trace
```

### 面试题 2

> Prompt-based ReAct Tool Calling 和模型原生 Function Calling 有什么区别？

不要背定义，直接从：

```text
LLM Output
↓
如何变成可执行 Tool Call
```

开始讲。

---

# 【晚上目标｜周五轻量版 20–40 分钟】

今晚**不要求完整编码**。

只闭卷手画一张你自己的 Mini Agent Framework：

```text
User
↓
Message
↓
Agent.run()
↓
LLM
↓
Tool Call
↓
ToolExecutor
↓
Registry
↓
Tool.execute()
↓
Tool Result
↓
Message
↓
History
↓
LLM
```

然后在纸上尝试写出最小接口，不要求运行：

```python
class Message:
    ...

class Tool:
    ...

class ToolRegistry:
    ...

class ToolExecutor:
    ...

class Agent:
    ...
```

只写：

```text
字段
方法名
职责
```

不要实现内部代码。

---

# 【验证｜手动设计 Case】

今天不使用 Pytest。

假设注册：

```text
calculator
weather
search
```

手动走三条链：

### Case A

```text
"你好"

LLM
↓
Final
```

### Case B

```text
"12 * 8"

LLM
↓
calculator
↓
Executor
↓
Registry
↓
Tool
↓
96
↓
LLM
↓
Final
```

### Case C

```text
LLM 请求：
unknown_tool

↓
Registry.find()
↓
Not Found
↓
Error Observation
↓
返回 Agent
```

尤其思考 Case C：

> 为什么应该返回 Error Observation，而不是整个 Agent Crash？

这是你 Day 1 的知识，现在要从 Framework 角度重新解释。

---

# 【闭卷小测】

### 概念题 1

为什么 Agent Framework 内部需要统一 Message，而不是所有模块直接传字符串？

### 概念题 2

为什么 Registry 应该负责“管理/发现 Tool”，而不应该把每个 Tool 的业务逻辑全部写进去？

### 概念题 3

Native Function Calling 出现之后，为什么 ReAct 的核心思想仍然有价值？

### 代码 / 流程题

不看笔记，画：

```text
User
↓
Agent
↓
LLM
↓
Tool Call
↓
?
↓
?
↓
Tool
↓
Result
↓
?
↓
LLM
↓
Final
```

并自己补上：

```text
Message
Registry
Executor
History
```

的位置。

---

# 【今天完成标准】

今天属于**理论预习日**，所以不以“写出完整 Framework”为标准。

下班前如果你能脱离原文解释：

- `Message` 为什么存在
- `Agent Base Class` 为什么需要抽象
- `Tool / Registry / Executor` 为什么要拆开
- `Prompt-based ReAct Parser` 与 `Native Function Calling` 的核心区别

并且能闭卷画出：

```text
User
↓
Agent
↓
LLM
↓
Tool Runtime
↓
Result
↓
History
↓
LLM
```

今天理论就算通过。

今晚只需要完成 Mini Framework 的接口草图和三个手动 Case，不要求完整代码。

---

# 【明天安排】

明天进入**周六补债模式**。

主任务不会继续冲第 7 章，而是回头闭卷补齐：

```text
Tool
↓
ToolRegistry
↓
ToolExecutor
↓
Tool Calling Runtime
↓
ReAct Agent Loop
↓
History / Trace
↓
max_steps
```

把现在已经懂的理论真正落成代码。

---

# 【状态反馈】

完成后回复以下任一种：

- `完成`
- `未完成 + 卡点`
- `暂停`
- `今天忙 + 可用时间`
