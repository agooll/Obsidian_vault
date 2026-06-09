# 自动化框架 testcases 执行层

`testcases/test_runner.py` 是这套框架的核心执行层，真正把 Excel 数据变成接口请求。

## 1. 执行层的定位

这一层不负责存数据，而是负责统一执行流程：

- 读取用例
- 参数化
- 渲染关联变量
- 发起请求
- 做断言
- 做提取

所以它相当于框架的“调度中枢”。

## 2. 类级数据设计

代码里有两个关键类属性：

```python
data = read_excel()
all = {}
```

含义分别是：

- `data`：所有待执行用例
- `all`：全局变量池，用来保存前面接口提取出来的数据

例如：

- 登录后提取 `TOKEN`
- 后续查询用户、上传图片时继续引用 `TOKEN`

## 3. pytest 参数化的作用

```python
@pytest.mark.parametrize("case", data)
```

这句的作用是把 Excel 中的每一行测试数据，都变成一次独立的测试执行。

也就是说：

- 不需要手写很多个测试函数
- 只要增加 Excel 行数，就能扩展用例

这就是数据驱动自动化的核心做法。

## 4. 用例执行主流程

### 4.1 获取全局变量池

```python
all = self.all
```

这样后续提取出来的数据都能写入统一容器。

### 4.2 写入 allure 报告分类

```python
allure.dynamic.feature(case["feature"])
```

这会把 Excel 中的模块名同步到报告里，方便按业务模块查看结果。

### 4.3 渲染模板变量

```python
case = eval(Template(str(case)).render(all))
```

它的作用是把类似：

```python
{"Authorization":"{{TOKEN}}"}
```

渲染成真实 token。

### 4.4 组装请求参数

执行层会从 Excel 当前行里取出：

- `method`
- `path`
- `headers`
- `params`
- `data`
- `json`
- `files`

然后统一封装成：

```python
request_data = {
    "method": method,
    "url": url,
    "headers": headers,
    "params": params,
    "data": data,
    "json": json,
    "files": files,
}
```

最后通过：

```python
requests.request(**request_data)
```

统一发起请求。

## 5. 断言机制

### 5.1 HTTP 断言

如果配置了 `check`，就用 `jsonpath` 从响应体里提取指定字段，再和 `expected` 比较。

如果没配 `check`，就退化成字符串包含断言：

```python
assert case["expected"] in res.text
```

这样兼顾了：

- 精确字段断言
- 简单文本断言

### 5.2 数据库断言

如果 Excel 配置了：

- `sql_check`
- `sql_expected`

就会连接 MySQL，执行查询，把查询结果和预期值比对。

这说明这套框架不只验证接口返回，还验证数据是否真正落库。

## 6. 提取机制

### 6.1 JSON 提取

如果 Excel 配了 `jsonExData`，就会按 key-value 遍历：

- key：保存到变量池里的变量名
- value：jsonpath 表达式

例如登录后把 `TOKEN` 存到 `all`。

### 6.2 SQL 提取

如果 Excel 配了 `sqlExData`，就会执行 SQL，然后把结果保存到全局变量池。

这适合从数据库里取：

- 用户名
- 订单号
- 业务 id

作为后续接口依赖数据。

## 7. 这一层的价值

执行层把所有接口共性的工作都抽象到了一套逻辑里：

- 同一套执行器跑所有用例
- 同一套断言逻辑跑不同接口
- 同一套提取逻辑完成接口关联

所以这层是自动化框架真正的“可复用核心”。

## 8. 当前实现的问题

- 使用 `eval()` 解析 headers、params、data、json、files，安全风险较高
- 数据库连接代码重复
- 基础 URL 写死
- 没有统一异常处理
- 全局变量池依赖类属性，共享状态要注意执行顺序

## 9. 一句话总结

`testcases` 层就是自动化框架的执行引擎，负责把 Excel 中定义的接口用例，统一转成“请求 + 断言 + 提取”的完整测试流程。
