# AI项目课堂笔记

    软件测试 昨天修改 AI速览试用
    本文讨论了AI项目的相关知识，涵盖前置知识、业务与测试、RAG原理及测试、Milvus向量数据库、RAGAS框架、项目业务...

## 两个阶段

## 1.AI项目前置知识

    - a.大模型基础认识
    - b.大模型提示词工程
    - c.NLP核心知识
    - d.RAG（检索增强生成）原理
    - e.RAGAS--RAG系统的评测框架

## 2.AI项目业务&测试

    - a.AI项目的业务逻辑
    - b.AI项目的技术栈&实现逻辑
    - c.AI项目测试点&测试用例
    - d.AI项目测试报告
    - e.AI项目简历&面试题

## 1.大模型基础认识

### 1.1AI和AGI（了解）

AI：“窄域人工智能”，专注于特定的领域的任务（比如：图像识别，语音识别，推荐系统）AGI："通用人工智能”，可以去学习任何知识，处理任何任务，具备与人类相当或者超过人类的智能，不限定于特
    定的领域

### 1.2Token的概念以及测试

## 1.什么是Token

在大模型眼中，文字不是以"字"或者词"为单位，而是划分为一个个的Token
        定义：Token是模型处理文本的最小的单位。可以是一个完整的单词（apple），也可以是一个词缀
        （ing），甚至是一个标点符号或者空格。
中英文Token区别
- 英文
    - 通常1个Token=0.75个单词（4个字母左右）
