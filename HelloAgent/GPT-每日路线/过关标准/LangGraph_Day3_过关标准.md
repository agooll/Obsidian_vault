# LangGraph Day 3 过关标准

> 今天过关的核心是：理解 State 怎么通过 Checkpointer 保存和恢复，以及 `thread_id` 为什么能区分不同执行线程。

## 1. State、Checkpoint、Checkpointer

- 能说明 `State` 是 Graph 当前运行时的共享数据。
- 能说明 `Checkpoint` 是某个执行时刻的 State Snapshot。
- 能说明 `Checkpointer` 负责保存和读取 Checkpoint。
- 能说清三者不是同一个东西。

**我的作答：**

- 
- 
- 
- 

## 2. Checkpoint 生成时机

- 能说明 Checkpoint 保存的是 State 快照，不是 Node 函数本身。
- 能说明简单串行图里可以近似理解为 Node 步骤完成、State 更新后形成快照。
- 能记住更严格说法：Checkpoint 保存于 super-step 边界。

**我的作答：**

- 
- 
- 

## 3. thread_id

- 能说明 `thread_id` 用来标识哪一条执行线程 / 会话。
- 能说明 `thread_id` 通常由应用侧提供，不要默认理解成 LangGraph 自动根据任务生成。
- 能说明相同 `thread_id` 可以继续同一条状态线。
- 能说明不同 `thread_id` 的 State / Checkpoint 彼此隔离。

**我的作答：**

- 
- 
- 
- 

## 4. thread_id + checkpoint_id

- 能说明只给 `thread_id` 通常定位这条线程的最新状态。
- 能说明 `thread_id + checkpoint_id` 可以定位某个历史快照。
- 能解释为什么这能支持回溯、恢复和 replay。

**我的作答：**

- 
- 
- 

## 5. Persistence 解决什么

- 能说明没有 Persistence 时，进程结束或下一次调用不一定保留原 State。
- 能说明 Persistence 支持多轮 Agent、Human-in-the-loop、错误恢复。
- 能区分 Checkpoint Persistence 和 Long-term Memory：前者是执行状态快照，后者更像长期事实/偏好存储。

**我的作答：**

- 
- 
- 

## 6. 最小流程验收

能闭卷画出并讲清楚：

```text
thread_id = "001"
-> Input
-> State 0
-> Node A
-> Partial Update
-> New State
-> Checkpointer
-> Checkpoint 1
-> Node B
-> New State
-> Checkpoint 2
```

**我的流程图 / 解释：**

```text










```

## 7. 最小代码 / Case 验收

不用查资料，能说明或写出：

- Graph 编译时配置 checkpointer。
- 调用 Graph 时传入 `configurable.thread_id`。
- 用相同 `thread_id` 连续两次 invoke，第二次能接上前面的状态。
- 换成不同 `thread_id` 后，状态不混在一起。
- 能查看最新 State Snapshot。

**我的闭卷代码 / Case：**

```python












```

**今日自检结论：**

- 我是否能区分 State / Checkpoint / Checkpointer / thread_id：
- 我是否能解释同 thread 和不同 thread 的差异：
- 今天还没彻底懂的点：

