# ReAct Day 2 过关标准

> 今天过关的核心是：能解释 ReAct 为什么必须形成 `Thought -> Action -> Observation -> History -> Thought` 的闭环。

## 1. ReAct = Reason + Act

- 能说明 Reason 对应 `Thought`，负责分析当前情况和下一步。
- 能说明 Act 对应 `Action`，负责选择工具或外部动作。
- 能说明 ReAct 不是一次性回答，而是边推理边行动。

**我的作答：**

- 
- 
- 

## 2. Thought、Action、Observation

- 能说清楚 `Thought` 是模型当前轮的推理。
- 能说清楚 `Action` 是模型决定执行的动作，通常包含工具名和参数。
- 能说清楚 `Observation` 是工具执行后返回给 Agent 的结果。
- 能举一个 `Search[LangGraph]` 或 `Calculator[1+2]` 的完整例子。

**我的作答：**

- 
- 
- 
- 

## 3. Observation 为什么必须进入 History

- 能说明 LLM 本身不会自动记住上一次工具结果。
- 能说明 Observation 进入 History 后，下一轮 LLM 才能基于真实反馈继续推理。
- 能解释：没有 Observation，ReAct 会退化成单向生成。

**我的作答：**

- 
- 
- 

## 4. ReAct Loop 与停止条件

- 能说清楚 ReAct 为什么天然需要循环。
- 能说明循环里每轮都要经历：LLM -> Parser -> Tool -> Observation -> History。
- 能说明 `Final Answer` / `max_steps` 是常见停止条件。
- 能解释没有 `max_steps` 时可能出现无限工具调用。

**我的作答：**

- 
- 
- 
- 

## 5. 最小流程验收

能闭卷画出并讲清楚：

```text
Question
-> LLM
-> Thought
-> Action
-> Parser
-> ToolExecutor
-> Observation
-> History
-> LLM
-> Final Answer / max_steps
```

**我的流程图 / 解释：**

```text










```

## 6. 最小闭卷代码验收

不用查资料，能写出一个 Fake LLM 版本：

- 第一轮 LLM 返回 `Action`。
- Parser 解析出工具名和参数。
- ToolExecutor 执行工具。
- Observation 被追加进 History。
- 第二轮 LLM 读取 History 后返回 Final Answer。
- `max_steps` 能阻止无限循环。

**我的闭卷代码：**

```python














```

**今日自检结论：**

- 我是否能闭卷讲清 ReAct 闭环：
- 我是否能解释 Observation 为什么进入 History：
- 今天还没彻底懂的点：