```python
"unbelievable":["un","believ","able"]---->3个Token
```

    中文
    中文的情况比较复杂。早期的模型就是一个字一个Token。但是现在的发展，比较新的大模型可以把一些常
        见的词组组合成一个Token
    “人工智能”：早期可能就是拆分为["人"，"工”，"智”，能"]--->4个Token。如果现在的一些大模型训练的词表可
        能被拆分为["人工"，"智能]--->2个Token
    中文语境下1Token对应大概1.5到2个汉字（不同的模型差异比较大）

## 2.测试为什么关注Token

## 1.成本与配额测试

计费模式：大多数的LLMAPI（OpenAI，阿里云.）都是按照"输入Token"+"输出Token"进行收费。一般来
    讲“输出Token"会比"输入Token"贵2-3倍
    验证提示词是否过长造成不必要的Token的浪费
    监控异常的场景：如果程序陷入死循环，或者模型产生胡言乱语“导致无线生成，Token消耗会瞬间爆炸。
        测试人员这种情况应该确保有截断机制和预算警报

## 2.性能与延迟测试

Token的数量直接决定响应速度首字延迟（TimetoFirstToken---TTFT）：用户看到第一个字的时间。InputToken（输入的token）越多，预处
    理时间越长，首字延迟越慢生成速度：outputToken（输出Token）越多，生成速度越慢
    - 建立Token数量和响应时间的基准线
    - 高并发下，大Token请求是否会造成阻塞或者超时

### 1.3概率生成与温度（temperature）

## 1.概率生成的本质

大模型本质上就是一个概率预测机器。当你输入一句话的时，模型并不是直接知道下一个字是什么，而是：

## 1.计算概率：根据上下文，计算词表中每一个可能的Token作为下一个字的概率分布

## 2.采样选择：从这个概率分布中抽取”一个Token作为输出

## 3.循环迭代：将选中的Token加入上下文，重复上面的过程，直到生成结束

这意味着：相同的输入，在不同的随机Token选择下，可能得到不同的结果

## 2.温度（temperature）的作用

Temperature参数就是在模型进行采样选择之前，对原始的概率分布进行平滑或者锐化的处理，可以改变每个候选词被选中的概率
        temperature：0-1，有些模型也可以设置1以上
```python
t=0：确定性，概率最高的词被选中的概率趋近100%，其他的词趋近0%。一般在数学解题，事实查
```

        询，需要绝对准确，不允许幻觉
        0<t<0.7，保守模式，高概率的词的概率被选中的概率更高，低概率的词几乎没有机会。客服系统，
        摘要总结，比较专业性的场景

### 0.7<=t<=0.9，平衡模式（一般大模型默认），保持一定的随机性，但是主要仍围绕高概率的词。日

        常对话，通用助手。
        T>=1发散模式，拉平概率的分布，原本只有1%的概率的词，有可能就有10%的概率被命中。文学创
        作，头脑风暴，需要意想不到的灵感。

## 3.temperature与其他参数的配合

## 1.Top-k:

    - a.只在概率最高的K个词中进行采样
    - b.直接剔除大量的低概率词
    - c.作用：防止高温下出现不通顺词

## 2.Top-p:

    - a.只累积概率总和达到P（0.9）的这部分词作为候选词，动态的调整候选词的数量
    - b.作用：比Top-K更加灵活，既可以保证多样性，又避免了极低概率的产生

        为什么叫温度（temperature）
        - 这个概率借用的物理学中的热力学概率
            低温：分子运动缓慢，系统趋于能量最低的稳定状态（最有可能的）
            - 高温：分子剧烈运动，系统充满能量，更容易跳跃到高能的词（低概率的词），表现出混乱
            - 的情况

## 4.测试人员关注

## 1.一致性测试

    - a.对于功能型的任务（提取json某些字段，生成sql），必须设置t=1或者比较低的温度（根据实际的业务情
        况），确保多次运行结果的一致

## 2.幻觉率评估

    - a.高温度（temperature）下，模型编造事实的概率增加，需要测试不同的温度（temperature）下的事实准确
        性

## 3.边界值测试

```python
a.测试t=0，t=0.8，t=1，t=1.1需要测试不同的温度下包括超过范围的值，验证API是否正确的拦截非法的参
```

        数

### 1.4上下文窗口

## 1.什么是上下文窗口

上下文窗口指的是模型在推理的过程中能够同时处理的最大Token数量（输入的Token+输出的Token）常见模型规格：8K，32K，128K等等..
    机制：大模型只能看见”上下文窗口"内的内容，一旦超过，旧的内容就会被"遗忘”
        1.遗忘机制
            当对话的内容超过窗口的限制，模型并不是”崩溃”，而是会丢弃最早的消息
            场景：上下文窗口是8k，现在记录了10轮对话，刚好用完了8k。当我们进行第11轮对话的时
                候，这个时候模型看到的上下文窗口就是第2轮到第11轮”，第一轮的内容就会遗忘
            后果：我在第1轮的时候就设置了很重要的规则（请使用文言文回答），在长对话之后这些规则
                就被挤出来窗口，模型就会突然变回白话文
        2.窗口并不是越大越聪明
            - 注意力分散：虽然大的上下文窗口可以让模型看到更多的数据，但是如果关键信息隐藏在海量的数
            据中，模型可能会出现大海捞针”的情况，会可能遗漏掉关键的内容
            成本与速度：窗口越大，能够一次记住内容更多，哪些一次处理的时间就会更长，速度会变慢。每
            次处理都在消耗token，api的调用费用也会增加

## 2.测试人员关注

## 1.极限长度的测试

    - a.构造接近上下文窗口（8k）的数据，验证系统的响应时间还有显存占用
    - b.验证超过窗口限制的时候处理的策略，是报错，还是截断

## 2.多轮对话记忆测试

    - a.在长对话场景中，测试大模型是否能记住第一轮设定的约束条件

## 3.性能衰减测试

    - a.监控随着Token数量的增加，首字生成时间和每秒生成的Token数的变化曲线。通常上下文窗口越大，推理
        的速度就越慢

## 2.大模型提示词工程

详细的大模型的提示词工程在基础课程里面，这里只讲核心的大模型提示词知识，详细内容在这里就不做赘述。

### 2.1为什么提示词是测试的核心

原因：在AI项目中，提示词就是“测试用例”。提示词的质量就决定了我们能发现多少大模型的缺陷传统测试VsAI项目测试
    传统测试：输入是确定的（点击某个按钮，API参数），输出也是确定的（页面提交，页面跳转，返回状态
        码）。测试用例/测试脚本都是有明确预期结果的
    AI项目测试：输入是自然语言（提示词），输出是有概率性的、开放的文本数据。提示词本身也是动态的，
        可变的

### 2.2提示词的基本框架

## 1.角色定位--告诉AI专业的身份

目的：消除语境的歧义，引导AI使用专业的特定的领域知识场景：你是一个有10年经验资深软件测试工程师

## 2.任务结构化--拆解任务目标

    目的：把复杂的需求分解成ai便于理解和执行的步骤
    分布引导，让AI的思考和你的思考方向同步
    场景：请根据以下的需求生成测试用例
    首先，列出该需求的所有的测试点
    然后，为每一个测试点生成一个正向的测试用例
    然后，为每一个测试点生成至少5条异常的测试用例
    最后，如果存在输入框之类的限制的需求，需要进行等价类+边界值结合设计测试用例

## 3.约束上下文

    目的：让AI输出有效的，并且符合要求的内容
    可以过滤掉大量无关的信息，直接产出符合要求的文件场景：请以excel的形式输出，包含测试用例id，测试场景，前置条件，测试步骤，预期结果，优先级

## 4.送代优化

目的：很少有提示词可以做到一次性就是完美的。我们可以根据AI的输出结果进行诊断和修正场景：请根据之前的用例，再补充"安全测试"方面的用例，最后汇总输出给我

## 3.NLP核心知识与测试

### 3.1什么是NLP

AI和语言的交叉领域，让计算机可以来理解、生成和处理人类的自然语言（中文，英文）
    自然语言理解（NLUNatureLanguageUnderstaning）
        让机器能够读懂输入的内容
            - 例子：意图识别（用户是想要查询天气还是订机票），实体抽取（人，地，物）
    自然语言生成（NLGNatureLanguageGeneration）
        让机器写出或者说出“符合人类习惯的内容
            - 例子：聊天机器人，代码生成，自动摘要
```python
NLP=自然语言理解+自然语言生成
```

### 3.2分词与文本预处理

分词：将连续的自然语言文本切分为模型可以理解的单元（Token）
    中文难点：中文没有天然的空格分隔，分词的颗粒度就直接影响语义
    LLM分词器：现在很多的大模型都是使用BPE或者WordPiece算法，能够去动态的组合常见的词组。但是如果
        遇到生僻字或者特殊符号仍然可能存在问题文本预处理：大小写转换，去除停用词，去除HTML标签分词测试关注

## 1.分词边界测试

    - 场景：输入包含专业术语，新的造词，二义连续短句
    测试用例：“重庆市长江大桥”
        - 重庆市长江大桥
        重庆市长江大桥

## 2.特殊字符

    - 场景：输入的内容包括Emoji、乱码，多余换行符，空格
    预处理要做到能够清洗掉这些不需要的特殊字符

## 3.多语言的混合测试

    - 场景：中英文混用、代码和文本混合
    分词器要能够正常识别预约的边界

### 3.3命名实体识别（NER）

命名实体识别指的是从连续性的自然语言中识别出有特定意义的实体，并且把这些实体进行分类。
简单来讲，就是让计算机读一段话，然后回答这段话里面提到了哪些人？哪些地方？哪些组织？哪些时间？
        NER通常包含两个步骤
        - 检测：找到文本中哪些词或者短语是实体
        - 分类：判断这些实体属于什么类别
        怎么评估？
        - 精准率：模型识别出的实体中，有多少是真的实体？（避免误报）
            - 例如：一个文本中，大模型识别出10个人名，但是实际上只有9个是真的人名，精准率就是90%
        召回率：文本中所有的真实实体，模型找到多少？（避免漏报）
            - 例如：一个文本中，一共有10个人名，但是大模型只找到9个，召回率就是90%
        F1-score：精准率和召回率的调和平均数，也是衡量NER最常用的综合指标
            公式：2×召回率×精准率/召回率+精准率NER测试关注

## 1.实体边界准确性

    用例：我明天要去北京首都国际机场
    - 检查：模型提取的是”北京”，“首都国际机场”，还是“北京首都”，“国际机场”

## 2.嵌套实体与歧义

    - 用例：我今天吃了一个苹果VS苹果发布了新款的手机
    - 检查：模型是否能区分出每一个"苹果的"分类

### 3.4语义相似度和向量空间

高维：更多的坐标来表示是一个高维空间（2048维）

NLP通过深度学习模型，将单词，句子甚至是整段文本映射到一个高维向量空间在这个高维空间中，每个文本都是一个点（向量）---后面我们会专门讲向量数据库
    关键：这个映射不是随机的，而是基于语义的学习。语义相似的文本在向量空间中的位置会很近
        核心概念：
        - 向量嵌入：将文本映射为高维空间中的向量，语义相近的文本在空间中距离更近
        相似度计算：常用的是余弦相似度（在后面向量数据库也会讲到），值越接近1表示语义越相似
        RAG检索，语义搜索，重复文件检测等等领域都会使用到语义相似度测试关注

## 1.语义匹配和关键词匹配

    用例：
        客户问题：怎么重置密码？
        关键词匹配：密码重置流程
        - 语义匹配：我忘记了我的登录密码，怎么恢复？

## 2.负样本测试

    - 用例：
        苹果多少钱一斤？
        苹果股票多少钱一股？
            - 从逻辑讲该两个问题相似度很低。如果被匹配到了，就证明Embedding模型（向量嵌入）区分度不足

## 3.多语言对齐测试

    - 用例：
        中文：你好
        英文：hello
            - 跨语言检索是必测项

### 3.5意图分类

意图分类是自然语言处理中一个很关键的任务，主要用于对话系统（聊天机器人，智能助手，智能客服....）具体会分为哪些类别，根据项目的实际业务情况来
    核心目标就是分析用户的输入（文本&语音），判断用户想要做什么或者达到什么目的，并将其归类到预定义的
    类别的
        意图分类和实体识别的关系：
        意图分类解决的是“做什么”
        实体识别解决的是”谁做”，“对谁做”，“什么时间做”，“什么地点做”
        例子：帮我设置明天早上8点钟的闹钟
            意图：设置闹钟
            实体：明天早上8点钟意图识别测试关注

## 1.明确意图测试

    - 用例：帮我订一张明天去三亚的机票
        意图预期：预订机票

## 2.模糊意图测试

    用例：“我想去看看”（未指明想看什么）
        - 意图预期：应该归类到需要澄清"或者直接触发"追问机制”，不应该强制归类为某个具体的业务

## 3.拒识测试

    - 用例：在一个航天客服的项目中，问今天超时鸡蛋打折吗”
    - 意图预期：模型应该识别为问题超出范围”，礼貌性进行引导回业务领域，而不是胡乱回答

## 4.对抗样本测试

    用例：我不想要你们这个垃圾产品了，赶紧给我退了
    意图预期：即使包含负面的情绪的词汇，意图仍然应该识别退货，而不是其他的一些闲聊”

### 3.6指代消解

含义：模型识别出句子中的"代词”或者省略语”具体是指的前文那个“实体”
        如果大模型没有这个能力，或者能力较差，就会出现模型像是一个记忆力极差的人，听到后面的就忘记前
        面的内容，无法去理解上下文的逻辑
        核心概念：
        - 指代：说话人用简短的词（如他”、“它”、“这个”、“那里”）来替代之前提到过的具体的名词
            一轮对话：我想去北京旅游，你能帮我订票吗？
            - 二轮对话：我如果去那里旅游，我要注意什么
        消解：模型通过推理，把这些简短的词还原成具体的名词，从而理清逻辑关系指代消解测试关注

## 1.人称代词消解

    用例：张三告诉李四他错了-->他"指的是谁

## 2.省略句补全

    - 用例：
        用户：北京天气怎么样
        模型：北京晴天
        - 用户：那重庆呢？
    预期：模型应该直接补全为那重庆的天气呢”，并且最后给出正确的回答

## 3.长距离的依赖测试

    用例：在第1轮对话中提到一个实体”，在第10轮用代词只带它
    风险：随着上下文边长，指代消解准确率通常会下降。测试的是模型的"记忆保持“的能力
        通常项目中要给出具体的需求要记住几轮

## 4.RAG（检索增强生成）核心原理&测试实战

## 1.什么是RAG

RAG（Retrieval-AugmentedGeneration）检索增强生成的缩写。
目前RAG是大模型应用中最主流，最核心的架构模式之一。
        因为大模型回答问题，很多时候其实不能够知道应该怎么回答（在具体的业务领域）。会出现大模型
        幻觉
        RAG就是给大模型装一个外挂知识库”，大模型回答问题之前先去知识库里面搜索相关的内容。然后再

        结合搜索到信息来智能生成回答。

## 2.软件测试工程师需要理解的概念

Enbedding（向量化）：理解向量化的本质，测试语义匹配效果
    切片：掌握切片策略以及不同的策略对于检索精度的影响，测试边界情况
    相似度度量：验证检索排序算法的准确性
    查询改写：测试用户模糊的提问的优化效果
    向量检索：验证召回率（Recall）和准确率（Precision）

## 3.Embedding（向量化）的本质

Embedding的本质就是将文本、单词、图像、视频等非结构化的数据映射为高维空间中的向量坐标的过程常见的维度有768/1024/1536/2048。维度越高就代表表达能力越强。但是维度越高，计算就越复杂，存储的成
    本越高在很多时候，AI的项目测试，向量化这个过程会占据很长的时间向量化测试关注

## 1.语义一致性测试

    - 用例：输入同义词（开心"和"高兴"）、上下位词（狗"和"动物"）、多义词（"一斤苹果"和"苹果公司”）
    - 预期：计算余弦相似度，同义词相似度应该>=0.8；多义词在不同的环境下应有显著区分

## 2.多语言测试

    - 用例：中文的"你好”，英文的"hello”
    - 预期：高质量的多语言Embedding模型应该是两个向量非常接近，支持跨语言检索

## 3.新词测试

    - 场景：输入公司特定的缩写，新造词
        用例：字节跳动（同学）
    预期：观察模型是否能根据上下文推断向量位置

## 4.长度敏感测试

    部分的模型对于长文本的Embedding效果衰减严重
    用例：给较长的文本给到模型进行向量化
    预期：对于短句和长文本的检索的向量质量向量化过程代码实现
        后面讲到向量数据库的时候会详细的讲到关于向量数据库的操作和计算，这里提前给大家看下向量化的过
        程。操作的步骤如下：
        连接向量数据库--->加载本地Embedding模型--->创建集合--->读取csv文件--->在向量数据库中插入数据
    代码块
        importos
    2 import pandas as pd
    3 import logging
    4 from typing import List,Dict,Any
    5 from sentence_transformers import SentenceTransformer
    6 from pymilvusimport（
    7 connections,
    8 Fieldschema,
    9 CollectionSchema,
    10 DataType,

11 Collection,12 utility,13 MilvusException14)1516 #配置日志
```python
17 1ogging.basicConfig(level=logging.INFo,format='%（asctime)s-%（levelname)s -%（message)s')
18 logger=logging.getLogger(__name__)
```

192021 class FAQVectorStore:
```python
22 def__init__(self,
```

23 host:str='123.60.46.254',24 port:str='19530'25 user:str='root',26 password:str='Mv@Bmc2026#X9kR'
```python
27 collection_name:str='ecommerce_faq'，
28 model_Local_path:str='./models/paraphrase-MiniLM-L6-v2'):
```

29 self.host=host30 self.port=port31 self.user =user32 self.password= password
```python
33 self.collection_name= collection_name
34 self.model_local_path=model_local_path
```

35 self.model=None36 self.collection =None37 self.dimension=038
```python
def connect（self):
```

40 try:
```python
41 logger.info（f"正在连接Milvus（(self.host}:{self.port}）...")
```

42 connections.connect(43 alias="default",44 host=self.host,45 port=self.port,46 user=self.user,47 password=self.password4849 logger.info（“Milvus连接成功。“）50 except MilvusException ase:
51 logger.error（f"连接Milvus失败：{e}"）52 raise53
```python
54 def load_model(self):
```

55 "从本地路径加载嵌入模型
```python
56 logger.info（f"正在从本地加载模型：{self.model_local_path}
```

57
```python
58 ifnot os.path.exists(self.model_local_path):
59 raiseFileNotFoundError（f"模型路径不存在：{self.model_local_path}\n请先手动下载模型文
```

6061 try:
```python
62 self.model=SentenceTransformer(self.model_local_path)
63 dummy_embedding=self.model.encode（["test"])
64 self.dimension =len（dummy_embedding[e])
```

65 logger.info（f"本地模型加载完成，向量维度：{self.dimension}"）66 except Exception as e:
67 logger.error（f"本地模型加载失败：{e}"）68 raise69
```python
70 def create_collection(self):
71 ifutility.has_collection(self.collection_name):
72 logger.warning（f"集合{self.collection_name}已存在，正在删除以重建..."）
73 utility.drop_collection（self.collection_name)
```

7475 fields=[

```python
76 FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
77 FieldSchema(name="question",dtype=DataType.VARCHAR,max_length=65535),
78 FieldSchema(name="answer",dtype=DataType.VARCHAR,max_length=65535),
79 FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=self.dimension)
```

    80
    81
```python
82 schema=collectionSchema（fields=fields，description="电商常见问题知识库"）
83 self.collection =Collection(name=self.collection_name,schema=schema)
84 logger.info（f"集合{self.collection_name}创建成功。"）
```

    85
    86 #【修改点1/2】：将metric_type 改为“cosINE”
```python
87 index_params={
```

    88 "metric_type":"cosINE"

## 4.切片策略

切片是一个预处理步骤。是RAG系统中最关键也是最容易忽视的步骤
    它核心的任务就是：将长篇的文档（pdf，word，网页）切割成一个个大小适中，语义完成的小块，以便后
        续进行向量化（Embedding）和检索

### 4.1为什么要切片

## 1.上下文窗口限制

    - 大模型输入的长度是有限的。如果文档很大，上百兆，根本塞不进去

## 2.大海捞针效应

    - 输入的内容过长的时候，大模型容易忽略中间的信息，只注重了开头和结尾
        比如把整本《员工手册》都喂给大模型，但是可能就会找不到关于"报销”，“请假"的具体的规定

## 3.检索精度下降

    Embedding向量化代表的是整体语义
        - 如果说切片很大，向量就会稀释掉，会导致检索的时候匹配不准
        - 如果切片太小也不行，因为可能会丢失上下文，模型不懂在说什么
切片需要找到黄金平衡点”--每个切片既要包含足够的信息让模型理解，又要足够小，保证检索的精度（开发+测试+产品+业务方进行沟通）

### 4.2切片常见的策略（开发）

固定字符/Token切片：每200Token切一刀。简单但是可能切断语义（实际工作中很少使用）递归字符切片：优先按照段落、句子、空格切片。尽量保证完整语义语义切片：先利用大模型判断语义转折点，然后进行切割（精度比较高，但是成本也高）父子索引：检索小切片，但是将对应的大切片送入大模型生成答案，兼顾检索精度与上下文完整性

### 4.3切片测试关注

## 1.语义断裂测试

    - 用例：公司的核心价值观是诚信与创新。被切分为"公司的核心价值观”，“是诚信和创新”
    - 测试系统是否应该进行语义的补全或者避免断裂

## 2.元数据保留测试

    - 切片后是否保留来源文件的文件名、页码、章节标题这些元数据
    引用溯源的基础

## 3.特殊格式的处理

    - 源文件中存在表格、列表、代码块
    特殊格式比如表格之类的不应该被拆散，代码块要保持缩进和完整性。
    测试需要覆盖pdf中复杂的排版解析（根据实际业务方的文档）

## 5.相似度度量

相似度度量就是RAG和向量检索的"尺子”
    当你的提问被转化为向量的时候，知识库里面文档也被转化为向量，就需要有一个数学方法来判断这两个
        向量在多维空间中距离有多近”
    离得越近，代表语义越相似，相关性越高。
    距离=0完全相同
        相似度=1完全相同
        相似度=0毫无关系
        相似度<0意思相反（只会在某些模型中出现）

## 1.三种最常用的度量方法

## 1.余弦相似度（最主流/推荐）

    原理：计算两个向量之间夹角的余弦值cOS。只关心方向是否一致，不关心向量的长度
            Cosine Similarity= A·B ZA;B;
                                        ||A||IB|I VZ=AVZ=B²

## 2.欧几里得距离

    - 计算亮点在空间中的直线距离（勾股定理多维推广）
                                                                    n
```python
EuclideanDistance=||A-B= C（Ai-Bi)²
```

## 3.点积

    - 两个向量对应的元素相乘之后求和
                                                            n
```python
DotProduct=A·B A;B
i=1
```

        以上的内容是原理，公式大家看一下就好了，不用记忆。
        因为在代码里面都是已经实现好的库，我们只用传参即可。

## 2.代码实现

    代码块
```python
#metric_type：cosINE 表示余弦相似度
```

    2 #metric_type：L2表示欧几里得距离
    3 #metric_type：IP表示点积
```python
4 index_params={
```

    5 "metric_type":"cosINE",
```python
6 "index_type":"IVF_FLAT",
7 "params":{"nlist":128}
```

    8 }
```python
6 self.collection.create_index(field_name="vector",index_params=index_params)
```

    10
    11
    12 #注：创建集合的时候采用什么相似度度量，那么取值的时候也是采用同样的相似度度量

## 3.相似度度量测试关注

## 1.阔值设定测试

    - 场景：设定相似间值（0.7），低于0.7的就不返回
    - 测试：调整值，观察查准率，查全率的变化

## 2.排序稳定性测试

    - 用例：相同的问题，进行多次检索
    - 预期：TopK结果的顺序应该保持一致

## 3.负样本测试

    - 预期：前者的得分一定是显著高于后者。如果得分接近，就证明向量模型的区分度不足

## 6.查询改写

将用户的问题发送给向量数据库进行检索之前，先让大模型把这个问题“翻译”或"优化”一下，让问题成为更适合
    进行检索的版本技术
    拼写纠错：把用户的错别字纠正
    同义扩展：将"咋办扩展为"如何解决”，“解决方案是什么”
    指代消解
        一轮：这个ipone16有哪些配色
        二轮：它多少钱
            - 改写：iPhone16多少钱
    假设性问题生成
        先让大模型生成一个假想的答案，然后再用该答案的向量去进行检索（检索答案的语义相似度）查询改写测试关注

## 1.多轮对话改写测试

    - 用例：
        一轮：华为Mate60发布了吗
        二轮：他有哪些配色
        三轮：他有几个版本
        四轮：发售价是多少
    预期：系统应该把他”，或者没有的指代情况下加上"华为Mate60"的前缀

## 2.过度改写测试

    风险：改写之后的问题偏离原意
    用例：
        问题：老板不在家怎么办
            - 改写：“家庭保姆招聘流程”
    预期：改写应该保留核心意图，测试需要对比改写前后的语义相似度

## 3.空查询和无效查询的处理

    - 用例

        问题：嗯嗯，呵呵，你好。。。
        预期：改写模块应该识别并拦截，直接返回闲聊回复，不需要去检索知识库

## 7.向量检索

## 1.向量检索和关键词检索对比

向量检索是RAG系统中的核心引擎
    可以在海量的文档中，找到和用户语义最相似的内容，而不仅仅是字面匹配特性 关键词检索 向量检索原理 匹配相同的字词（SQL中的like，ESTerm） 匹配语义含义（基于向量空间距离）案例 搜索”手机”，只能找到”包含手机"的文本 搜索”手机”，能找到"iPhone”“智能电话”、“移动电话”弱势 无法处理同义词、错别字 对精确的数字、专业名词匹配稍弱（需要配合关键词搜
                                                                索）底层技术 倒排索引 向量索引RAG角色定位 辅助 主力（负责理解意图）

## 2.向量检索的工作流程

- 在RAG系统中向量检索分为两个阶段：入库阶段，查询阶段
阶段一：入库阶段文档切片：将PDF/Word文档切为小块向量化（Embedding）：调用Embedding模型，把每个文本都转换为一个高维向量
    [-0.028643812984228134,.....,0.047197017818689346,0.041706282645463943]阶段二：查询阶段用户提问：收到衣服尺码不对咋办
    问题向量化：用同一个Embedding模型，把这个问题也转换为高维向量
    [-0.028643812984228134....,.0..047197017818689346,0.041706282645463943]
    因为和入库阶段的Embedding模型相同，语义相似的文本在向量空间坐标会非常接近
    相似度计算：向量数据库计算“问题向量"在库中与所有的”文档向量”的距离（通常使用余弦相似度）Top-K返回：找出最相似的K个文本（比如Top-10），返回给大模型

## 3.向量检索测试关注

## 1.召回率（Recall）测试

    - 方法：造数据，把我们已知答案的数据集准备好，然后写入到向量数据库
    - 指标：标准答案是否在Top-K中
    - 重点：RAG系统中，召回率比精准率更加重要，只要正确答案在候选列表中，大模型通常都能提炼出来
        如果压根就没有召回，没在Top-k中，必挂

## 2.索引构建和更新测试

    - 场景：新增文档之后，多久可以被检索到（实时性）
    - 测试：根据公司实际的业务情况来（实时，队列-可能有点延迟，定时任务）

## 3.混合检索测试

    - 策略：向量检索+关键词检索
    - 场景：专有名词（SR-71，XT5..）向量检索可能会失效，需要靠关键词检索

        需要测试包含有一些专有名词（业务情况）进行混合检索的情况

## 8.重排序

RAG重排序是检索增强生成的精筛"环节
    先通过向量检索快速召回一大批（Top20，Top50..）相关的文档，然后使用一个计算量更大，更精准的模型，
    对这批文档进行二次打分和排序最终选择最相关的Top-K（Top-3Top-5）送给大模型生成答案

## 1.重排序和向量检索对比

特性 向量检索模型 重排序模型工作方式 双塔结构：分别计算"问题向量"和"文档向量”，然后计算相 单塔结构：把"问题"和"文档"直接拼接在一起，输入大模型，大模型给
            似度 出相关性分数输入格式 Embedding（问题）Embedding（文档） 模型请注意，这是开头[CLS]，接下来是用户的问题，问题结束了
```python
[SEP]，接下来是候选文档，文档结束了[SEP]。请你综合理解这两段话
```

                                                                的关系，并根据[CLS]的状态告诉我有多相关。
```python
开头[CLS]问题[SEP]文档[SEP].
```

交互深度 浅层交互：只是在最后一步来计算距离 深度交互：利用的是Transformer的注意力机制，让问题的每个字都文
                                                                档做交互速度 极快：百亿级别，千亿级别的数据做快速搜索 慢：每一对（文档，问题）单独跑一遍模型。所以只适合少量数据精筛精度 中 极高角色 海选 决赛

## 2.重排序测试关注

## 1.排序提升测试

    - 对比重排序之后标准答案的排名变化
    预期：相关文档的排名应该显著上升

## 2.噪声过滤测试

    - 场景：向量检索出来Top-20，其中有10个是弱相关
    - 预期：重排序的时候，弱相关的文档应该直接排到后面或者直接截断

## 3.延迟成本评估

    - 指标：重排序对于耗时的增加
    预期：如果重排序提升排名不明显，但是延迟增加很多，需要评估是否值得上线（根据实际的业务情况来
        定）

## 5.Milvus向量数据库

Milvus是一款开源的云原生的向量数据库，专门为大规模相似度搜索设计
    - 支持PB级别的数据
    - 毫秒级查询

## 1.环境配置

库名 版本 用途说明pymilvus >=2.4.0 是milvus官方的pythonSDK，用于连接数据库、建表、增删查改sentence_transformers >=2.2.0 用于加载paraphrase-MiniLM-L6-v2模型，将文本转为向量（Embedding）

sepued >=1.3.0 用于读取和处理CSV文件
    代码块
        pip install pymilvus sentence_transformers pandas

## 2.Milvus连接配置&环境初始化

连接是所有数据操作的基础
- 第一步需要和Milvus服务器建立连接
第二步加载本地的sentence_transformers模型
    代码块
    1 -*-coding:utf-8-*
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeicesht
    4
    5 from sentence_transformers import SentenceTransformer
    6 from pymilvus import connections,utility
    7
    8
    9 #配置区域
    10 MILVUS_HOST="123.60.46.254"
    11 MILVUS_PORT="19530"
    12 MILVUS_USER="root"
    13 MILVUS_PASSWORD="MV@BmC2026#X9kR"
```python
14 MILVUS_MODEL_PATH="../models/paraphrase-MiniLM-L6-v2"
```

    15
    16
    17 print（"目前正在连接milvus数据库"）
    18 #1.连接miLvus
```python
19 connections.connect(host=MILVUS_HoST,port=MILVUS_PORT,user=MILVUS_USER,
20 pasSWord=MILVUS_PASSWORD)
```

    21
    22 print（"milvus数据库连接成功，接下来加载本地模型"）
    23
    24 #2.加载模型
```python
25 SentenceTransformer（MILVus_MODEL_PATH,device=’cpu'） # 可以改为 cuda 使用GPU
```

    26
    27 print（"本地模型加载完成"）

## 3.Milvus建库建表

Schema：是向量数据库的一个概念，可以理解为关系型数据库中的"表结构”
    Field：对应可以理解为关系型数据库中的字段”
    DataType：对应可以理解为关系型数据库中的数据类型”
    代码块
    1 -*-coding:utf-8-*
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4
    5 #建库建表（createcoLLection）
    6
    7 #-*-coding:utf-8-*
    8 #北梦测教育
    6 #课程咨询加微信：xiaobeiceshi
    10
    11 from sentence_transformers import SentenceTransformer

    12 from pymilvus import connections,utility,Fieldschema,CollectionSchema,DataType,Collection
    13
    14
    15 #配置区域
    16 MILVUS_H0ST="123.60.46.254"
    17 MILVUS_PORT="19530"
    18 MILVUS_USER="root"
    19 MILVUS_PASSWORD="Mv@Bmc2026#X9kR"
```python
20 MILVUS_MODEL_PATH="../models/paraphrase-MiniLM-L6-v2"
```

    21
    22
    23 print（“目前正在连接mi1vus数据库"）
    24 #1.连接miLvus
```python
25 connections.connect(host=MILVUS_HoST,port=MILVUS_PORT,user=MILVUS_USER,
26 passWord=MILVUS_PASSWORD)
```

    27
    28 print（“milvus数据库连接成功，接下来加载本地模型"）
    29
    30 #2.加载模型
```python
31 SentenceTransformer（MILVuS_MODEL_PATH,device=cpu')#可以改为 cuda 使用GPU
```

    32
    33 print（“本地模型加载完成"）
    34
    35
    36
    37 print（"="*100)
    38
    39 #配置区
```python
40 COLLECTION_NAME="faq2_crud"
```

    41 DIMENSION=384 #模型的向量维度
    42
    43 #1.检查模型是否存在
    44 print（"1.判断集合是否存在，存在的情况进行删除处理"）
```python
45 ifutility.has_collection(COLLECTION_NAME):
46 utility.drop_collection(CoLLECTIoN_NAME)
```

    47
    48 #2.字段定义
    49 fields=[
```python
50 FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
51 FieldSchema(name="question",dtype=DataType.VARCHAR,max_length=65535),
52 FieldSchema(name="answer",dtype=DataType.VARCHAR,max_length=65535),
53 FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=DIMENSION),
```

    54]
    55
    56 #3.创建Schema
```python
57 schema=CollectionSchema（fields=fields,description="电商FAQ知l识库")
```

    58
    59 #4.创建集合
```python
60 collection = Collection(name=COLLECTION_NAME,schema=schema)
```

    61
    62 print（"集合和schema创建完毕"）
    63
    64 #5.创建索引
```python
65 index_params={
```

    66 "index_type"："IVF_FLAT"，#表示倒排文件索引l，通过聚类加速搜索
    67 "metric_type":"cosINE", #COSINE表示使用余弦相似度计算
```python
68 "params":{"nlist":128} #聚类数量越大越准越慢越小越快可能漏检
```

    69 }
