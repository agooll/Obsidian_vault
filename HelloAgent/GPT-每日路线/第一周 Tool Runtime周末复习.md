### ReAct Loop 全流程
1. LLM
   LLM 输出：
   Action: Search[深圳天气] 

2. Action parser
   从字符串里提取：
   tool_name = "Search"
   tool_input = "深圳天气" 
   
3. Tool Runtime Registry
   registry.get_tool("Search") 

4. Tool Runtime Execute/Executor
   search.execute("深圳天气") 

5. observation
   返回：
   "深圳今天多云..." 

6. React Loop self.history = history+observation
   把：
   Observation: 深圳今天多云...
   加进 history 
   
7. LLM再次Reason
   LLM 根据 Observation 决定下一步

#### HelloAgents Day 4：Tool Runtime 错误处理踩坑笔记

##### 1. 这次踩到的核心坑

一开始我认为：

> 如果工具内部出现 `1 / 0` 这样的逻辑错误，应该由 LLM 在调用工具之前判断并阻止错误发生，因此异常最终应该由 LLM 处理。

这个理解不准确。

正确答案是：

> **工具内部的 Python 异常，应该优先由 `Tool.execute()` 捕获，并转换成 Error Observation，再交给 LLM 决定下一步。**

​

---

​

##### 2. 为什么不能把异常处理交给 LLM

LLM 的确应该尽可能减少错误调用，例如依靠：

​

- Prompt

- Tool Description

- 参数 Schema

- 模型自身的推理能力

​

来决定：

​

- 要不要调用工具

- 调用哪个工具

- 给工具传什么参数

​

但 Agent 工程不能建立在一个假设上：

​

> “LLM 一定不会犯错。”

​

同样也不能假设：

​

> “只要 LLM 参数传对，工具就一定能正常执行。”

​

现实中工具可能因为很多 LLM 无法提前知道的原因失败，例如：

​

