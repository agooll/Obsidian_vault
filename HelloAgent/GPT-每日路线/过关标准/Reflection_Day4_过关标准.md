# Reflection Day 4 过关标准

> 今天过关的核心是：能说明 Reflection 的价值来自 Feedback 进入下一轮生成，而不是单纯多问一次 LLM。

## 1. Generate、Reflect、Revise

- 能说清楚 `Generator` 第一次根据问题生成 Draft。
- 能说清楚 `Reflector` 根据问题和 Draft 产生 Feedback。
- 能说清楚 `Generator` 第二次要读取原问题、上一版答案和 Feedback，生成 Revision。

**我的作答：**

- 
- 
- 

## 2. Feedback 必须进入下一轮

- 能解释 Feedback 只打印出来不算 Reflection。
- 能说明 Revision 为什么要读取 Feedback。
- 能举例说明 Draft 的缺陷如何通过 Feedback 改进。

**我的作答：**

- 
- 
- 

## 3. Reflection、Retry、ReAct 的区别

- 能说明 Reflection 的反馈来自对答案质量的评价。
- 能说明 ReAct 的反馈来自外部工具或环境 Observation。
- 能说明 Retry 通常是失败后重试，不一定带质量反馈。
- 能说清这三种循环不能混成同一种。

**我的作答：**

- 
- 
- 
- 

## 4. Stop Condition

- 能说清楚 Reflection 不能无限执行。
- 能说明 `max_rounds` 保护 token、耗时和无限修改风险。
- 能说明 Reflector 可能给出错误反馈，轮数越多不一定越好。

**我的作答：**

- 
- 
- 

## 5. 最小流程验收

能闭卷画出并讲清楚：

```text
Question
-> Generator
-> Draft
-> Reflector
-> Feedback
-> Generator(Question + Previous Answer + Feedback)
-> Revision
-> Continue? / END
```

**我的流程图 / 解释：**

```text








```

## 6. 最小闭卷代码验收

不用查资料，能写出：

- `Generator.generate(question, previous_answer=None, feedback=None)`。
- `Reflector.reflect(question, answer)`。
- `ReflectionAgent.run(question)`。
- `current_answer` 被保存并更新。
- `feedback` 真正进入下一轮生成。
- `round / max_rounds` 能控制退出。

**我的闭卷代码：**

```python














```

**今日自检结论：**

- 我是否能解释 Reflection 不是简单重试：
- 我是否能闭卷写出 Generate -> Reflect -> Revise：
- 今天还没彻底懂的点：