```python
70 collection.create_index（field_name="vector",index_params=index_params)
```

    71 #索引创建成功
    72 print（“索引l创建成功")

## 4.Milvus数据插入

代码块1 #-*-coding:utf-8-2 #北梦测教育3 #课程咨询加微信：xiaobeiceshi45 #建库建表（createcoLLection）67 #-*coding:utf-8-*8 #北梦测教育9 #课程咨询加微信：xiaobeiceshi1011 from sentence_transformers import SentenceTransformer12 from pymilvus import connections,utility,FieldSchema,CollectionSchema,DataType,Collection131415 #配置区域16 MILVUS_H0ST="123.60.46.254"17 MILVUS_PORT="19530"18 MILVUS_USER="root"19 MILVUS_PASSWORD ="Mv@Bmc2026#X9kR"
```python
20 MILVUS_MODEL_PATH="../models/paraphrase-MiniLM-L6-v2"
```

212223 print（“目前正在连接milvus数据库"）24 #1.连接miLvus
```python
25 connections.connect(host=MILVUS_HOST,port=MILVUS_PORT,user=MILVUS_USER,
26 passWord=MILVUS_PASSWORD)
```

2728 print（“milvus数据库连接成功，接下来加载本地模型"）2930 #2.加载模型
```python
31 model=SentenceTransformer（MILVUS_MoDEL_PATH,device='cpu'）#可以改为 cuda 使用GPU
```

