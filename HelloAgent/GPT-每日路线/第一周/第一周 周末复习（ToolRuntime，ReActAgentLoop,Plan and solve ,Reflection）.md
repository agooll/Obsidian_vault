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

正确理解是：

> **工具内部的 Python 异常，应该优先由 `Tool.execute()` 捕获，并转换成 Error Observation，再交给 LLM 决定下一步。**

---

##### 2. 为什么不能把异常处理完全交给 LLM

LLM 的确应该尽可能减少错误调用。

例如依靠：

- Prompt
    
- Tool Description
    
- 参数 Schema
    
- 模型自身推理能力
    

去决定：

- 要不要调用工具
    
- 调用哪个工具
    
- 给工具传什么参数
    

但是 Agent 工程不能建立在下面这个假设上：

> **LLM 一定不会犯错。**

同样，也不能认为：

> **只要 LLM 参数传对了，工具就一定能够正常运行。**

因为工具运行时还会遇到很多 LLM 无法提前预测的问题。

例如网络请求：

```python
requests.get(...)
```

可能出现：

```text
Timeout
ConnectionError
```

JSON 解析：

```python
json.loads(...)
```

可能遇到非法 JSON。

数据库工具可能：

```text
连接中断
连接超时
SQL 执行失败
```

计算工具甚至可能出现：

```python
1 / 0
```

最终抛出：

```text
ZeroDivisionError
```

因此必须记住：

> **LLM 可以减少错误，但 Runtime 必须假设错误一定会发生。**

---

##### 3. 正确的异常处理链路

假设 LLM 输出：

```text
Action: Calculator[xxx]
```

完整链路：

```text
LLM
 ↓
Action
 ↓
Action Parser
 ↓
ToolExecutor
 ↓
Registry 查找 Tool
 ↓
tool.execute(tool_input)
 ↓
Tool.execute()
 ↓
self.func(tool_input)
 ↓
发生异常
 ↓
try-except 捕获
 ↓
Error Result
 ↓
Observation
 ↓
ReAct Loop
 ↓
LLM 根据错误重新决策
```

例如当前的 `Tool`：

```python
class Tool:
    def execute(self, tool_input: str) -> str:
        try:
            return str(self.func(tool_input))
        except Exception as e:
            return f"Error executing tool {self.name}: {str(e)}"
```

底层工具：

```python
def calculator(x):
    return 1 / 0
```

执行：

```python
tool.execute("xxx")
```

进入：

```python
self.func(tool_input)
```

此时：

```python
1 / 0
```

抛出：

```text
ZeroDivisionError
```

但是异常不会继续把整个 Agent 程序搞崩。

因为：

```python
except Exception as e:
```

会把异常捕获。

最终转换成：

```text
Error executing tool Calculator: division by zero
```

然后可以作为：

```text
Observation:
Error executing tool Calculator: division by zero
```

重新交给 LLM。

---

##### 4. 我这次混淆的两种错误

###### 4.1 LLM 决策错误

假设 Registry 中只有：

```text
Search
Calculator
```

但 LLM 却生成：

```text
Action: Weather[深圳]
```

这属于：

> **LLM 决策错误 / 工具选择错误。**

可能原因：

- Tool Description 描述不清楚
    
- Prompt 约束不够
    
- LLM 推理错误
    
- LLM 对当前工具列表理解错误
    

这类问题确实可以通过：

```text
更好的 Prompt
+
更好的 Tool Description
+
更严格的 Schema
+
更好的模型能力
```

减少。

但是：

> **即使 LLM 犯错，Runtime 依然必须兜底。**

正确流程：

```text
LLM:
Action: Weather[深圳]

 ↓

ToolExecutor 查找 Weather

 ↓

不存在

 ↓

Error Observation:
Tool 'Weather' not found

 ↓

LLM 再次 Reason

 ↓

发现还有 Search

 ↓

Action:
Search[深圳天气]
```

也就是说：

```text
LLM 犯错
≠
Agent 必须 Crash
```

---

###### 4.2 Tool 执行错误

另一种情况：

LLM 的决策其实完全正确：

```text
Action: Calculator[xxx]
```

Registry 里面也确实存在：

```text
Calculator
```

但是工具真正运行的时候出现：

```python
1 / 0
```

这属于：

> **Tool Runtime 阶段的执行错误。**

这个时候问题不是 LLM 选错了工具。

而是：

```text
工具本身执行失败
```

因此应该由：

```python
Tool.execute()
```

内部的：

```python
try-except
```

进行异常保护。

---

##### 5. LLM 和 Tool Runtime 的职责边界

这是这次最重要的知识点。

###### LLM：负责智能和决策

LLM 主要负责：

```text
用户需求
 ↓
理解任务
 ↓
Reason
 ↓
选择 Tool
 ↓
生成 Tool Input
 ↓
根据 Observation 决定下一步
```

一句话：

> **LLM 负责“应该做什么”。**

---

###### Tool Runtime：负责可靠执行

Tool Runtime 主要负责：

```text
收到 Tool Call
 ↓
解析 Tool Name / Tool Input
 ↓
Registry 找工具
 ↓
Executor 调用工具
 ↓
执行成功 / 执行失败
 ↓
产生结果
```

一句话：

> **Tool Runtime 负责“把 LLM 的决定可靠地执行出来”。**

---

##### 6. Tool.execute() 的职责

`Tool.execute()` 是一个统一的工具执行入口。

例如：

```python
class Tool:
    def execute(self, tool_input: str) -> str:
        try:
            return str(self.func(tool_input))
        except Exception as e:
            return f"Error executing tool {self.name}: {str(e)}"
```

