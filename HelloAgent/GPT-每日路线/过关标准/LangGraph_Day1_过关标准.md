# LangGraph Day 1 过关标准

> 今天过关的核心是：理解 LangGraph 是「带状态的节点执行图」，并能跑通最小 StateGraph。

## 1. State、Node、Edge

- 能说明 `State` 是 Graph 当前共享的数据。
- 能说明 `Node` 是读取 State、执行逻辑、产生更新的步骤。
- 能说明 `Edge` 决定一个 Node 执行完后去哪里。
- 能说清 Node 不是完整 Agent，而是 Agent Workflow 中的步骤。

**我的作答：**

- 
- 
- 
- 

## 2. Conditional Edge

- 能说明 Conditional Edge 对应过去手写代码里的 `if / else` 路由。
- 能说明它根据当前 State 决定下一步 Node 或 END。
- 能举例说明 `Action` 走 Tool Node，`Final` 走 END。

**我的作答：**

- 
- 
- 

## 3. Cycle

- 能说明 Graph 可以通过 Edge / Conditional Edge 回到前面的 Node。
- 能说明 Cycle 对应过去手写 ReAct 的 `while loop`。
- 能说明必须有退出条件，否则会无限循环。

**我的作答：**

- 
- 
- 

## 4. 最小 StateGraph API

- 能知道今天只需要认识：`StateGraph`、`add_node()`、`add_edge()`、`compile()`、`invoke()`、`START`、`END`。
- 能说明 `compile()` 是把图结构变成可执行 Graph。
- 能说明 `invoke(initial_state)` 会从初始 State 开始执行并返回最终 State。

**我的作答：**

- 
- 
- 

## 5. ReAct 到 LangGraph 的映射

能闭卷补全：

```text
手写 ReAct                  LangGraph
history              ->     
call_llm()           ->     
execute_tool()       ->     
if Action / Final    ->     
while loop           ->     
return final         ->     
```

**我的作答：**

```text






```

## 6. 最小闭卷代码 / 流程验收

不用查资料，能写出或画出：

```text
START
-> add_one
-> multiply_ten
-> END
```

初始：

```text
value = 1
```

最终：

```text
value = 20
```

**我的闭卷代码：**

```python












```

**今日自检结论：**

- 我是否能区分 State / Node / Edge：
- 我是否能闭卷画出最小 StateGraph：
- 今天还没彻底懂的点：

