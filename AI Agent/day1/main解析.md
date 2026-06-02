# ui/main.py 详细解析

> 学习目标：看懂 `ui/main.py` 在整个 Auto_prd_test_expert 项目里负责什么，以及用户从上传 PRD 到生成、评估、归档测试用例的完整流程。

---

## 1. 先给这个文件定位

`ui/main.py` 是这个项目的页面入口，也是主业务编排文件。

你可以把它理解成：

```text
ui/main.py = Streamlit 页面 + 用户交互 + 调用核心模块 + 管理页面状态
```

它本身不直接完成所有底层能力，而是负责把其他模块串起来：

```text
用户上传文件
-> ui/main.py 接收文件
-> 调 core/rag_engine.py 检索知识库
-> 调 core/llm_client.py 调 Gemini
-> 调 core/evaluator.py 做质量评估
-> 调 ui/components.py 展示和导出结果
```

所以学习这个文件时，不要把它当成普通脚本看，而要把它当成“项目总控制台”。

---

## 2. 文件整体结构

`ui/main.py` 可以分成 5 个部分：

```text
1. 导入依赖和项目模块
2. 定义 split_text_and_json() 工具函数
3. 定义 main() 主函数
4. 在 main() 里构建两个页面 Tab
5. 文件末尾调用 main() 启动页面
```

代码结构大致如下：

```python
import ...

from config.settings import setup_proxy
from config.prompts import PromptManager
from ui.sidebar import render_sidebar
from ui.components import display_results
from core.llm_client import ...
from core.rag_engine import RAGEngine
from core.evaluator import Evaluator


def split_text_and_json(text):
    ...


def main():
    ...


if __name__ == "__main__":
    main()
```

---

## 3. 导入依赖部分

### 3.1 第三方库

```python
import streamlit as st
import pandas as pd
import json
import sys
import os
from PIL import Image
```

逐个解释：

| 依赖 | 作用 |
|---|---|
| `streamlit as st` | 构建网页界面，比如按钮、上传框、聊天框、表格 |
| `pandas as pd` | 把 JSON 测试用例转成 DataFrame 表格 |
| `json` | JSON 字符串和 Python 对象之间转换 |
| `sys` / `os` | 处理项目路径，保证跨目录导入模块 |
| `PIL.Image` | 读取用户上传的图片文件，交给 Gemini 多模态模型 |

这里最重要的是 `streamlit` 和 `pandas`：

```text
Streamlit 负责页面交互
Pandas 负责结果表格化
```

---

## 4. 路径适配代码

```python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

这行代码的作用是：把项目根目录加入 Python 的模块搜索路径。

因为当前文件在：

```text
ui/main.py
```

但是它要导入：

```text
config/settings.py
core/llm_client.py
core/rag_engine.py
```

如果不把项目根目录加入 `sys.path`，直接运行 `streamlit run ui/main.py` 时，Python 可能找不到 `config` 和 `core`。

可以这样理解：

```text
__file__                 -> 当前文件 ui/main.py
os.path.dirname(__file__) -> ui 目录
..                       -> 回到项目根目录
sys.path.append(...)     -> 让 Python 能从项目根目录找模块
```

---

## 5. 项目内部模块导入

```python
from config.settings import setup_proxy
from config.prompts import PromptManager
from ui.sidebar import render_sidebar
from ui.components import display_results
from core.llm_client import get_gemini_chat_response, generate_summary, extract_json_from_text
from core.rag_engine import RAGEngine
from core.evaluator import Evaluator
```

这些导入体现了项目的分层结构：

| 模块 | 在 `main.py` 里的作用 |
|---|---|
| `setup_proxy` | 启动时设置网络代理，保证能访问 Gemini |
| `PromptManager` | 生成各种 Prompt：首次生成、修改、RAG 过滤、评估 |
| `render_sidebar` | 渲染侧边栏，获取 API Key 和模型名 |
| `display_results` | 展示表格，并提供 CSV/JSON/YAML/Markdown 下载 |
| `get_gemini_chat_response` | 调 Gemini 聊天接口 |
| `generate_summary` | 给文档或用例生成摘要 |
| `extract_json_from_text` | 从 AI 回复里提取 JSON |
| `RAGEngine` | 操作 ChromaDB，完成知识库检索、入库、删除 |
| `Evaluator` | 调用 AI 对测试用例进行质量评估 |

一句话总结：

```text
main.py 不直接实现所有能力，而是负责把 config、core、ui 三层连接起来。
```

---

## 6. split_text_and_json(text) 函数

### 6.1 函数作用

```python
def split_text_and_json(text):
    """分离 AI 回复中的【分析说明】和【JSON数据】"""