3233 print（“本地模型加载完成"）34353637 print（"="*100）3839 #配置区
```python
40 COLLECTION_NAME="faq3_crud"
```

41 DIMENSION=384 #模型的向量维度4243 #1.检查模型是否存在44 print（"1.判断集合是否存在，存在的情况进行删除处理"）
```python
45 ifutility.has_collection(COLLECTION_NAME):
46 utility.drop_collection(COLLECTION_NAME)
```

4748 #2.字段定义49 fields=[
```python
50 FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
51 FieldSchema(name="question",dtype=DataType.VARCHAR,max_length=65535),
52 FieldSchema(name="answer",dtype=DataType.VARcHAR,max_length=65535),
53 FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=DIMENSION),
```

54]5556 #3.创建schema
```python
57 schema=CollectionSchema（fields=fields,description="电商FAQ知识库")
```

5859 #4.创建集合
```python
60 collection=Collection(name=COLLECTION_NAME,schema=schema)
```

6162 print（"集合和schema创建完毕"）63

    64 #5.创建索引
```python
65 index_params={
```

    66 "index_type"："IVF_FLAT"，#表示倒排文件索引l，通过聚类加速搜索
    67 "metric_type":"cosINE", #COSINE表示使用余弦相似度计算
```python
68 "params":{"nlist":128} #聚类数量越大越准越慢越小越快可能漏检
```

    69
