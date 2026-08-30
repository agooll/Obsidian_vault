# Plan-and-Solve Day 3 过关标准

> 今天过关的核心是：能把一个复杂问题先拆成 Plan，再按 Step 执行，并让后续 Step 看见前面结果。

## 1. Planner 与 Executor

- 能说清楚 `Planner` 负责把问题拆成步骤。
- 能说清楚 `Executor` 负责执行当前 Step。
- 能说明 Agent 负责组织 Planner、Executor 和执行上下文。
- 能区分 Plan-and-Solve 与 ReAct：一个先规划再执行，一个边观察边行动。

**我的作答：**

- 
- 
- 
- 

## 2. Plan、Step、Context

- 能说明 `Plan` 是步骤列表，不是最终答案。
- 能说明 `Step` 是当前要执行的单个任务。
- 能说明 `context / previous_results` 保存前面 Step 的结果。
- 能解释为什么 Step 2 可能需要 Step 1 的结果。

**我的作答：**

- 
- 
- 
- 

## 3. previous_results 的价值

- 能说清楚 previous_results 不是装饰日志，而是后续执行的输入依据。
- 能说明如果 Step 2 看不到 Step 1 结果，Plan-and-Solve 会变成机械逐步调用。
- 能意识到失败结果也可以进入 Context，供后续步骤判断。

**我的作答：**

- 
- 
- 

## 4. 最小流程验收

能闭卷画出并讲清楚：

```text
Question
-> Planner
-> Plan: [Step 1, Step 2, Step 3]
-> Executor(Step 1, Context)
-> Result 1
-> Context Update
-> Executor(Step 2, Context)
-> Result 2
-> Final Answer
```

**我的流程图 / 解释：**

```text









```

## 5. 最小闭卷代码验收

不用查资料，能写出：

- `Planner.plan(question)` 返回步骤列表。
- `Executor.execute(step, context)` 执行单步。
- `PlanAndSolveAgent.run(question)` 先拿 Plan，再循环执行 Step。
- 每一步结果都进入 `context / previous_results`。
- 最后能基于所有结果产出 Final。

**我的闭卷代码：**

```python














```

## 6. 手动 Case 验收

- Step 1：得到数字 `10`。
- Step 2：把上一步结果乘以 `2`。
- 能手动推演并说明最终应得到 `20`。

**我的 Case 推演：**

```text





```

**今日自检结论：**

- 我是否能解释 Planner / Executor / Context：
- 我是否能闭卷写出 Step Loop：
- 今天还没彻底懂的点：

