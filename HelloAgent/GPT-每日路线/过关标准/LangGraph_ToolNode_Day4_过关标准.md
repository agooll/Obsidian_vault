# LangGraph ToolNode Day 4 过关标准

> 今天过关的核心是：理解 ToolNode 怎么接住 LLM 的 tool call、执行工具、把 ToolMessage 写回 `messages`，并能说清它和手写 ReAct ToolExecutor 的对应关系。

## 1. ToolNode 的职责

- 能说明 ToolNode 不是 LLM，本身不负责决定要不要调用工具。
- 能说明 ToolNode 读取的是 State 里的 `messages`，重点看最近一条 AIMessage 里的 tool calls。
- 能说明 ToolNode 根据工具名和参数执行已绑定 / 已注册的工具。
- 能说明 ToolNode 的输出通常是 ToolMessage，并回写到 `messages`。

**我的作答：**

- 
- 
- 
- 

## 2. tools_condition

- 能说明 `tools_condition` 是一个路由判断函数。
- 能说明它根据最新 AIMessage 是否包含 tool calls，决定下一步去 ToolNode 还是 END。
- 能区分：LLM Node 产生 tool call；`tools_condition` 只做路由；ToolNode 只执行工具。
- 能画出最小控制流：

```text
LLM Node
-> tools_condition
-> ToolNode / END
```

**我的作答：**

- 
- 
- 
- 

## 3. messages 数据流

- 能说明 HumanMessage、AIMessage、ToolMessage 在 `messages` 里的顺序。
- 能说明工具执行结果为什么必须作为 ToolMessage 回到 `messages`。
- 能解释下一轮 LLM 为什么要读取 ToolMessage 后再生成最终答案。
- 能说明 `add_messages` 为什么适合合并消息列表。

**我的作答：**

- 
- 
- 
- 

## 4. 手写 ReAct 到 LangGraph ToolNode 的映射

能闭卷补全：

```text
手写 ReAct                         LangGraph
history                     ->      
call_llm(history)           ->      
parse_action(llm_output)    ->      
tool_executor.run(action)   ->      
observation                 ->      
if has action else final    ->      
while loop                  ->      
```

**我的作答：**

```text
手写 ReAct                         LangGraph
history                     ->      State[Messages]
call_llm(history)           ->      AIMessage
parse_action(llm_output)    ->      tool_calls
tool_executor.run(action)   ->      Tool_Node
observation                 ->      ToolMessages
if has action else final    ->      tools_condition
while loop                  ->      cycle
```
### 核心升级亮点回顾：
1. **不用手写正则了**：以前手写 ReAct 必须写 `re.search(r"Action: (.*)")` 来抠工具名，现在直接通过大模型原生支持的 **`tool_calls`** 搞定。
2. **不用写 `while` 死循环了**：以前容易控制不好 `while` 导致死循环，现在通过 **`tools` →→ `agent` 的图连线（Edge）** 配合 **`tools_condition` 条件边**，自动优雅地完成循环控制。
## 5. 最小流程验收

不用查资料，能闭卷画出并讲清楚：

```text
START
-> LLM Node
-> AIMessage(tool_calls=[...])
-> tools_condition
-> ToolNode
-> ToolMessage(result)
-> messages reducer 合并
-> LLM Node
-> AIMessage(final answer)
-> tools_condition
-> END
```

要求能指出每一步：

- 哪一步在做决策。
- 哪一步在做路由。
- 哪一步在执行工具。
- 哪一步把工具结果写回 State。

**我的流程图 / 解释：**

```text









```

## 6. 最小闭卷代码验收

不用查资料，能写出或解释一个最小 LangGraph：

- 定义带 `messages` 的 State。
- 定义一个最小工具，例如 `search()` 或 `calculator()`。
- LLM Node 能返回带 tool call 的 AIMessage，或用 Fake LLM 模拟。
- 添加 ToolNode。
- 用 `tools_condition` 做条件路由。
- ToolNode 后回到 LLM Node，形成 ReAct 式循环。
- 最后没有 tool call 时走 END。

**我的闭卷代码：**

```python


















```

## 7. 手动 Case 验收

手动推演这个 Case：

```text
User: 2 + 3 等于多少？
LLM: tool_call -> calculator({"expression": "2+3"})
ToolNode: 执行 calculator
ToolMessage: 5
LLM: 最终回答 2 + 3 = 5
```

要求能解释：

- Tool call 是谁生成的。
- 工具是谁执行的。
- `5` 以什么消息类型回到 State。
- 最终答案为什么仍然应该由 LLM Node 生成，而不是 ToolNode 直接结束。

**我的 Case 推演：**

```text





```

## 8. 最终过关线

今天算过关，必须达到：

```text
能区分 LLM Node / tools_condition / ToolNode 的职责
+
能讲清 tool call -> ToolNode -> ToolMessage -> LLM Node 的数据流
+
能把手写 ReAct 的 ToolExecutor 映射到 LangGraph ToolNode
+
能闭卷画出一个 ToolNode 循环图
```

**今日自检结论：**

- 我是否能说清 ToolNode 不负责决策：
- 我是否能画出 tool call 到 ToolMessage 的完整链路：
- 我是否能把它映射回手写 ReAct：
- 今天还没彻底懂的点：
