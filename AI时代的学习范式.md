# 给你一个特别适合你的学习范式

你现在学 Agent / LangGraph，我建议以后每学一个机制，都强制经过下面 6 步。

1. **先不写代码，画数据流。**  
    例如 LangGraph：

```
User Input
   ↓
State
   ↓
planner_node
   ↓
partial update
   ↓
Reducer
   ↓
router
  ↙   ↘
tool   END
```

如果这个东西画不出来，先不要让 AI 写项目。

2. **自己写一个 30～100 行的最小版本。**  
    不是写完整项目，只验证机制。例如 Conditional Edge，就写两个 Node + 一个 Router，不要上来搞 1000 行 Agent。
    
3. **然后让 AI 帮你工程化。**  
    这时候 Codex/Claude Code 可以大量使用：目录、schema、日志、API、测试、UI、Docker 都交出去。
    
4. **读 AI 代码时不要逐行读，而是 Trace。**  
    只追踪关键变量。例如：
    

```
question
→ state["messages"]
→ planner
→ AIMessage
→ ToolCall
→ ToolNode
→ ToolMessage
→ state["messages"]
→ LLM
```

只要数据流掌握了，大量样板代码根本没必要背。

5. **故意制造 Bug。**  
    这个非常重要。

例如：

```
return {"message": result}
```

故意把：

```
return {"messages": [result]}
```

写错。

看看 LangGraph 怎么炸。

或者 router 返回不存在的 Node。

或者 Tool 参数类型错误。

**Debug 一次，比照着教程敲三遍更有价值。**

6. **最后关闭 AI，回答三个问题。**

```
这个模块解决什么问题？

数据从哪里来，到哪里去？

如果它坏了，我第一步查哪里？
```

三个问题都能回答，才算真正学会。

---

你之前其实已经慢慢走到这个方向了。

比如你学习 Tool Runtime 时，不只是记：

```
executor.execute()
```

而是在搞清楚：

```
Registry 干嘛
ToolExecutor 干嘛
Observation 为什么要返回
为什么 Tool Error 不能直接 crash
LLM 和 Runtime 各负责什么
```

这种学习，比把 HelloAgents 全部代码闭卷复刻一遍价值大得多。

你现在 LangGraph 也一样。

不需要哪天突然说：

> “我要脱离 AI，所有代码自己写。”

这反而会让效率大幅降低。

而应该变成：

```
Node / Edge / State
      ↓
理解

Reducer
      ↓
理解 + 最小实现

Conditional Edge
      ↓
理解 + Debug

Checkpointer
      ↓
理解数据生命周期

完整 Agent 项目
      ↓
AI 大量参与
```

---

# 以后真正拉开程序员差距的东西

我认为 AI 越强，下面这些能力反而越值钱：

**第一层：知道要做什么。**

需求模糊的时候，能拆成：

```
Input
State
Node
Tool
Memory
Output
Evaluation
```

**第二层：知道为什么这么做。**

AI 给你三个方案，你能判断哪一个合理。

**第三层：知道它为什么坏了。**

Agent 卡死、无限循环、tool schema 对不上、state 被覆盖、context 爆掉——你能定位。

**第四层：知道怎么改。**

而不是：

> “Claude，再修一下。”

**第五层：知道系统的边界。**

什么时候根本不应该上 Agent？

什么时候 Workflow 比 Agent 好？

什么时候 RAG 根本解决不了问题？

什么时候规则系统比 LLM 更稳定？

这些才是工程能力。

---

所以你以后可以把一句话刻进自己的学习路线里：

> **不要和 AI 比谁写代码快，要训练自己成为那个知道 AI 应该写什么、为什么这么写、写错了在哪里的人。**

你不需要停止手敲代码。

但可以停止**为了手敲而手敲**。

你现在最合适的比例，我反而建议大概：

> **核心机制 100% 亲自理解，关键代码亲手实现一次；完整项目允许 AI 写 60%～80%，但关键数据流、架构决策、Debug 和 Review 必须是你自己完成。**

这样你既不会退回到“2020 年式纯手撸学习”，也不会陷入“AI 帮我做了十个项目，我一个都讲不明白”的另一极端。

而且对于你现在想走 **Agent 开发实习** 这条路，这种方式其实比“疯狂背 LangGraph API”更合适。面试真正问深一点的时候，最后还是会回到：**State 为什么这么设计、Tool Calling 怎么跑、Agent Loop 怎么结束、Memory 怎么存、错误怎么恢复、为什么选这个架构。** 能讲清楚这些，你才是真的会。