```

这个函数负责把 AI 回复拆成两部分：

```text
自然语言解释 + JSON 测试用例数据
```

因为项目要求 AI 回复时：

```text
前面先解释分析思路
后面再输出完整 JSON 数组
```

例如 AI 可能返回：

```text
我将从正常登录、异常登录、边界输入三个角度设计用例。
[
  {"id": "TC_001", "module": "登录", ...}
]
```

这个函数会拆成：

```text
explanation = "我将从正常登录、异常登录、边界输入三个角度设计用例。"
json_data = [{"id": "TC_001", ...}]
```

---

### 6.2 第一步：先尝试提取 JSON

```python
json_data = extract_json_from_text(text)
if not json_data:
    return text, None
```

含义：

1. 调用 `extract_json_from_text()` 尝试从 AI 回复里提取 JSON。
2. 如果提取不到，说明这次回复可能只是普通聊天或报错。
3. 直接返回原文本和 `None`。

这里的返回值固定是二元组：

```python
return explanation_text, json_data
```

---

### 6.3 第二步：找到 JSON 开始的位置

```python
text_stripped = text.strip()
split_idx_list = text_stripped.find('[')
split_idx_dict = text_stripped.find('{')
```

因为测试用例可能是 JSON 数组：

```json
[
  {...}
]
```

也可能是 JSON 对象：

```json
{
  "score": 85
}
```

所以它同时找 `[` 和 `{` 第一次出现的位置。

接着：

```python
if split_idx_list != -1 and split_idx_dict != -1:
    split_idx = min(split_idx_list, split_idx_dict)
elif split_idx_list != -1:
    split_idx = split_idx_list
elif split_idx_dict != -1:
    split_idx = split_idx_dict
```

这段逻辑的意思是：

```text
哪个 JSON 开始符号更靠前，就认为 JSON 从哪里开始。
```

---

### 6.4 第三步：拆出解释文本

```python
if split_idx > 0:
    explanation = text_stripped[:split_idx].strip()
    explanation = explanation.replace("```json", "").replace("```", "").strip()
```

如果 JSON 前面有内容，就把 JSON 之前的文本当成解释说明。

同时清理掉 Markdown 代码块标记：

```text
```json
```

如果解释太短：

```python
if len(explanation) < 2:
    explanation = "✅ 已根据指令生成最新测试用例数据（详情请见右侧预览）"
```

它会给一个默认提示。

---

### 6.5 第四步：如果回复一上来就是 JSON

```python
if text_stripped.startswith("[") or text_stripped.startswith("{") or text_stripped.startswith("```"):
    return "✅ 已根据指令生成最新测试用例数据（详情请见右侧预览）", json_data
```

有时候 AI 直接输出 JSON，没有解释文字。这时页面左侧不能空着，所以返回一个默认说明。

---

### 6.6 这个函数的核心价值

这个函数解决的是“展示体验”问题。

```text
左侧聊天区：展示自然语言解释
右侧预览区：展示结构化 JSON 表格
```

如果没有这个函数，页面上可能会把一大坨 JSON 全塞进聊天区，体验很差。

---

## 7. main() 函数总览

`main()` 是整个页面的起点。

它大致做这些事：

```text
1. 设置代理
2. 设置页面配置
3. 初始化 session_state
4. 渲染侧边栏，获取 API Key 和模型
5. 初始化 RAGEngine 和 Evaluator
6. 创建两个 Tab：智能共创工作台、知识库管理
7. 在智能共创工作台里处理上传、生成、微调、预览、评估、归档
8. 在知识库管理里处理知识上传、预览、删除
```

---

## 8. 启动代理和页面配置

```python
def main():
    setup_proxy()
    st.set_page_config(page_title="Auto_prd_test_expert", layout="wide")
```

### 8.1 setup_proxy()

`setup_proxy()` 来自 `config/settings.py`。

作用是设置 HTTP/HTTPS 代理，让项目能访问 Gemini API。

为什么需要代理？

```text
Gemini API 在部分网络环境下不能直接访问，所以项目启动时先检查并设置代理。
```

### 8.2 st.set_page_config()

```python
st.set_page_config(page_title="Auto_prd_test_expert", layout="wide")
```

作用：设置网页标题和页面布局。

| 参数 | 含义 |
|---|---|
| `page_title` | 浏览器标签页标题 |
| `layout="wide"` | 使用宽屏布局，适合左右分栏 |

这个项目后面会做左侧聊天、右侧预览，所以需要宽屏布局。

---

## 9. Session State 初始化

Streamlit 有一个特点：每次用户点按钮、上传文件、输入内容，页面脚本会重新从头运行。

如果没有状态保存，聊天记录、生成结果都会丢失。

所以项目用 `st.session_state` 保存关键数据。

代码：

```python
if 'messages' not in st.session_state: st.session_state['messages'] = [] 
if 'gemini_history' not in st.session_state: st.session_state['gemini_history'] = [] 
if 'res_data' not in st.session_state: st.session_state['res_data'] = None 
if 'prd_context' not in st.session_state: st.session_state['prd_context'] = "" 
if 'rag_context' not in st.session_state: st.session_state['rag_context'] = "" 
if 'rag_sources_display' not in st.session_state: st.session_state['rag_sources_display'] = None
if 'processed_files' not in st.session_state: st.session_state['processed_files'] = []
if 'eval_report' not in st.session_state: st.session_state['eval_report'] = None
```

这些状态的含义：

| key | 保存什么 | 为什么需要 |
|---|---|---|
| `messages` | 页面聊天记录 | 重新渲染页面时还能看到历史对话 |
| `gemini_history` | Gemini 多轮对话历史 | 让模型知道之前生成过什么 |
| `res_data` | 当前测试用例 JSON | 右侧表格预览和导出要用 |
| `prd_context` | 当前 PRD 的文本摘要 | 生成和评估都要用 |
| `rag_context` | RAG 检索并过滤后的上下文 | 让生成结果参考规范和历史案例 |
| `rag_sources_display` | RAG 来源展示字段 | 当前代码里初始化了，但实际主要用 `rag_sources_list` |
| `processed_files` | 已处理过的文件名列表 | 避免同一批文件重复预处理 |
| `eval_report` | 质量评估报告 | 右侧评估 Tab 展示 |

最重要的是这三个：

```text
messages       页面聊天记录
gemini_history 模型对话历史
res_data       测试用例结果
```

---

## 10. 渲染侧边栏并初始化引擎

```python
api_key, selected_model = render_sidebar()
rag_engine = None
evaluator = None
```

`render_sidebar()` 来自 `ui/sidebar.py`。

它负责：

```text
1. 显示 Gemini API Key 输入框
2. 保存 API Key
3. 获取可用模型列表
4. 返回 api_key 和 selected_model
```

接着，如果用户填了 API Key：

```python
if api_key:
    try:
        rag_engine = RAGEngine(api_key)
        evaluator = Evaluator(api_key)
    except Exception as e:
        st.sidebar.error(f"引擎初始化失败: {e}")
```

这里初始化两个核心对象：

| 对象 | 作用 |
|---|---|
| `RAGEngine(api_key)` | 知识库检索、文档入库、历史案例入库 |
| `Evaluator(api_key)` | 对生成的测试用例做质量评估 |

为什么要等有 API Key 才初始化？

因为这两个对象都需要调用 Gemini：

```text
RAGEngine 需要 Gemini Embedding 和多模态解析
Evaluator 需要 Gemini 生成评估报告
```

---

## 11. 页面顶层结构：两个 Tab

```python
st.title("🤖 Auto_prd_test_expert")

tab_work, tab_manage = st.tabs(["💬 智能共创工作台", "📚 知识库管理"])
```

页面分为两个大功能区：

| Tab | 功能 |
|---|---|
| 智能共创工作台 | 上传 PRD，生成测试用例，微调，评估，归档 |
| 知识库管理 | 上传知识文档，查看技术规范和历史案例，删除或预览 |

这就是项目的两个主场景：

```text
用知识库生成用例
管理知识库内容
```

---

# Tab 1：智能共创工作台

## 12. 左右分栏布局

```python
with tab_work:
    col_chat, col_preview = st.columns([0.4, 0.6], gap="medium")
```

工作台内部又分成左右两栏：

| 区域 | 宽度 | 作用 |
|---|---:|---|
| 左侧 `col_chat` | 40% | 上传文件、聊天、补充指令 |
| 右侧 `col_preview` | 60% | 表格预览、JSON 编辑、质量评估、归档 |

这样设计是为了实现“双屏共创”：

```text
左侧：和 AI 对话
右侧：实时看结构化测试用例
```

---

## 13. 左侧：需求对话区

```python
with col_chat:
    st.subheader("需求对话")
```

左侧主要做四件事：

```text
1. 上传 PRD / 图片 / PDF / 文本
2. 检索知识库和历史案例
3. 点击按钮生成初版测试用例
4. 后续用聊天输入框继续微调
```

---

## 14. 文件上传区

```python
with st.expander("📂 上传/补充需求文档", expanded=not st.session_state['messages']):
    uploaded_files = st.file_uploader("拖拽文件至此", accept_multiple_files=True, key="chat_uploader")
```

这里用了 `st.expander`，意思是一个可展开/收起的区域。

`expanded=not st.session_state['messages']` 的意思：

```text
如果还没有聊天记录，默认展开上传区。
如果已经开始对话，默认收起上传区。
```

`st.file_uploader` 的参数：

| 参数 | 含义 |
|---|---|
| `accept_multiple_files=True` | 支持一次上传多个文件 |
| `key="chat_uploader"` | 给这个上传组件一个唯一标识 |

---

## 15. RAG 参考开关

```python
c1, c2 = st.columns(2)
use_kb = c1.checkbox("📚 参考技术规范", value=True)
use_hist = c2.checkbox("🕰️ 参考历史案例", value=True)
```

这里给用户两个开关：

| 开关 | 作用 |
|---|---|
| 参考技术规范 | 是否从公司规范库检索相关规则 |
| 参考历史案例 | 是否从历史用例库检索相似案例 |

这两个开关会传给：

```python
rag_engine.search_context(preview_txt, use_history=use_hist, use_knowledge=use_kb)
```

---

## 16. 文件预处理入口

```python
if uploaded_files and rag_engine and api_key:
```

只有同时满足三个条件才处理文件：

```text
1. 用户上传了文件
2. RAG 引擎初始化成功
3. 用户填写了 API Key
```

接着：

```python
current_file_names = [f.name for f in uploaded_files]
if current_file_names != st.session_state['processed_files']:
```

这段是为了避免重复处理同一批文件。

因为 Streamlit 每次交互都会重跑脚本，如果不判断文件名，可能会反复解析、反复检索。

---

## 17. 解析上传文件

核心代码：

```python
preview_txt = ""
prompt_content = []
for file in uploaded_files:
    file.seek(0)
    if "image" in file.type:
        img = Image.open(file)
        prompt_content.extend([f"图片 {file.name}:", img])
        preview_txt += f"[图片 {file.name}] "
    elif "pdf" in file.type:
        prompt_content.extend([f"文档 {file.name}:", {"mime_type": "application/pdf", "data": file.read()}])
        preview_txt += f"[PDF {file.name}] "
    else:
        txt = file.read().decode("utf-8")
        prompt_content.append(f"文档 {file.name}:\n{txt}")
        preview_txt += txt[:500]
```

这里同时准备两份内容：

| 变量 | 作用 |
|---|---|
| `prompt_content` | 真正发给 Gemini 的多模态内容 |
| `preview_txt` | 用于 RAG 检索的文本摘要 |

不同文件类型的处理方式：

| 文件类型 | 处理方式 |
|---|---|
| 图片 | 用 `PIL.Image.open()` 打开，直接交给 Gemini Vision |
| PDF | 以 `mime_type: application/pdf` 的形式交给 Gemini |
| 普通文本 | 解码成 UTF-8 文本 |

注意：图片和 PDF 没有在这里先转文本，而是直接作为多模态输入传给 Gemini。

---

## 18. 第一阶段 RAG：向量粗筛

```python
raw_rag_info, sources = rag_engine.search_context(
    preview_txt,
    use_history=use_hist,
    use_knowledge=use_kb
)
```

这一步叫“粗筛”。

含义：

```text
拿当前 PRD 的摘要 preview_txt 去 ChromaDB 里检索相似的规范和历史案例。
```

返回两个东西：

| 返回值 | 含义 |
|---|---|
| `raw_rag_info` | 检索出来的原始上下文片段 |
| `sources` | 这些片段来自哪些文件或历史案例 |

为什么叫粗筛？

因为向量检索只负责“相似”，不一定保证“真正有用”。它可能召回一些语义接近但业务无关的片段。

---

## 19. 第二阶段 RAG：LLM 细筛去噪

```python
final_rag_context = ""
if raw_rag_info:
    filter_prompt = PromptManager.get_rag_filter_prompt(preview_txt, raw_rag_info)
    filtered_text, _ = get_gemini_chat_response(
        api_key,
        selected_model,
        [],
        filter_prompt
    )
```

这一步叫“细筛”。

含义：

```text
把向量检索出来的片段再交给 Gemini，让它判断哪些片段真的和当前需求相关。
```

这里 `history` 传的是空数组：

```python
[]
```

因为 RAG 过滤是一个独立任务，不需要参考之前的聊天历史。

如果模型认为没有相关资料：

```python
if "无相关参考资料" in filtered_text:
    final_rag_context = ""
else:
    final_rag_context = filtered_text
```

这就是项目 README 里说的“两阶段检索”：

```text
向量召回：找得到
LLM 过滤：找得准
```

---

## 20. 更新 Session State

```python
st.session_state['rag_context'] = final_rag_context
st.session_state['prd_context'] = preview_txt 
st.session_state['current_prompt_content'] = prompt_content
```

这三项很关键：

| key | 保存内容 |
|---|---|
| `rag_context` | 最终清洗后的 RAG 上下文 |
| `prd_context` | 当前需求摘要 |
| `current_prompt_content` | 后续点击“开始生成”时真正发给 Gemini 的内容 |

接着处理引用来源：

```python
if sources and final_rag_context:
    source_list = "\n".join(sources)
    st.session_state['rag_sources_list'] = f"\n{source_list}\n"
else:
    st.session_state['rag_sources_list'] = "经 AI 分析，知识库中暂无与当前 PRD 强相关的技术规范。"
```

最后记录已处理文件：

```python
st.session_state['processed_files'] = current_file_names
st.toast("✅ 知识库检索完成！")
```

---

## 21. 开始生成按钮

```python
btn_label = "🚀 开始生成" if not st.session_state['messages'] else "📤 发送补充文件并分析"
if st.button(btn_label, type="primary", use_container_width=True):
```

按钮文字会根据状态变化：

| 状态 | 按钮文案 |
|---|---|
| 还没有聊天记录 | 开始生成 |
| 已经有聊天记录 | 发送补充文件并分析 |

点击按钮后，先检查 API Key：

```python
if not api_key:
    st.error("请配置 API Key")
    st.stop()
```

---

## 22. 构造首次生成 Prompt

```python
initial_prompt = PromptManager.get_initial_prompt(
    st.session_state['prd_context'], 
    st.session_state['rag_context']
)
full_payload = initial_prompt + st.session_state.get('current_prompt_content', [])
```

这里把两类信息拼到一起：

```text
initial_prompt：文字指令，包括 PRD 摘要和 RAG 参考资料
current_prompt_content：用户上传的原始文件内容，可能包含图片/PDF/文本
```

`full_payload` 最终会发给 Gemini。

---

## 23. 调用 Gemini 生成测试用例

```python
resp_text, updated_history = get_gemini_chat_response(
    api_key,
    selected_model,
    st.session_state['gemini_history'],
    full_payload,
    system_instruction=PromptManager.CORE_SYSTEM_PROMPT
)
```

这里是核心调用。

参数解释：

| 参数 | 含义 |
|---|---|
| `api_key` | Gemini API Key |
| `selected_model` | 用户选择的模型 |
| `gemini_history` | 之前的模型对话历史 |
| `full_payload` | 本次用户输入和文件内容 |
| `CORE_SYSTEM_PROMPT` | 测试架构师角色和 JSON 输出规则 |

生成后保存历史和回复：

```python
st.session_state['gemini_history'] = updated_history
st.session_state['messages'].append({"role": "assistant", "content": resp_text})
```

---

## 24. 提取 JSON 并更新结果区

```python
json_data = extract_json_from_text(resp_text)
if json_data:
    st.session_state['res_data'] = json_data
    st.session_state['eval_report'] = None
```

如果 AI 回复里有合法 JSON，就保存到 `res_data`。

为什么清空 `eval_report`？

```text
因为测试用例重新生成了，旧评估报告已经不对应当前结果。
```

最后：

```python
del st.session_state['current_prompt_content'] 
st.rerun()
```

`st.rerun()` 会让页面重新运行，从而右侧立即显示新结果。

---

## 25. 聊天流渲染

```python
chat_container = st.container(height=500)
with chat_container:
```

这里创建一个固定高度的聊天区域。

### 25.1 展示 RAG 上下文

```python
if st.session_state.get('rag_context'):
    with st.expander("📚 本次对话参考的知识库片段 (RAG Context)", expanded=False):
```

如果本次有 RAG 内容，就展示引用来源和片段。

```python
fragments = st.session_state['rag_context'].split('<<<RAG_SEP>>>')
for frag in fragments:
    if frag.strip():
        st.info(frag.strip())
```

`<<<RAG_SEP>>>` 是 RAG 片段之间的分隔符。

### 25.2 展示消息记录

```python
for msg in st.session_state['messages']:
    with st.chat_message(msg["role"]):
```

Streamlit 的 `st.chat_message()` 会渲染聊天气泡。

如果是用户消息：

```python
st.markdown(msg["content"])
```

如果是 AI 消息：

```python
explanation, _ = split_text_and_json(msg["content"])
st.markdown(explanation)
```

AI 消息只优先展示解释部分，JSON 放到折叠区：

```python
with st.expander("🔍 查看 JSON 数据", expanded=False):
    st.code(..., language="json")
```

---

## 26. 底部聊天输入：多轮微调

```python
if prompt := st.chat_input("输入指令 (如: '增加几个异常场景')"):
```

这是用户后续修改用例的入口。

比如用户输入：

```text
增加 3 条异常登录场景
```

代码会先把用户消息加入聊天记录：

```python
st.session_state['messages'].append({"role": "user", "content": prompt})
```

然后构造修改 Prompt：

```python
refine_prompt_str = PromptManager.get_refinement_prompt(
    prompt,
    st.session_state['rag_context']
)
```

再调用 Gemini：

```python
resp_text, updated_history = get_gemini_chat_response(
    api_key,
    selected_model,
    st.session_state['gemini_history'],
    refine_prompt_str,
    system_instruction=PromptManager.CORE_SYSTEM_PROMPT
)
```

这里仍然传入 `gemini_history`，所以模型能知道之前生成过哪些用例。

如果本次回复里有新的 JSON：

```python
if new_json:
    st.session_state['res_data'] = new_json
    st.session_state['eval_report'] = None
    st.rerun()
```

也就是说：

```text
用户一句补充指令 -> AI 输出完整新 JSON -> 右侧表格自动更新
```

---

# 右侧：结果预览、编辑、评估、归档

## 27. 右侧结果区入口

```python
with col_preview:
    st.subheader("📄 实时结果预览")
```

如果还没有结果：

```python
st.info("👈 请在左侧上传 PRD 文档")
```

如果已经有 `res_data`：

```python
df = pd.DataFrame(st.session_state['res_data'])
```

把 JSON 测试用例转成 Pandas 表格。

---

## 28. 用例统计

```python
module_list = df['module'].unique() if 'module' in df.columns else []
st.caption(f"📊 当前共 **{len(df)}** 条用例 | 覆盖模块: {', '.join(module_list)}")
```

这里展示：

```text
当前生成了多少条测试用例
覆盖了哪些模块
```

如果 JSON 里有 `module` 字段，就统计模块列表。

---

## 29. 右侧三个子 Tab

```python
tab_table, tab_json, tab_eval = st.tabs(["📊 表格视图", "🔍 源码/编辑", "⚖️ 智能评估"])
```

| Tab | 功能 |
|---|---|
| 表格视图 | 展示测试用例表格和下载按钮 |
| 源码/编辑 | 直接编辑 JSON |
| 智能评估 | 对当前用例做质量评估 |

---

## 30. 表格视图

```python
with tab_table:
    display_results(df, st.session_state['res_data'])
```

`display_results()` 来自 `ui/components.py`。

它负责：

```text
1. 展示前 5 条测试用例
2. 提供 CSV 下载
3. 提供 JSON 下载
4. 提供 YAML 下载
5. 提供 Markdown 下载
```

这就是项目支持多格式导出的地方。

---

## 31. JSON 源码编辑

```python
with tab_json:
    json_str_val = json.dumps(st.session_state['res_data'], indent=2, ensure_ascii=False)
    edited_json_str = st.text_area("直接编辑 JSON", value=json_str_val, height=600)
```

这里把当前测试用例转换成格式化 JSON 字符串，让用户手动修改。

`ensure_ascii=False` 的作用：

```text
保证中文正常显示，不被转成 \u4e2d\u6587 这种形式。
```

`edited_json_str` 后面归档时会用到。

---

## 32. 智能评估 Tab

```python
with tab_eval:
    st.markdown("### 🕵️ 质量质检 & 智能对抗评估")
```

这个模块的目标：

```text
让 AI 扮演 QA 验收负责人，对生成的测试用例进行审查。
```

### 32.1 上传标准参考用例

```python
golden_file = st.file_uploader(
    "上传标准参考用例 (可选，作为对比标杆)",
    type=['json', 'txt', 'md'],
    help="如果有已存在的正确用例，上传后 AI 将进行对比分析"
)
```

如果用户上传了标准答案：

```python
golden_content = golden_file.getvalue().decode('utf-8')[:10000]
```

这里只取前 10000 个字符，避免内容太长。

### 32.2 点击评估按钮

```python
if st.button("⚖️ 开始全面评估", use_container_width=True):
```

如果评估器存在：

```python
report = evaluator.evaluate_cases(
    selected_model,
    st.session_state.get('prd_context', '无详细PRD'),
    st.session_state['res_data'],
    rag_context=st.session_state.get('rag_context', ''),
    golden_cases_content=golden_content
)
```

传给评估器的信息包括：

| 参数 | 含义 |
|---|---|
| `selected_model` | 用哪个 Gemini 模型评估 |
| `prd_context` | 原始需求信息 |
| `res_data` | 当前测试用例 |
| `rag_context` | 相关规范和历史案例 |
| `golden_content` | 可选标准答案 |

评估完成后：

```python
st.session_state['eval_report'] = report
```

---

## 33. 渲染评估报告

```python
if st.session_state['eval_report']:
    report = st.session_state['eval_report']
```

评估报告主要包含：

```json
{
  "score": 85,
  "summary": "整体质量不错，但缺少异常场景。",
  "coverage_gap": [],
  "logic_issues": [],
  "duplicates": [],
  "suggestions": []
}
```

页面展示分为三块：

### 33.1 分数和总评

```python
c_score.metric("质量评分", f"{score} 分", delta=None)
c_sum.info(f"**总评**: {report.get('summary', '无')}")
```

### 33.2 问题区

```python
coverage_gap  -> 漏测风险
logic_issues  -> 逻辑/幻觉风险
```

### 33.3 建议区

```python
duplicates   -> 重复冗余
suggestions  -> 改进方向
```

这个设计让用户不只拿到测试用例，还能看到“这批用例质量怎么样”。

---

## 34. 归档入库

```python
if st.button("💾 确认最终版并归档入库", type="primary", use_container_width=True):
```

点击后：

```python
final_data = json.loads(edited_json_str) if 'edited_json_str' in locals() else st.session_state['res_data']
```

如果用户在 JSON 编辑区改过内容，就用编辑后的版本；否则用原始 `res_data`。

接着生成摘要：

```python
summary = generate_summary(api_key, str(final_data), model_name=selected_model)
```

然后归档进历史案例库：

```python
rag_engine.add_history_case(
    st.session_state.get('prd_context', '对话生成的用例'),
    final_data,
    summary=summary
)
```

这一步非常重要，因为它实现了项目闭环：

```text
本次生成的优秀用例 -> 归档到历史库 -> 下次生成时可以被 RAG 检索出来参考
```

这就是 README 里说的“资产回流”。

---

# Tab 2：知识库管理

## 35. 知识库管理页面入口

```python
with tab_manage:
    st.header("🗂️ 知识库管理后台")
```

这个 Tab 负责管理两类知识：

```text
技术规范
历史案例
```

---

## 36. 上传新知识

```python
with st.expander("➕ 上传新知识", expanded=False):
    kb_file = st.file_uploader(
        "上传规范文档/历史资料",
        type=["txt", "md", "pdf", "jpg", "png"],
        key="kb_upload"
    )
```

支持上传：

```text
txt / md / pdf / jpg / png
```

点击上传并处理：

```python
if kb_file and st.button("上传并处理", key="kb_btn"):
```

处理逻辑：

```python
if "text" in kb_file.type:
    parsed_text = kb_file.getvalue().decode("utf-8")
else:
    parsed_text = rag_engine.parse_file_content(kb_file, kb_file.type, model_name=selected_model)
```

文本文件直接读取。

PDF 和图片交给 `rag_engine.parse_file_content()`，也就是用 Gemini 解析成文本。

然后生成摘要：

```python
summary = generate_summary(api_key, parsed_text[:5000], model_name=selected_model)
```

最后入库：

```python
rag_engine.add_knowledge(kb_file, summary=summary, content_text=parsed_text, model_name=selected_model)
```

这里会进入 `core/rag_engine.py`，完成：

```text
保存原始文件
文本切片
生成 embedding
写入 ChromaDB
```

---

## 37. 技术规范和历史案例双栏展示

```python
col_kb, col_hist = st.columns(2)
```

页面分两栏：

| 左栏 | 右栏 |
|---|---|
| 技术规范 | 历史案例 |

---

## 38. 内部函数 render_doc_list()

在 `main()` 里面定义了一个内部函数：

```python
def render_doc_list(doc_type, title, icon):
```

它负责展示某一类文档列表。

参数：

| 参数 | 含义 |
|---|---|
| `doc_type` | `knowledge` 或 `history` |
| `title` | 页面标题，比如“技术规范” |
| `icon` | 页面图标 |

---

## 39. 获取文档列表

```python
docs = rag_engine.list_documents(doc_type)
```

这一步从 ChromaDB 里取出文档元信息。

然后转成表格：

```python
df = pd.DataFrame(docs)
st.dataframe(df[["文件名/标题", "AI摘要", "录入时间", "ID"]], use_container_width=True, hide_index=True)
```

表格展示字段：

```text
文件名/标题
AI摘要
录入时间
ID
```

---

## 40. 删除文档

```python
del_id = c1.text_input("输入 ID 进行操作", key=input_key, placeholder=f"粘贴 ID")

if c2.button("🗑️ 删除", key=f"del_{doc_type}"):
    if del_id:
        rag_engine.delete_document(del_id, doc_type)
        st.success(f"ID {del_id} 已删除")
        st.rerun()
```

用户输入文档 ID，点击删除。

删除动作实际由 `rag_engine.delete_document()` 完成。

它会删除：

```text
ChromaDB 里的向量记录
可能还会删除本地原始文件
```

---

## 41. 预览文档

```python
if c2.button("👀 预览", key=f"view_{doc_type}"):
```

点击预览后，先根据 ID 找到目标文档：

```python
target = next((d for d in docs if d['ID'] == del_id), None)
```

然后读取内容：

```python
content = rag_engine.get_doc_content(
    target['原始路径'],
    doc_id=target['ID'],
    collection_type=doc_type
)
```

如果是历史案例：

```python
lang = "json" if doc_type == "history" else "markdown"
```

历史案例按 JSON 展示，技术规范按 Markdown 展示。

---

## 42. 渲染两个列表

```python
with col_kb:
    render_doc_list("knowledge", "技术规范", "📚")
with col_hist:
    render_doc_list("history", "历史案例", "🕰️")
```

这两行真正把左右两栏渲染出来。

---

## 43. 程序入口

```python
if __name__ == "__main__":
    main()
```

这表示：当这个文件被直接运行时，调用 `main()`。

启动命令是：

```powershell
streamlit run ui/main.py
```

Streamlit 会执行这个文件，最后进入 `main()`，页面就开始渲染。

---

# 44. 完整业务流程复述

你可以按下面这条线理解整个 `ui/main.py`：

```text
用户打开页面
-> render_sidebar() 输入 API Key，选择模型
-> 初始化 RAGEngine 和 Evaluator
-> 用户在左侧上传 PRD/PDF/图片/文本
-> main.py 把文件整理成 prompt_content 和 preview_txt
-> RAGEngine.search_context() 根据 preview_txt 检索规范和历史案例
-> Gemini 对 RAG 结果做二次过滤，得到 final_rag_context
-> 用户点击“开始生成”
-> PromptManager.get_initial_prompt() 构造生成 Prompt
-> get_gemini_chat_response() 调 Gemini 生成测试用例
-> extract_json_from_text() 提取 JSON
-> res_data 保存测试用例
-> 右侧 DataFrame 展示表格
-> 用户可以继续用 chat_input 微调用例
-> 用户可以点击智能评估，Evaluator 输出质量报告
-> 用户确认最终版后，add_history_case() 归档回历史案例库
```

---

# 45. 这个文件最核心的 5 个点

## 45.1 `main()` 是页面和业务入口

所有页面组件和业务流程都在 `main()` 里被组织起来。

## 45.2 `st.session_state` 是状态核心

因为 Streamlit 每次交互都会重跑脚本，所以必须用 `session_state` 保存聊天、RAG、结果、评估报告。

## 45.3 左侧负责输入，右侧负责结果

左侧是“需求对话”，右侧是“实时结果预览”。这就是项目的双屏共创体验。

## 45.4 RAG 是两阶段

```text
ChromaDB 向量召回 -> Gemini 语义过滤
```

这个设计能减少无关知识污染。

## 45.5 归档形成闭环

最终测试用例可以入库，后续作为历史案例继续被检索。

---

# 46. 面试时怎么讲 `ui/main.py`

可以这样回答：

> `ui/main.py` 是整个项目的 Streamlit 主入口，负责页面布局和业务流程编排。它先通过侧边栏读取 API Key 和模型，然后初始化 RAG 引擎和评估器。用户上传 PRD、PDF 或图片后，页面会先整理输入内容，再调用 RAGEngine 检索技术规范和历史案例，并用 LLM 做二次过滤。用户点击生成后，main.py 会通过 PromptManager 构造 Prompt，调用 Gemini 生成结构化测试用例 JSON，再转成 Pandas 表格展示。后续用户可以继续通过聊天框微调用例，也可以用 Evaluator 做质量评估，最后把确认后的用例归档回历史案例库，形成知识回流闭环。

---

# 47. 常见报错排查路径

## 47.1 页面启动失败

先看：

```text
streamlit run ui/main.py 是否执行成功
依赖是否安装完整
Python 版本是否是 3.10
```

重点文件：

```text
requirements.txt
ui/main.py
```

## 47.2 找不到 config 或 core 模块

重点看这行是否生效：

```python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

也要确认启动命令是在项目根目录执行的：

```powershell
streamlit run ui/main.py
```

## 47.3 API Key 或模型调用失败

优先看：

```text
config/settings.py
ui/sidebar.py
core/llm_client.py
```

检查：

```text
API Key 是否填写
代理是否可用
模型名是否可用
Gemini 配额是否耗尽
```

## 47.4 上传图片或 PDF 失败

优先看：

```text
PIL 是否安装
文件类型 file.type 是否正确
Gemini 多模态接口是否能访问
```

相关代码：

```text
ui/main.py 文件预处理部分
core/rag_engine.py parse_file_content()
```

## 47.5 右侧没有表格

说明 `res_data` 没有被成功写入。

排查：

```text
AI 回复里有没有合法 JSON
extract_json_from_text() 是否提取成功
Prompt 是否要求输出 JSON
```

相关文件：

```text
core/llm_client.py
config/prompts.py
ui/main.py
```

## 47.6 评估失败

排查：

```text
Evaluator 是否初始化成功
API Key 是否有效
评估 Prompt 返回的是否是合法 JSON
```

相关文件：

```text
core/evaluator.py
config/prompts.py
```

---

# 48. 今天要记住的一句话

> `ui/main.py` 不是单纯的页面文件，它是整个项目的业务总控：左侧收集需求，核心层生成和检索，右侧展示、评估并归档结果。

---

# 49. 学习检查问题

你学完这份文档后，应该能回答下面几个问题：

1. 为什么 `main.py` 里要初始化 `st.session_state`？
2. `messages` 和 `gemini_history` 有什么区别？
3. 用户上传文件后，`preview_txt` 和 `prompt_content` 分别干什么？
4. 为什么 RAG 要先向量检索，再让 LLM 过滤？
5. `res_data` 是什么时候被赋值的？
6. 右侧表格为什么要先把 JSON 转成 `DataFrame`？
7. 评估报告为什么要在重新生成用例后清空？
8. “确认最终版并归档入库”解决了什么问题？

---

# 50. 下一步建议

下一步建议继续学习：

```text
core/llm_client.py
```

因为 `ui/main.py` 只是调用模型，真正和 Gemini 通信的细节在 `core/llm_client.py` 里。

学习顺序建议：

```text
1. get_available_models()
2. get_gemini_chat_response()
3. extract_json_from_text()
4. generate_summary()
```