```python

requests.get(...)

可能网络超时。

json.loads(...)

可能遇到非法 JSON。

数据库工具可能连接中断。

计算工具也可能出现：

1 / 0

最终抛出：

ZeroDivisionError

因此：

> **LLM 可以减少错误，但 Runtime 必须假设错误一定会发生。**

---

##### 3. 正确的异常处理链路

假设 LLM 输出：

Action: Calculator[xxx]

调用链应该是：

LLM

 ↓

Action

 ↓

Action Parser

 ↓

ToolExecutor

 ↓

Registry 找到 Tool

 ↓

tool.execute(tool_input)

 ↓

Tool.execute()

 ↓

self.func(tool_input)

 ↓

发生异常

 ↓

Tool.execute() 的 try-except 捕获

 ↓

转换成 Error Result

 ↓

Observation

 ↓

回到 ReAct Loop

 ↓

LLM 根据错误重新决策

例如：

class Tool:

    def execute(self, tool_input: str) -> str:

        try:

            return str(self.func(tool_input))

        except Exception as e:

            return f"Error executing tool {self.name}: {str(e)}"

如果底层函数：

def calculator(x):

    return 1 / 0

那么工具不会让整个 Agent Crash，而是返回：

Error executing tool Calculator: division by zero

随后它可以被包装成：

Observation:

Error executing tool Calculator: division by zero

LLM 再根据 Observation 判断：

- 是否修改参数
- 是否重新调用
- 是否切换工具
- 是否采用备用方案
- 是否直接向用户解释失败原因

---

##### 4. 我混淆的两类错误

###### 4.1 LLM 决策错误

例如 Registry 中只有：

Search

Calculator

但 LLM 却输出：

Action: Weather[深圳]

这属于：

> **LLM 的决策错误 / 工具选择错误**

造成这种问题的因素可能包括：

- Tool Description 不够清晰
- Prompt 约束不足
- LLM 推理错误
- 工具列表理解错误

但是即使 LLM 犯错，Runtime 仍然必须兜底。

例如：

Weather 不存在

 ↓

ToolExecutor / Registry 检查失败

 ↓

Error Observation:

Tool 'Weather' not found

 ↓

LLM 重新 Reason

 ↓

尝试 Search[深圳天气]

所以：

> **不能因为这是 LLM 的决策错误，就允许程序 Crash。**

---

###### 4.2 Tool 执行错误

例如：

Action: Calculator[xxx]

工具本身存在，但执行时出现：

1 / 0

这属于：

> **工具运行阶段错误**

此时异常是在：

tool.execute(tool_input)

进入工具内部以后发生的。

因此应该由：

Tool.execute()

中的：

try-except

优先捕获。

---

##### 5. LLM 和 Tool Runtime 的职责边界

这是这次最重要的认知。

###### LLM：负责智能和决策

主要负责：

用户需求

 ↓

理解任务

 ↓

Reason

 ↓

选择工具

 ↓

生成参数

 ↓

根据 Observation 决定下一步

可以总结为：

> **LLM 负责“该做什么”。**

---

###### Tool Runtime：负责可靠执行

主要负责：

接收 Tool Call

 ↓

解析工具名和参数

 ↓

Registry 查找工具

 ↓

Executor 调用工具

 ↓

处理成功或失败

 ↓

生成可返回的结果

可以总结为：

> **Tool Runtime 负责“把它可靠地做出来”。**

---

###### Tool.execute()：工具内部异常保护

负责：

调用真实 Python 函数

 ↓

成功 → 返回结果

失败 → 捕获异常

 ↓

返回 Error Result

---

###### Observation：把执行结果告诉 Agent

Observation 不只包括成功结果。

成功：

Observation:

深圳今天多云

失败也可以是：

Observation:

Error executing Search: timeout

因此：

> **Observation 是 Agent 对工具执行结果的反馈，其中错误本身也是一种有效信息。**

---

##### 6. 最值得记住的一句话

> **LLM 可以减少错误，但 Runtime 必须假设错误一定会发生。**

进一步可以理解为：

> **LLM 负责智能，Runtime 负责可靠性。**

这也是 Agent 工程与“简单调用一次大模型 API”之间非常重要的区别。

---

##### 7. 当前 ToolExecutor 的正确思路

简化版本：

class ToolExecutor:

    def __init__(self, registry):

        self.registry = registry

​

    def execute(self, tool_name: str, tool_input: str) -> str:

        if tool_name not in self.registry:

            return f"Error: Tool '{tool_name}' not registered"

​

        tool = self.registry[tool_name]

​

        return tool.execute(tool_input)

它做了三件事：

1. 根据 tool_name 查找工具

2. 工具不存在时返回 Error，而不是 Crash

3. 工具存在时调用 tool.execute(tool_input)

其中：

ToolExecutor.execute(...)

表示：

> **执行器调度某一个工具。**

而：

tool.execute(...)

表示：

> **真正执行这个 Tool。**

两者名字虽然都是 `execute`，但是职责不同。

---

##### 8. 下一步需要继续思考的问题

目前 `Tool.execute()` 的 `try-except` 只能捕获：

已经进入 Tool.execute() 之后

发生的异常。

如果下面这一行：

tool = self.registry[tool_name]

本身因为 Registry 内部问题抛出异常，那么：

Tool.execute()

还没有被调用。

因此需要继续思考：

> **Registry / ToolExecutor 自己发生的异常，应该由哪一层兜底？**

这会进一步引出：

- 分层异常处理
- Runtime 级异常保护
- Error Observation 标准化
- Retry / Fallback
- 最大循环次数
- Agent Loop 的可靠性设计

---

##### 9. 今日知识结构

ReAct Loop

│

├── LLM

│    └── Reason / Action

│

├── Action Parser

│    └── tool_name + tool_input

│

├── Tool Runtime

│    │

│    ├── Registry

│    │    └── 查找 Tool

│    │

│    └── ToolExecutor

│         └── 调用 tool.execute()

│

├── Tool

│    └── execute()

│         ├── 调用真实函数

│         └── 捕获工具内部异常

│

├── Observation

│    ├── Success Result

│    └── Error Result

│

└── 回到 LLM

     └── 根据 Observation 决定下一步

---

##### 10. 自测

###### Q1

工具内部执行：

1 / 0

异常优先在哪里捕获？

**答案：**

Tool.execute()

###### Q2

为什么不能完全依赖 LLM 在调用工具前避免错误？

**答案：**

因为：

- LLM 可能判断错误
- 工具可能受到网络、数据库、第三方 API 等外部因素影响
- 很多运行时异常无法被 LLM 提前预测

所以 Runtime 必须具备异常兜底能力。

###### Q3

下面哪个说法更准确？

A. LLM 负责所有错误处理

B. Tool Runtime 只负责发出执行信号

C. LLM 负责智能决策，Runtime 负责可靠执行

**答案：C**

###### Q4

Error 是否可以成为 Observation？

**答案：可以。**

错误信息也是 Agent 判断下一步的重要反馈。

---

##### 今日最终结论

LLM

= 尽可能做对决策

​

Tool Runtime

= 即使决策或工具出错，也尽量不让系统直接崩溃

​

Error

= 不一定意味着 Agent 结束

​

Error

→ Observation

→ Reason

→ Retry / Change Tool / Fallback

​

这版你直接整段复制进 Obsidian/Typora 就行。