```python
70 collection.create_index（field_name="vector",index_params=index_params)
```

    71 #索引创建成功
    72 print（"索引l创建成功"）
    73
    74
    75
    76 print（"="*100)
    77
    78 import pandas as pd
    79
    80 #1.数据读取
```python
81 df=pd.read_csv('../test_samples.csv',encoding="gbk")
```

    82
    83 #2.数据清洗
```python
84 questions=df['question'].fillna().tolist（)
85 answers=df['answer'].fillna(').tolist()
```

    86
    87 #3.向量化
```python
88 vectors =model.encode(questions,normalize_embeddings=True).tolist()
```

    68 print（f"已生成{len（vectors）}个向量"）

## 5.Milvus数据查询

    代码块
    1 #-*-coding:utf-8-*
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4 #-*-coding:utf-8-*-
    5 #北梦测教育
    6 #课程咨询加微信：xiaobeiceshi
    7 from sentence_transformers import SentenceTransformer
    8 from pymilvus import connections,Collection
    6
    10
    11 #配置区域
    12 MILVUS_HOST=“123.60.46.254"
    13 MILVUS_PORT="19530"
    14 MILVUS_USER="root"
    15 MILVUS_PASSWORD="Mv@Bmc2026#X9kR"
```python
16 MILVuS_MoDEL_PATH="../models/paraphrase-MiniLM-L6-v2"
```

    17
    18
    19 print（"目前正在连接milvus数据库"）
    20 #1.连接miLvus
```python
21 connections.connect(host=MILVUS_HoST,port=MILVUS_PORT,user=MILVUS_USER,
22 passWord=MILVUS_PASSWORD)
```

    23
    24 print（“milvus数据库连接成功，接下来加载本地模型"）
    25
    26 #2.加载模型
```python
27 model=SentenceTransformer（MILVUS_MoDEL_PATH,device=cpu'）#可以改为cuda 使用GPU
```

    28
    29 print（“本地模型加载完成"）
    30
    31
    32
```python
33 print("="*100)
```

    34

    35 #配置区
```python
36 COLLECTION_NAME="faq3_crud"
```

    37
```python
38 collection=Collection(name=COLLECTION_NAME)
```

    39
    40
    41
    42 query_text=input（“请输入查询内容：“）
    43
    44 #1.加载集合到内存
    45 collection.load()
    46
    47 #2.将查询文本转为向量
```python
48 query_vector = model.encode([query_text],normalize_embeddings=True)
```

    49
    50 #3.构建搜索参数
```python
51 search_params={
```

    52 "metric_type":"cosINE",
```python
53 "params":{"nprobe":128}
```

    54
    55
    56 #4.执行搜索
    57 results= collection.search（
    58 data=query_vector,
    59 anns_field="vector" #指定在哪个字段搜索
    60 param=search_params,
    61 limit=3, #召回多少数据top-k
```python
62 output_fields=["question","answer"] #指定返回哪些原始字段
```

    63
    64
    65 print（“打印召回结果"）
    66 #print(results)
    67
    68 #5.处理结果
```python
69 for i,hit in enumerate(results[e]):
70 print（f"相似度：[hit.distance}")
71 print（f"问题：{hit.entity.get（question）)}")
72 print（f"回答：{hit.entity.get（'answer'）)}")
```

    73 print('-*100)

## 6.Milvus删除数据

    代码块
    1 #-*-coding:utf-8-*
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4 from sentence_transformers import SentenceTransformer
    5 from pymilvus import connections,collection
    6
    7 #配置区域
    8 MILVUS_H0ST="123.60.46.254"
    6 MILVUS_PORT="19530"
    10 MILVUS_USER="root"
    11 MILVUS_PASSWORD="Mv@Bmc2026#X9kR"
```python
12 MILVUS_MoDEL_PATH="./models/paraphrase-MiniLM-L6-v2"
```

    13
    14 print（“目前正在连接milvus数据库"）
    15 #1.连接miLvus
```python
16 connections.connect(host=MILVUS_HOST, port=MILVUS_PORT,user=MILVUS_USER,
17 passWord=MILVUS_PASSWORD)
```

    18
    19 print（“milvus数据库连接成功，接下来加载本地模型"）
    20

    21 #2.加载模型
```python
22 model=SentenceTransformer（MILVUS_MoDEL_PATH，device='cpu'）#可以改为 cuda 使用GPU
```

    23
    24 print（"本地模型加载完成"）
    25
    26 print（"="*100）
    27
    28 #配置区
```python
29 COLLECTION_NAME="faq3_crud"
```

    30
```python
31 collection=Collection(name=COLLECTION_NAME)
```

    32
    33
    34 #定义需要删除的列表
```python
35 de1_ids=[464637054753578431,464637054753578432]
```

    36 #写布尔表达式
```python
37 expr=f"id in {del_ids}"
```

    38 collection.delete(expr)
    6 collection.flush()
    40 print（"删除数据成功"）

## 7.Milvus更新数据

    - 更新数据是否传id取决于auto_id是否为True
            - 如果主键是True，那么就不能传id
                - 但是是否传id对查询几乎没有影响，因为向量数据是相似度查询
            如果是False，可以传id
    代码块
```python
#-*-coding:utf-8-*
```

    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4 from sentence_transformers import SentenceTransformer
    5 from pymilvus import connections,collection
    6
    7 #配置区域
    8 MILVUS_H0ST="123.60.46.254"
    6 MILVUS_PORT="19530"
    10 MILVUS_USER="root"
    11 MILVUS_PASSWORD="Mv@Bmc2026#X9kR"
```python
12 MILVUS_MODEL_PATH="../models/paraphrase-MiniLM-L6-v2"
```

    13
    14 print（"目前正在连接milvus数据库"）
    15 #1.连接mLvus
```python
16 connections.connect(host=MILVUS_HOST, port=MILVUS_PORT,user=MILVUS_USER,
17 password=MILVUS_PASSWORD)
```

    18
    19 print（"milvus数据库连接成功，接下来加载本地模型"）
    20
    21 #2.加载模型
```python
22 model=SentenceTransformer（MILVUS_MODEL_PATH，device='cpu'）#可以改为cuda 使用GPU
```

    23
    24 print（"本地模型加载完成"）
    25
```python
26 print("="*100)
```

    27
    28 #配置区
```python
29 COLLECTION_NAME="faq3_crud"
```

    30
```python
31 collection = Collection(name=COLLECTION_NAME)
```

    32
    33
    34 #定义需要删除的列表
```python
35 del_ids=[464637054753578435]
```

    36 #写布尔表达式
```python
37 expr =f"id in {del_ids}"
```

    38 collection.delete(expr)
        collection.flush()
    40 print（"删除数据成功"）
    41
    42 #2.生成新的向量
    43 #原问题：海关收取高额关税能报销吗
    44 #新问题：海关可以免费吗
    45
```python
46 new_question=[“海关可以免费吗"]
```

    47
    48 #新的向量
```python
49 new_vector=model.encode（["海关可以免费吗"],normalize_embeddings=True）[e].tolist（）
```

    50
    51 #新的回答：不可以免费
```python
52 new_answer=["不可以免费"]
```

    53
    54 #构造新的插入数据
    55 entities=[
    56 new_question,
    57 new_answer,
```python
58 [new_vector]
```

    59]
    60
    61 collection.insert(entities)
    62 collection.flush()

## 8.Milvus操作封装

    代码块
    1 #-*-coding:utf-8-*-
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4
    5 from sentence_transformersimportSentenceTransformer
    6 from pymilvus import connections,utility,Fieldschema,CollectionSchema,DataType,Collectior
    7
    8
```python
6 class MilvusClient(object):
10 def__init_（self,host,port,user,password,
```

    11 model_path="../models/paraphrase-MiniLM-L6-v2"
```python
12 collection_name="faq3_crud",dimension=384):
```

    13 self.host =host
    14 self.port=port
    15 self.user = user
    16 self.password=password
```python
17 self.model_path=model_path
18 self.collection_name=collection_name
```

    19 self.dimension =dimension
    20
    21 #建立连接
```python
22 self._connect()
```

    23
    24 #加载模型
```python
25 self.model=SentenceTransformer（self.model_path，device=cpu'）#可以改为 cuda 使用GP
```

    26
    27 #集合
```python
28 self.collection=Collection(name=self.collection_name)
```

    29
```python
30 def_connect(self):
```

    31 """建立和Mi1vus的连接"""
    32 try:
```python
33 connections.connect(host=self.host,port=self.port,user=self.user,
```

    34 password=self.password)
    35
    36 print（"Milvus连接建立成功"）
    37 except Exception ase:
    38 print（f"建立Milvus连接失败：{e}"）