它负责：

```text
接收 tool_input
 ↓
执行真正的 func
 ↓
成功
 └── 返回 Result

失败
 └── 捕获 Exception
      ↓
      转换成 Error Result
```

所以：

```python
self.func(tool_input)
```

才是真正调用底层工具。

而：

```python
tool.execute(tool_input)
```

是经过统一异常保护之后调用工具。

---

##### 7. ToolExecutor 和 Tool.execute() 的区别

当前的 `ToolExecutor`：

```python
class ToolExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, tool_input: str) -> str:

        if tool_name not in self.registry:
            return f"Error: Tool '{tool_name}' not registered"

        tool = self.registry[tool_name]

        return tool.execute(tool_input)
```

这里有两个 `execute()`。

###### ToolExecutor.execute()

```python
ToolExecutor.execute(...)
```

作用：

> **调度工具。**

它负责：

```text
你想执行哪个工具？
 ↓
这个工具存在吗？
 ↓
找到对应 Tool
 ↓
调用这个 Tool
```

---

###### Tool.execute()

```python
tool.execute(...)
```

作用：

> **真正进入某一个具体 Tool 的执行过程。**

负责：

```text
执行 self.func()
+
捕获 Tool 内部异常
```

所以完整关系：

```text
ToolExecutor.execute()
        ↓
找到具体 Tool
        ↓
tool.execute()
        ↓
self.func()
```

---

##### 8. Observation 不只有成功结果

以前容易把 Observation 理解成：

> 工具正常执行以后返回的数据。

其实不够准确。

Observation 可以是成功：

```text
Observation:
深圳今天多云
```

也可以是失败：

```text
Observation:
Error executing Search: timeout
```

甚至可以是：

```text
Observation:
Tool 'Weather' not found
Available tools: Search, Calculator
```

对于 Agent 来说：

> **错误本身也是环境反馈。**

因为 LLM 可以根据错误重新做决策。

---

##### 9. 为什么 Error Observation 很重要

普通程序可能：

```text
发生异常
 ↓
Crash
 ↓
程序结束
```

Agent 更希望做到：

```text
发生异常
 ↓
捕获异常
 ↓
Error Observation
 ↓
LLM Reason
 ↓
重新规划
```

例如：

```text
Action:
Weather[深圳]

 ↓

Observation:
Tool Weather not found

 ↓

Thought:
Weather 工具不存在，但是 Search 可以搜索天气。

 ↓

Action:
Search[深圳今天天气]
```

因此：

```text
Error
≠
Agent 必须结束
```

而可以变成：

```text
Error
 ↓
Observation
 ↓
Reason
 ↓
Retry / Change Tool / Fallback
```

---

##### 10. 当前完整架构理解

```text
ReAct Loop
│
├── LLM
│    │
│    ├── Reason
│    └── Action
│
├── Action Parser
│    │
│    ├── tool_name
│    └── tool_input
│
├── Tool Runtime
│    │
│    ├── Registry
│    │    └── 根据 tool_name 找 Tool
│    │
│    └── ToolExecutor
│         └── 调用 tool.execute()
│
├── Tool
│    │
│    └── execute()
│         │
│         ├── self.func(tool_input)
│         │
│         └── try-except 异常保护
│
├── Observation
│    │
│    ├── Success Result
│    └── Error Result
│
└── 回到 LLM
     │
     └── 根据 Observation 决定下一步
```

---

##### 11. 一个非常重要的边界

目前：

```python
Tool.execute()
```

中的：

```python
try-except
```

只能捕获：

> **已经进入 `Tool.execute()` 以后发生的异常。**

例如：

```python
return tool.execute(tool_input)
```

已经成功进入 Tool。

然后：

```python
self.func(tool_input)
```

出现：

```python
1 / 0
```

这时候可以捕获。

但是如果异常发生在：

```python
tool = self.registry[tool_name]
```

这一行呢？

此时：

```python
Tool.execute()
```

甚至还没有被调用。

因此：

> **Tool.execute() 无法捕获发生在它外面的异常。**

这就会进一步引出下一层 Agent 工程问题：

```text
Runtime 级异常保护
Registry 异常
Executor 异常
Retry
Fallback
最大循环次数
```

---

##### 12. 这次最重要的认知升级

###### 错误认知

```text
LLM 足够聪明
 ↓
提前避免错误
 ↓
工具就不会出错
```

###### 正确认知

```text
LLM
 ↓
尽可能做正确决策

但是

Runtime
 ↓
始终假设执行可能失败
 ↓
做好异常保护
```

因此：

> **LLM 负责智能，Runtime 负责可靠性。**

以及：

> **LLM 可以减少错误，但 Runtime 必须假设错误一定会发生。**

---

##### 13. 今日最终总结

```text
LLM
= 决定做什么

Parser
= 把 Action 拆成 Tool Name + Tool Input

Registry
= 管理和查找 Tool

ToolExecutor
= 调度 Tool

Tool.execute()
= 执行 Tool + 捕获工具内部异常

Observation
= 把成功或失败结果反馈给 Agent

ReAct Loop
= 根据 Observation 再次 Reason
```

最终形成：

```text
Reason
 ↓
Action
 ↓
Tool Runtime
 ↓
Result / Error
 ↓
Observation
 ↓
Reason
```

###### 最终记忆句

> **LLM 负责智能，Runtime 负责可靠性。**

> **错误不是 Agent Loop 的终点，错误也可以成为下一轮推理的信息。**



### ReActAGEN