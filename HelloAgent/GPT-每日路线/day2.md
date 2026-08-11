[question]
1. ReAct 为什么叫 Reason + Act？
2. Thought、Action、Observation 分别是什么？
3. 为什么 Observation 必须加入 History？
4. while current_step < max_steps 为什么必须存在？
5. LLM 输出 Search[xxx] 后，是怎么一步一步变成真实 Python Tool 调用的？
[answer]
1.因为
2.Thought是大模型的思考过程，Action是大模型要调用工具时的行动说明，observation是在模型调用工具时候工具带回来的参数的观察，这三个关键机制合成了一个ReAct机制
3.因为需要把observation输出到llm的上下文环境中，这样才能保证llm的可执行性
4.