```python
raise
```

    40
```python
41 def create_collection(self,collection_name=None):
```

    42
    43 创建集合
    44 ：param collection_name：集合的名字，默认为空
    45 :return:
    46 1
    47 #传了coLLection_name就重新赋值
    48 ifcollection_name:
```python
49 self.collection_name=collection_name
```

    50
```python
51 ifutility.has_collection(self.collection_name):
52 utility.drop_collection(self.collection_name)
```

    53
    54 #2.字段定义
    55 fields=[
```python
56 FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
57 FieldSchema(name="question",dtype=DataType.VARCHAR,max_length=65535),
58 FieldSchema(name="answer",dtype=DataType.VARCHAR,max_length=65535),
59 FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=self.dimension),
```

    60
    61
    62 #3.创建schema
```python
63 schema =CollectionSchema（fields=fields，description=“电商FAQ知识库"）
```

    64
    65 #4.创建集合
```python
66 collection =Collection(name=self.collection_name,schema=schema)
```

    67
    68 print（“集合和schema创建完毕"）
    69
    70 #5.创建索引
```python
71 index_params={
```

    72 "index_type"：“IVF_FLAT"，#表示倒排文件索引l，通过聚类加速搜索
    73 “metric_type”：“coSINE”，#coSINE表示使用余弦相似度计算
```python
74 "params":{"nlist":128}#聚类数量越大越准越慢越小越快可能漏检
```

    75
```python
76 collection.create_index（field_name="vector",index_params=index_params)
```

    77 #索引创建成功
    78 print（“索引l创建成功"）
    79
```python
80 def insert_data(self,questions,answers):
```

    81 1111
    82 插入数据
    83 :param questions：问题列表
    84 :param answers：回答列表
    85 :return:
    86
```python
87 vectors=self.model.encode(questions,normalize_embeddings=True).tolist()
```

    88 print（f"已生成{len（vectors）}个向量"）

## 9.Milvus向量数据库的可视化工具

```python
下载地址:https://github.com/zilliztech/attu/releases?spm=5176.28103460.0.0.7ce1298806JNKF
```

FileEditViewWindowHelp
        欢迎来到Milvus！ 123.60.46.254:19530
                                                                                                运行中
        数据库
        田
        default
        所有Collection8 3 创建数据库
        创建时间
        2026/3/2 18:36:28
        系统信息
        v2.3.12 STANDALONE 45.18day 1 2
        MilvusVersion 部署模式 运行时间 用户 角色数据库 123.60.46.254:19530default 运行中default Collections田faq2_crud（o）
```python
田faq3_crud(50)
ecommerce_f..(50) 创建Collection 导入文件刷新 Q按名称搜索
```

                                名称 状态 大约的Entity数量 描述 别名 创建时间
                            口 faq2_crud 已加载 0 电商FAQ知识库 2026/4/1
                            口 faq3crud 已加载+ 50 电商FAQ知识库 + 2026/4/11
                            口 ecommercefaq_v2 已加载 50 电商常见问题知识库 + 2026/3/2
                    集合

## 6.RAGAS框架--量化RAG系统的“标尺”

## 1.RAGAS是什么

RAGAS（RAGAssesSment）是一个专门为RAG系统设计的自动化评估框架

## 2.RAGAS核心

## 定位

    问题：RAG系统开发中，面临问题：就是无法确定系统输出的结果的好坏，之前的好坏全凭”人"的感觉
    解决：RAGAS提供了一套无需人工标注大量数据的自动化评估指标，采用大模型"来评估"大模型”。让RAG效果

    可量化，可对比，可优化

## 价值

无需参考评估，大部分指标不需要标准答案，无需提前准备好数据多维度诊断：将RAG系统拆解为检索“和生成"两个环节，对这两个环节分别进行打分，精准定位问题自动化测试集成，可以利用现有的文档进行自动化生成评测问题

## 3.RAGAS作用

对比不同的Embedding模型，不同的向量数据库，不同的大模型组合效果
    每次开发修改代码，或者修改提示词之后，自动化的去进行量化评估，提升效率
    每次上线前可以作为准入的门槛
    问题诊断：通过各项指标的得分，判断问题是“检索不准"还是“生成胡说”

## 4.RAGAS核心原理

    RAGAS核心原理就是：利用一个更强的大模型来作为裁判评估RAG系统
        用户输入问题--->检索模块：召回上下文--->生成模块：生成答案---->RAGAS：作为裁判读取用户的问题
        和生成的答案---->RAGAS：对问题相应的答案给出指标得分
    RAGAS也是基于语义对输出的问题进行打分

## 5.四大核心指标

## 1.忠诚度（faithfuless）-防止大模型胡说八道

    - 定义：生成的答案中的所有的事实是否都能从检索的上下文中推导出来
        计算逻辑：
            1.将答案拆分为多个独立的陈述句
            2.让“更强的这个大模型”来判断陈述句是否都能从上下文中找到依据
            3.得分=有依据的句子数/总句子数
    示例：
        问题：公司Q3营收多少
        上下文：财报显示Q3季度营收为500万美元
            答案1：公司营收为500万美元
            - faithfuless=1.0
            答案1：公司营收为500万美元，增长20%
```python
faithfuless=0.5
```

                因为增长20%没有依据，属于模型的幻觉

## 2.答案相关性（AnswerRelevancy）-防止答非所问

    - 定义：生成的答案是否切题，有没有直接解决用户问题
    计算逻辑：
        1.让"更强的大模型“根据生成的答案，反向生成几个“可能的问题”
        2.再计算这些"反向生成的问题“和"原始的问题“的语义相似度
        相似度越高，答案相关性越高
        示例：
        问题：如何重置密码
        答案1：点击登录页面--点击"忘记密码"--按照操作走..

            - 高分
        答案2：密码是定期更换，是账户安全重要保障
            - 低分

## 3.上下文精确度（ContextPrecision）

    定义：所有检索到的上下文片段中，包含正确的答案的是否排在前面
    计算逻辑
        识别到哪些上下文片段中包含了包含了有关的答案的信息
        计算这些片段的平均排名位置
        - 排名越靠前，得分越高
    示例：
        检索结果：【片段A（无关）片段B（有关）片段C（无关）片段D（有关）】
        理想情况：【片段B（有关）片段D（有关）片段C（无关）片段A（无关）
        实际情况：有可能相关的片段排在后面，导致大模型可能忽略

## 4.上下文召回率（ContextRecall）

    定义：检索到的上下文中，是否包含了回答的答案所需的所有信息
    计算逻辑：
        1.将答案拆分成多个事实点
        2.检索每个事实点是否能够在上下文中检索到
        得分：找得到的事实点/总的事实点
        示例：
        答案：银行的理财产品支持回购，价格在100美元
        检索上下文：【理财产品价格为100美元】
```python
ContextRecall=0.5
```

## 6.如何使用RAGAS

## 1.环境安装

    代码块
        pip install ragas langchain-community datasets pandas
        注意：ragas需要python版本在3.10+

## 2.数据准备

RAGAS需要准备四类数据
    question：用户提出的问题案例：公司Q3季度营收是多少
    answer：RAG系统生成的回答回答：公司Q3季度营收是500w美元
    context：检索到的上下文片段列表【财报显示Q3季度营收数据.."，“新闻提到公司Q3季度营收是.】
    ground_truth：标准答案 案例：500w美元（部分的指标需求）question answer contexts我的订单已发货10天物您的订单已通过平邮小包发出，国际物流更新通常5个工作日。订单发货后10天内无更新属[国际平邮小包物流信息更新延迟通常为3-国际物流更新通常有3-5天的流未更新 有3-5天的延迟。建议您再等待2个工作日。 延迟
                                                        于正常范围。]收到衣服尺码不对怎么非常抱歉发错了尺码。您可以申请免费换货，我们[发错货情况支持免费换货，商家承担往返支持免费换货，商家承担往办 将承担往返运费。请在后台提交申请并上传照片。 运费。，用户需在后台提交申请并上传照片凭证。 返运费

包裹显示签收但我没收对于未授权放置导致的丢失，我们深表歉意。请联[未授权放置导致包裹丢失，需用户提供邮需提供未收到货证明，可办到 您全额退款。系当地邮局开具未收到货证明，凭此证明我们将为局未收到货证明。，凭证明可为用户办理全额退款或补发。了 理全额退款商品质量有问题退货运 因商品质量问题产生的退货，运费由我们承担。请【质量问题退货运费由商家承担。，用户需运费由商家承担，入库确认费谁出 您先行垫付，退货入库确认后，我们会将运费退还先行垫付，入库确认后退还至原支付账 后退还
                    给您。 户.]海关收取高额关税能报根据平台政策，进口关税由收件人自行承担。但如[进口关税通常由收件人自行承担。，若因进口关税由收件人承担，申销吗 果是因我们申报价值错误导致的额外税费，核实后商家申报错误导致额外税费，核实后可补 报错误可补偿
                    会补偿差额。 偿差额。
                    我们的标准退货政策是签收后30天内。超过30天 [标准退货期为签收后30天内。，超期严重标准退货期30天，超期严重超过30天还能退货吗 原则上不支持，但如果是严重质量问题，我们可以质量问题可申请特殊处理，如维修或部分 质量问题可特殊处理
                    为您申请特殊处理。 退款。]想换货但商品下架了怎若商品下架无法换货，建议您直接申请退货退款。 [商品下架无法换货时，建议申请退货退 建议退货退款，可提供5%优么办 退款成功后，我们可以为您提供一张5%的优惠券款。，退款后可提供5%优惠券作为补 惠券补偿
                    作为补档 档
    test_samples.csv

## 3.配置评估器&运行

LLM：用于打分的大模型---这里我采用智谱aiEmbedding：用于计算语义相似度的嵌入模型代码实现
    代码块
    1 #-*-coding:utf-8-*
    2 #北梦测教育
    3 #课程咨询加微信：xiaobeiceshi
    4 import pandas as pd
    5 from langchain_community.chat_modelsimport ChatZhipuAI
    6 from langchain_community.embeddings import ZhipuAIEmbeddings
    7 from datasets import Dataset
    8 from ragas import evaluate
```python
6 from ragas.metrics import _faithfulness,_answer_relevancy,_context_precision,_context_recall
```

    10 importos
    11 importast
    12
    13 #配置区域
```python
14 os.environ["ZHIPUAI_API_KEY"]=“8d3882f760364fd997ae0550a1f8af4b.oPKOkFe1yrOudvmq"
15 INPUT_cSV="test_samples.csv"
```

    16 OUTPUT_CSV ="results.csv"
    17
    18 #模型初始化
    19 print（"正在初始化模型"）
```python
20 judge_1lm=ChatZhipuAI（model='glm-4',temperature=0)
21 embeddings=ZhipuAIEmbeddings（model="embedding-2")
```

    22
    23
    24 #数据加载和预处理
```python
25 def load_and_prepare_data(file_path):
26 df=pd.read_csv(file_path,encoding="gbk")
```

    27 print（“读取csv数据完成"）
    28
    29
    30 #处理contexts 列，要求必须是列表比如[“片段1”，“片段2"]
```python
31 def parse_contexts(val):
32 if isinstance(val,str)and val.startswith('['):
33 return ast.literal_eval(val)
```

    34
    35 else:
    36 return[val]
    37
    38 #appLy就是把每一个数据都传入到括号内的函数进行处理然后返回数据
```python
39 df['contexts']=df['contexts'].apply(parse_contexts)
```

    40
    41

    42 #RAGAs要求ground_truth必须是字符串
    43 #直接取值判断不是字符串强制转字符串
```python
44 def parse_ground_truth(val):
```

    45 if isinstance（val,str):
    46 return val
    47 else:
    48 return str(val)
    49
```python
50 df['ground_truth']=df['ground_truth'].apply(parse_ground_truth)
```

    51
    52 return df.fillna（）
    53
    54
    55
    56 ifute==weu
    57 #进行评估的主流程
    58
    59 #加载和处理数据
```python
60 df_input=load_and_prepare_data(INPuT_csV)
```

    61 print（"数据加载和处理完毕"）
    62
    63 #进行评估
    64 print（"开始进行评估.5."）
    65 results =evaluate（
```python
66 dataset=Dataset.from_pandas(df_input),
67 metrics=[_faithfulness,_answer_relevancy,_context_precision,_context_recall],
```

    68 1lm=judge_1lm,
    69 embeddings=embeddings
    70
    71
    72
    73 #保存结果
```python
74 df_results =results.to_pandas()
75 df_results.to_csv(ouTPuT_cSV,index=False,encoding="utf-8")
```

    76 print（"大模型评测完毕"）

## 运行结果

```python
user_input retrieved_contexts response reference faithfulness answer_relevancy context_pr
```

                    [国际平邮小包物流 您的订单已通过平邮我的订单已发货10天信息更新延迟通常为小包发出，国际物流国际物流更新通常有物流未更新 3-5个工作日。订单更新通常有3-5天的 3-5天的延迟 0.33333333333333330.333884215067582 0.999999999
                    发货后10天内无更新延迟。建议您再等待
                    属于正常范围。 2个工作日。
                    [发错货情况支持免 非常抱歉发错了尺收到衣服尺码不对怎费换货，商家承担往码。您可以申请免费支持免费换货，商家么办 返运费。，用户需在换货，我们将承担往承担往返运费 0.8 0.610548739282103 0.999999999
                    后台提交申请并上传返运费。请在后台提
                    照片凭证。] 交申请并上传照片。
                    [未授权放置导致包 对于未授权放置导致
                    裹丢失，需用户提供的丢失，我们深表歉包裹显示签收但我没邮局未收到货证明。，意。请联系当地邮局需提供未收到货证 0.66666666666666660.30538679092623270.999999999收到 凭证明可为用户办理开具未收到货证明， 明，可办理全额退款
                    全额退款或补发。 凭此证明我们将为您
                                    全额退款。
                    [质量问题退货运费 因商品质量问题产生商品质量有问题退货由商家承担。用户的退货，运费由我们承担。请您先行垫 运费由商家承担，入运费谁出 需先行垫付，入库确付，退货入库确认 库确认后退还 1.0 0.674749672355477 6666666660
                    认后退还至原支付账后，我们会将运费退
                    户。 还给您。
    results.csv

## 4.结果解读与优化建议

指标分低 可能原因 优化方向

faithfulness低 模型产生幻觉，编造信息 1.优化提示词，强调基于上下文回答
                                                        2.降低大模型的温度
                                                        3.提供更清晰的上下文
answer_relevancy低 答案啰嗦，答非所问 1.优化提示词，要求"直接回答”
                                                        2.过滤无关的上下文片段
context_precision低 关键信息排在后面 1.优化检索排序算法
                                                        2.使用更好的Embedding模型
                                                        3.进行查询改写
context_recall低 漏掉关键文档 1.扩大检索的范围（top-k)
                                                        2.优化文档切片策略
                                                        3.使用混合检索（关键词+向量）

## 7.项目业务--项目概述&行业背景

## 1.智能客服项目

项目是一个RAG技术架构的智能客服项目
    智能客服为什么要采用RAG技术
    相对比纯生成模型的方案，RAG可以实时更新知识库，降低大模型的幻觉
        可以追溯答案的来源，并且可以采用较小的模型+向量数据库成本会更低
        客服回答需要涉及到售后、安全等问题，对于准确性要求更高

## 2.RAG的智能客服项目在哪些领域会用到

电商领域
    售前咨询，售中咨询，售后咨询
    - 订单查询处理...
    金融服务
    金融产品推荐
    风险评估，投资建议
    政务领域
    - 智能政务咨询
    工单管理：智能处理民生诉求
    医疗领域
    智能医疗咨询：症状描述，智能推荐科室和医生
    医疗客服：根据用户上传的内容，提供健康咨询
        医疗知识库：医生使用的，提升医生诊断效率
    教育培训
    招生咨询：招生问题解答
    - 学生学习咨询：AI学习助手
    - 教育知识库：课程信息，学习资料智能管理
    汽车领域
    汽车售前咨询：车型推荐，购车优惠解答
    售后服务：维修保养，售后政策
    汽车知识库：车型参数，维修保养的知识

    旅游酒店
    旅游咨询：旅游路线
    预定服务：酒店，机票预定咨询，订单处理
    法律服务
    - 法律咨询：法律问题在线解答
    法务工单：案件咨询跟踪
    - 法律知识库：法律天文库，案例搜索
    游戏娱乐
    - 游戏客服：游戏问题解答，账号问题自选
    游戏知识库：游戏攻略，游戏技术问题
        我们讲的这个项目，是电商领域的，但是实际上每个领域，每个行业都是可以去包装的
        - 技术架构，测试方法都是一样的
        - 不一样的只有知识库里面具体的内容不一样
        - 也就是问题和答案不一样，其他都是一样的

## 3.项目的整体架构

    RAG智能客服整体系统架构
        - 知识库
        - FAQ管理
        - 文档上传
        - 文档切片（面试的时候必须有的功能）
        向量化存储
        智能助手
        - 智能体配置
        ?提示词模版
        - 大模型选择
        - 消息记录
        客服
        会话管理
        - 消息管理
    知识库--->智能体--->客服
        - 技术支撑
        Mysql数据库：关系存储
        - Milvus:向量存储
        - ES：关键字检索
        大模型：干问，智谱ai...
核心数据库表MySQL

知识库：bytedesk_kbase_faq
    - 功能：FAQ问答对存储
    智能助手
    机器人配置：bytedesk_ai_robot
    提示词模版：bytedesk_ai_prompt
```python
对话消息记录：bytedesk_ai_robot_message
```

## 8.项目核心业务模块

## 1.知识库模块

知识库是RAG系统的"大脑”，负责存储和管理所有可检索的知识知识库的流程
    用户添加/上传文档---->MySQL数据库存储--->ES数据库（关键字检索）---->Milvus（向量检索）
                                    十创建 Q搜索测试 对话测试 导入导出 更多操作：
电商客服知识库-常见问题
                                                                                    C1
            问题 全文索引状态 向量索引状态① 点击次数（操作
            收到的衣款</p> 处理成功 ? 向量化成功 0 编辑删除 更新索引
                                                                        第1-1条/总共1条
                问题 全文索引状态 向量索引状态 操作
                能不能发殊管理... 处理成功 O 向量化成功 ?编辑删除
                能不能发...，... 处理成功 向量化成功 编辑删除
                能不能发单位名... 待处理 待向量化 编辑删除
                能不能发.和收件 处理成功 D向量化成功 编辑删除
                能不能发.验室名... 待处理 待向量化 编辑删除
                能不能发—科室. 待处理 待向量化 编辑删除
                能不能发签收，. 处理成功 向量化成功 编辑删除
                能不能发楼层.. 待处理 待向量化 编辑删除
                能不能发和收件.. 待处理 待向量化 ? 编辑删除
        10 能不能发和联系... 处理成功 向量化成功 编辑删除

                                                第1-10条/总共101条 3451功能讲解
- 知识库创建
    - 上传知识库logo，选择语言，输入知识库名称，输入描述，点击确定创建知识库
    - 知识库可以删除和边界
    创建分类
    - 选择知识库可以创建分类，选择上级分类，分类名称，所属知识库
    - 分类可以删除和编辑
    问题管理
    点击创建按钮进行创建
        选择分类，输入问题，智能生成相似问法，手动填写相似问法，输入文本答案，上传图片，上传附件，
        有效期设置，是否启用
    导入创建
        下载excel模版，填写问题和答案以及分类和类型
        面试的时候不说目前的导入方式，而是说通过上传的pdf或者word文档进行的语义切片然后进行数据存储
    导出功能
    - 导出当前的FAQ为excel格式
    搜索测试
    - 测试目前上传的FAQ数据能否正确召回
    对话测试
    选择机器人打开对话框进行测试
    更多操作
    - 更新和删除全文索引（ES），更新和删除向量索引I（Milvus）
    查询
    根据问题或者回答搜索

## 2.智能助手模块

智能体创建流程
        $机器人创建--->智能体创建的时候选择机器人”--->选择大模型--->选择提示词--->选择知识库
    大模型：面试的时候不用去讲“我们有很多大模型的配置，可以任意选择”
        面试的时候讲：我们用的”通义干问”的大模型
            后面会讲到实际通义千问的大模型会用到两个，一个是低B版本的，一个是高B版本的功能讲解大模型（通义干问）
    配置Apikey（实际工作是开发来做）
    - 添加统一千问的各类模型
        - 低B，高B
    基本功能
        编辑，删除，刷新，搜索...

    通义千问×
        通义千问已启用 C
        只有在模型启用且配置有baseUrl和apikey的情况下才会启用。
        配置信息 编辑
            APIKey未配置 立即配置
            请配置APIKey以正常使用AI服务
            模型列表
    +添加模型 导入模型 C刷新模型 按模型名称搜索 Q
        QwenMax文本对话模型 已启用
        qwen-max 编辑 删除
        通义千问的最高规格版本，提供最佳的能力和性能
        2.QwenPlus文本对话模型 已启用
        qwen-plus 编辑 删除
        通义千问的增强版本，具有更强的理解能力和生成质量
                                            1-3/3 10条/页
    提示词管理
    提示词创建
        - 输入名称，昵称，类型，是否启用，描述，语言，提示词内容
        可以进行编辑，删除，查询，修改
        优化：调用大模型对目前写好的提示词进行优化，可以选择使用和不使用
    评分：把提示词给到大模型进行评分名称： 昵称：请输 重置 查询 展开V提示词 创建 重置全部默认 C
    名称 昵称 类型 描述 操作0 airline_booking_assistant 航空客服助手 通用 创建一个航空客服助手机器人，支持预订查询、查看重置默认评分优化编辑删除
    promptoptimize 提示词优化 通用 创建一个提示词优化和改进机器人 查看重置默认评分优化编辑删除③ prompt_score 提示词评分 通用 创建一个提示词评分和评估机器人 查看重置默认评分优化编辑删除
    - cr_extraction OCR文字提取 通用 使用先进的OCR技术从图像中提取文字 查看重置默认评分优化编辑删除
    faq_similar_questions FAQ相似问题生成器 通用 创建一个为FAQ生成相似问题变体的机器人，以2查看重置默认评分优化编辑删除? agentassistant 客服助手 通用 创建一个客服助手机器人 查看重置默认评分优化编辑删除
    faq_generate 生成FAQ 通用 创建一个生成FAQ机器人 查看重置默认评分优化编辑删除
    ticket_generate 工单生成 工单辅助 创建一个智能填写工单机器人 查看重置默认评分优化编辑删除
    thread_summary 会话小结 会话总结 创建一个会话摘要机器人 查看重置默认评分优化编辑删除
    机器人
        创建：选择机器人配置（默认机器人--去创建了一些默认的配置）
        编辑
            是否启用
            使用哪个大模型
            温度，top-p，top-k，得分值，知识库等设置

            这些都可以在智能体里面进行修改
    删除，查询等功能
    机器人账号 机器人配置
    搜索：请输 重置 查询
    机器人 新建 C工@
            昵称 头像 类型 ID 机器人配置 提示词 操作
            默认机器人 机器人 dfrtuid 默认机器人配置 查看 对话测试获取机器人代码编辑
        2 测试机器人 机器人 1873831031472512 默认机器人配置 查看 对话测试获取机器人代码编辑删除
                                                                                                    第1-2条/总共2条
    智能体
        创建：上传头像，选择机器人配置，输入昵称
        编辑
        是否启用
            使用哪个大模型
            温度，top-p，top-k，得分间值，知识库等设置
        删除，查询等功能
        对话测试
            页面上打开一个对话框，进行对话的测试
        打开机器人地址
        打开一个web网页进行对话的测试
            面试的时候可以不说这个功能，因为实际都是在小程序或者app当中进行操作的索： 重置 查询器人 新建 C工命
    昵称 头像 类型 ID 名称 机器人配置 操作D 电商售后客服 8 智能体 1858322441437568 汽车售后客服 glm-4-long 对话测试获取机器人代码编辑删除? 提示词优化 智能体 1857943930667145 prompt.optimize glm-4-flash 对话测试获取机器人代码编辑删除B 提示词评分 智能体 1857943930667144 promptscore glm-4-flash 对话测试获取机器人代码编辑删除
    航空客服助手 智能体 1857943930667143 airline_booking_assistantglm-4-flash 对话测试获取机器人代码编辑删除
    - CR文字提取 智能体 1857943930667141 ocr_extraction glm-4-flash 对话测试获取机器人代码编辑删除
? FAQ相似问题生成器 智能体 1857943930667140 faq_similar_questions glm-4-flash 对话测试获取机器人代码编辑删除D 生成FAQ 智能体 1857943930667138 faq_generate glm-4-flash 对话测试获取机器人代码编辑删除

## 3.客服模块

## 功能讲解

一对一：把系统的成员创建为客服，可以对客服进行增删查改的操作
    客服人员登录系统之后可以点击进入到客服工作台”，在这里进行消息回复
        客服工作台的功能可以大致了解

        客服状态：在线，挂起，停止接待
        目前有哪些会话：会话可折叠，排队中，可以添加常用语
        可以查看数据：处理中，待回复，已读未回复...
    工作组：把不同的客服编入到一组里面，可以设置一个组长（管理员）
    - 工作组可以设置不同的路由规则：就是用户的会话分配规则（随机，轮询，加权随机，最小回复时间...）
        工作组也可以设置机器人回复：可以默认启用，也可以设置没有客服的时候启用
        可以转人工
    工作组配置
        欢迎语，关闭语言，没有新消息多久关闭会话，多久可以撤回消息…会话：就是和客服的聊天的窗口保持
    - 新增一个聊天（智能体），就会新增一个会话
    - 会统计会话中的总的消息数，智能客服的消息，用户的消息
    目前是哪个智能体/机器人接待，状态是什么
    消息：每一条用户和智能体的对话消息都会在这里作展示
    - 有查询，查看，导出的功能
面试的时候：
    原本的系统是只有人工客服，大致有哪些功能（并不是我们目前测试的）。我们主要做的是智能客服的接入。
    用户创建会话的时候默认就是只能客服进行回答，然后可以选择转人工
    如果人工目前都是停止接待”的状态，触发留言工单，这个工单人工客服可以看到
    发送的每一条消息都会记录到消息“列表页面

## 9.智能客服核心流程讲解（重要）

面试的时候面试官问到可以给面试官直接讲述的智能客服的流程

## 1.智能客服的核心流程

    - 用户提出问题+历史5轮的对话
            - 对用户目前的问题和历史的五轮对话进行上下文感知
            查询改写+指代消解--->通过一个大模型（通义千问-14B）-->初步意图识别：订单咨询，退
                货，物料，产品服务---->生成两个疑问句
        双疑问句（实际开发测试中发现双疑问句会比单疑问句召回效果更好）
            使用双疑问句进行Milvus向量检索
            - 通过”余弦相似度”进行度量
            检索：Top-10
        检索的Top10--->Top2
            - 通过”通义千问-235B"高精度大模型进行重排序
            精选：top-2
            再对top-2的内容给到大模型，生成最终的回答
                最终的回答带上emoji（风格化的处理）
        不同项目可选
            项目行业背景区分
            - 政务项目，金融项目，汽车项目，医疗项目，法律咨询
                - 人机协同审核

                - 可选流程：AI生成的内容不会直接发送给客户，而是通过人工进行审核之后才会发送给客户
                电商，游戏娱乐，教培，旅游等等
                可以直接发送给客户
                    可以转人工客服

## 2.流程问题解答

- 为什么第一次要用低B的模型？
    - 速度快，成本低
    ?对于基本的意图识别来讲准确度也是足够
    为什么要选择5轮对话作为上下文窗口？
    - 通过实际得出的需求
    - 太少可能会丢失关键信息，太多会引入噪声，增加模型的负担
    为什么要做双疑问句？
    - 因为在实际的开发测试中发现双疑问句召回检索的能力更强，单疑问句可能会漏掉一些信息
    为什么要带上emoji表情？
    - 因为技术单纯的回复会显得冷冰冰，不近人情
    - 加上风格化的回复会更加亲切，减少投诉
    为什么要进行人工审核？
