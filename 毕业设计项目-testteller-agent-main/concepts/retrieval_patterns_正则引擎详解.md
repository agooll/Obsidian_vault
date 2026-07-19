# retrieval_patterns.py 正则引擎详解

## 结论
12 个正则表达式集中管理，覆盖测试 ID、API 路径、HTTP 方法、代码符号、环境变量、文件名、通用 token 等提取场景。所有检索层模块（QueryAnalyzer, LocalIndex）共享同一套模式。

## 核心模式

| 变量名 | 正则 | 用途 | 匹配示例 |
|---|---|---|---|
| `TEST_ID_PATTERN` | `r"\b(?:E2E\|INT\|TECH\|MOCK)_[A-Z0-9_]+\b"` | 测试用例 ID | `E2E_LOGIN_001` |
| `API_PATH_PATTERN` | `r"/(?:api/)?[A-Za-z0-9_./{}:-]+"` | API 路径 | `/api/login`, `/users/{id}` |
| `HTTP_METHOD_PATTERN` | `r"\b(?:GET\|POST\|PUT\|...)\b"` | HTTP 方法 | `POST`, `GET` |
| `PYTHON_CLASS_PATTERN` | `r"\bclass\s+([A-Za-z_]\w*)"` | Python 类名 | 捕获 `UserService` |
| `PYTHON_FUNCTION_PATTERN` | `r"\b(?:async\s+)?def\s+([A-Za-z_]\w*)"` | Python 函数名 | 捕获 `login` |
| `JS_TS_FUNCTION_PATTERN` | `r"\b(?:function\|const\|let\|var)\s+([A-Za-z_$]\w*)"` | JS/TS 函数/变量 | 捕获 `fetchUser` |
| `QUALIFIED_SYMBOL_PATTERN` | `r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b"` | 全限定符号 | `UserService.login` |
| `DATA_TESTID_PATTERN` | `r'''data-testid\s*=\s*["']([^"']+)["']'''` | 前端测试属性 | 捕获 `login-btn` |
| `ENV_GETENV_PATTERN` | `r'''os\.(?:getenv\|environ\[)\s*\(?\s*["']([A-Z][A-Z0-9_]+)["']'''` | 环境变量（Python） | 捕获 `DATABASE_URL` |
| `ENV_PROCESS_PATTERN` | `r"\bprocess\.env\.([A-Z][A-Z0-9_]+)\b"` | 环境变量（Node） | 捕获 `JWT_SECRET` |
| `ENV_TEMPLATE_PATTERN` | `r"\$\{([A-Z][A-Z0-9_]+)\}"` | 环境变量（模板） | 捕获 `API_BASE` |
| `FILE_NAME_PATTERN` | `r"\b[A-Za-z0-9_.-]+\.(?:py\|js\|ts\|...)\b"` | 文件名 | `app.py` |
| `TOKEN_PATTERN` | `r"[A-Za-z][A-Za-z0-9_-]*\|[\u4e00-\u9fff]{2,}"` | 通用分词 | `login`, `用户`, `测试用例` |

## 正则语法笔记

### `\b` — 单词边界
匹配单词字符（`[A-Za-z0-9_]`）和非单词字符之间的位置，防止部分匹配。

### `(?:...)` — 非捕获组
分组但不保存匹配结果。`findall()` 返回整个匹配而非捕获组。

### `[...]` — 字符类
方括号内任意一个字符即匹配。`[A-Z0-9_]+` = 大写字母、数字、下划线至少 1 个。

### `re.IGNORECASE`
大小写不敏感标志。

### 中文匹配关键：`[\u4e00-\u9fff]{2,}`
Unicode 中文字符集（CJK 统一表意文字），至少 2 个连续中文字符的支持。这是 QueryAnalyzer 做中文分词的"地基"——不用 NLP 库，纯靠正则。

## 验证
- source: `testteller/core/retrieval/retrieval_patterns.py:L5-L19`
- source: `testteller/core/retrieval/query_analyzer.py`（使用方）
- source: `testteller/core/retrieval/local_index.py`（使用方）

## 迁移场景
需要从自然语言或代码中提取结构化信息的任何系统。

## 下一次复习提示
- `TOKEN_PATTERN` 如何同时处理英文和中文文本？
- `QUALIFIED_SYMBOL_PATTERN` 的 `(?:\.[A-Za-z_]\w*)+` 中 `+` 的含义？
