# LangGraph Day 2 过关标准

> 今天的目标不是背 API，而是能判断一个 Graph 执行时 State 是怎么被读、被更新、被合并、被路由的。
> 每个「我的作答」区域留给你闭卷填写，最后能用自己的话写完整，就算真正过关。

## 1. State Schema

- 能闭卷写出一个 `TypedDict` / State Schema。
- 能说清楚每个字段的用途：哪些字段是输入，哪些字段是中间过程，哪些字段是最终结果。
- 能区分普通字段和需要 Reducer 的字段。
- 能说明：State Schema 决定 Graph 中所有 Node 共享的状态结构。

**我的作答：**

- 
- 
- 
- 

## 2. Partial Update

- 能说清楚：Node 可以读取完整 State，但通常只返回自己要更新的字段。
- 能分清楚“读取了哪些字段”和“返回更新了哪些字段”不是一回事。
- 能画出流程：

```text
Current State
-> Node
-> Partial Update
-> Reducer / 默认更新规则
-> New State
```

**我的作答：**

- 
- 
- 
- 

## 3. Reducer

- 能说清楚：Reducer 定义同一个 State 字段收到新 Update 时应该怎么合并。
- 能解释串行场景：没有 Reducer 的普通字段，后一次更新通常覆盖前一次值。
- 能解释并行场景：多个并行 Node 更新同一个无 Reducer 字段时，不能简单理解成谁快谁覆盖谁，而是可能产生并发更新冲突。
- 能判断哪些字段需要 Reducer：日志、消息列表、多节点结果集合、轨迹记录等。

**我的作答：**

- 
- 
- 
- 

## 4. `operator.add` vs `add_messages`

- 能说明 `operator.add` 本质是 Python 的 `a + b`。
- 能举出最小例子：
  - `int`：相加。
  - `str`：拼接字符串。
  - `list`：拼接列表。
- 能说明 `operator.add` 不理解 LangChain Message 的语义，只做普通加法/拼接。
- 能说明 `add_messages` 适合 `HumanMessage`、`AIMessage`、`ToolMessage` 这类消息列表。
- 能说出 `add_messages` 的关键优势：按消息结构合并，并能基于 message id 处理替换/追加。

**我的作答：**

- 
- 
- 
- 
- 

## 5. Conditional Edge

- 能说清楚：Conditional Edge 根据当前 State 决定下一步走哪个 Node。
- 能说明它读取的是上一个节点更新并合并后的 New State。
- 能写出一个简单判断函数，例如根据 `status` / `need_tool` / `error` 返回下一条路径。
- 能解释：具体回到哪个节点或走向哪个节点，取决于业务流程设计。

**我的作答：**

- 
- 
- 
- 

## 6. Cycle

- 能说清楚 Cycle 是 Graph 中允许“回到前面节点继续执行”的结构。
- 能说明 Cycle 必须有退出条件，否则可能无限循环。
- 能举出一个最小场景：生成答案 -> 检查是否合格 -> 不合格回到生成节点 -> 合格结束。
- 能指出 Cycle 常和 Conditional Edge 配合使用。

**我的作答：**

- 
- 
- 
- 

## 7. 最小闭卷代码验收

不用查资料，能写出一个最小 LangGraph：

- 定义 `State`。
- 至少包含 2 个 Node。
- 至少一个 Node 返回 Partial Update。
- 至少一个字段使用 Reducer。
- 至少一个 Conditional Edge。
- 至少一个可能回环的 Cycle。
- 能配置 `thread_id` 并说明它用于区分同一套 Graph 下的不同执行线程/会话。

**我的闭卷代码：**

```python




















```

## 8. 最小流程验收

能闭卷画出并讲清楚：

```text
START
-> Node A
-> Partial Update
-> Reducer 合并
-> New State
-> Conditional Edge 判断
-> Node B / 回到 Node A / END
```

如果能用自己的话解释上面每一步，并能指出 State 在哪里被读、在哪里被更新、在哪里被合并、在哪里决定下一步，就算 LangGraph Day 2 过关。

**我的流程图 / 解释：**

```text









```

**今日自检结论：**

- 我是否能闭卷讲清楚 State 流转：
- 我是否能闭卷写出最小 Graph：
- 今天还没彻底懂的点：
