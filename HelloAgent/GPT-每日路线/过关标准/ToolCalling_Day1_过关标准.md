# Tool Calling Day 1 过关标准

> 今天过关不看背了多少定义，只看你能不能把「LLM 决定调用工具」到「工具结果返回」这条链路讲清楚。

## 1. Tool Calling 本质

- 能说清楚：Tool Calling 是让模型把「想做的外部动作」表达成可执行的工具调用。
- 能区分：模型负责决策，程序负责执行。
- 能说明 Tool Calling 不等于完整 ReAct；它只解决「调用外部能力」这一层。

**我的作答：**

- 
- 
- 

## 2. LLM、Parser、Runtime 的职责

- 能说清楚 LLM 输出的是工具意图，例如 `tool_name + tool_input`。
- 能说明 Parser 只是把模型输出翻译成结构化调用，不负责重新决策。
- 能说明 Runtime / Executor 负责根据结构化调用真正执行工具。

**我的作答：**

- 
- 
- 

## 3. Tool、Registry、ToolExecutor

- 能说明 `Tool` 保存工具名称、描述和真实执行函数。
- 能说明 `Registry` 负责注册和查找工具。
- 能说明 `ToolExecutor` 负责拿到 `tool_name/tool_input` 后，查工具并执行。
- 能说清楚三者不能混成一个概念。

**我的作答：**

- 
- 
- 
- 

## 4. Result / Observation

- 能说清楚工具执行结果会变成 Agent 后续可使用的信息。
- 能区分普通函数返回值和 Agent 语境里的 Observation。
- 能说明错误结果也应该被包装成可读的 Error Observation。

**我的作答：**

- 
- 
- 

## 5. 最小流程验收

能闭卷画出并讲清楚：

```text
User Question
-> LLM
-> tool_name + tool_input
-> Parser / Structured Call
-> ToolExecutor
-> Registry
-> Tool.execute()
-> Result / Error Observation
```

**我的流程图 / 解释：**

```text








```

## 6. 最小闭卷代码验收

不用查资料，能写出最小结构：

- `Tool`
- `ToolRegistry`
- `ToolExecutor`
- `register(tool)`
- `get_tool(name)`
- `execute(tool_name, tool_input)`
- 未知工具或工具异常时不直接崩溃，而是返回错误信息。

**我的闭卷代码：**

```python












```

**今日自检结论：**

- 我是否能说清 LLM、Parser、Executor 的职责边界：
- 我是否能闭卷写出 Tool Runtime：
- 今天还没彻底懂的点：

