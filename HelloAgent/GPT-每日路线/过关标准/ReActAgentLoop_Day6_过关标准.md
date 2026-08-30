# ReAct Agent Loop Day 6 过关标准

> 今天过关不看 ReAct 定义，而是看你能不能关闭教程后写出最小 Agent Loop，并把它映射到 LangGraph。

## 1. Parser 职责

- 能说明 Parser 不负责决策，只负责解析 LLM Response。
- 能从 `Action: Search[LangGraph]` 中解析出 `tool_name = "Search"` 和 `tool_input = "LangGraph"`。
- 能说明 Parser 输出会交给 ToolExecutor。

**我的作答：**

- 
- 
- 

## 2. Runtime 执行链

- 能闭卷说出：ToolExecutor -> Registry -> Tool.execute。
- 能说明未知 Tool 属于 LLM 决策错误或工具查找错误，不能直接让程序崩溃。
- 能说明 Tool 内部异常应该转成 Error Observation。

**我的作答：**

- 
- 
- 

## 3. History 与下一轮 LLM

- 能说明 Observation 要追加回 History。
- 能说明下一轮 Prompt / Context 必须包含历史轨迹。
- 能说明最终答案不是 Tool 直接返回，而是 Agent 根据历史综合后结束。

**我的作答：**

- 
- 
- 

## 4. max_steps

- 能说明 `max_steps` 是 Agent Loop 的安全阀。
- 能举例说明 Fake LLM 永远返回 Action 时如何退出。
- 能区分 Tool 异常保护和 Loop 退出保护。

**我的作答：**

- 
- 
- 

## 5. ReAct 到 LangGraph 的映射

- `history` -> State。
- `call_llm()` -> LLM Node。
- `execute_tool()` -> Tool Node。
- `if Action / Final` -> Conditional Edge。
- `while loop` -> Graph Cycle。
- `return final` -> END。

**我的作答：**

- 
- 
- 
- 
- 
- 

## 6. 最小闭卷代码验收

不用查资料，能写出：

- Fake LLM。
- `parse_action()`。
- Tool Runtime。
- `run(question)` 主循环。
- History 追加 Observation。
- Final Answer 或 `max_steps` 退出。

**我的闭卷代码：**

```python
















```

**今日自检结论：**

- 我是否能从 LLM Response 推到下一轮 LLM：
- 我是否能把 ReAct Loop 映射成 LangGraph：
- 今天还没彻底懂的点：

