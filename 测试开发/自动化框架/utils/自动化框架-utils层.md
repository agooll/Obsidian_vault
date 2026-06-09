![](assets/自动化框架-utils层/file-20260609155337365.png)

# 自动化框架 utils 工具层

当前项目的 `utils` 层只有一个核心文件：`excel_utils.py`，职责很明确，就是把 Excel 测试数据读取成执行层可以直接使用的数据结构。

## 1. utils 层的定位

在自动化框架里，`utils` 层通常不直接执行业务接口，而是负责：

- 读取测试数据
- 处理公共参数
- 封装通用方法
- 给执行层提供可复用能力

这个示例里，它承担的是“测试数据装配器”的角色。

## 2. `read_excel()` 做了什么

它的执行流程可以拆成几步：

### 2.1 打开 Excel 文件

```python
workbook = openpyxl.load_workbook("./data/测试用例.xlsx")
```

说明：

- 数据源放在 `data` 目录
- `utils` 层负责把原始文件转成 Python 数据

### 2.2 选择工作表

```python
worksheet = workbook["Sheet1"]
```

表示当前只读取 `Sheet1`，也说明这套框架的有效用例都集中在这个 sheet。

### 2.3 读取字段名

```python
keys = [cell.value for cell in worksheet[2]]
```

这里拿的是第二行，而不是第一行。

原因是这份 Excel 设计成了：

- 第一行：中文说明，方便人看
- 第二行：程序字段名，方便代码取值

所以第二行才是真正用来组装字典 key 的一行。

### 2.4 逐行读取测试数据

```python
for row in worksheet.iter_rows(min_row=3, values_only=True):
```

表示从第三行开始拿测试数据，前两行都属于表头说明。

### 2.5 把每一行组装成字典

```python
dict_data = dict(zip(keys, row))
```

这一句非常关键，它把：

- 字段名列表 `keys`
- 当前行数据 `row`

一一配对，最后生成一条标准测试用例字典。

例如：

```python
{
    "method": "post",
    "path": "/login",
    "data": {"username": "admin", "password": "123456"}
}
```

## 3. 为什么常用 `列表[字典]`

当前代码的写法是：

```python
data = []
...
data.append(dict_data)
```

这样做是因为：

- 一个字典表示一条测试用例
- 一个列表表示多条测试用例

所以最终返回 `list[dict]`，是最适合 Excel 多行数据的结构。

例如：

```python
[
    {"title": "管理员登录成功", "method": "post"},
    {"title": "查询用户列表成功", "method": "get"}
]
```

执行层后续就可以直接：

```python
for case in data:
    ...
```

## 4. 为什么不能只返回一个字典

如果只用一个字典：

```python
data = {"title": "管理员登录成功", "method": "post"}
```

那只能表示一条数据。

而 Excel 里通常有很多行用例，所以必须有一个“外层容器”来装多条记录，这个容器最自然的就是列表。

## 5. `is_true` 开关的作用

代码里还有一段过滤逻辑：

```python
if dict_data["is_true"]:
    data.append(dict_data)
```

意思是：

- `is_true` 为真，当前用例加入执行队列
- `is_true` 为空或假，当前用例跳过

这相当于给 Excel 加了一个“是否执行”的总开关。

优点是：

- 临时屏蔽用例不用删行
- 维护回归集更方便
- 调试时可以快速控制执行范围

## 6. 为什么要用 `zip()`

`zip(keys, row)` 的本质是“把表头和当前行数据配对”。

例如：

```python
keys = ["method", "path", "expected"]
row = ["post", "/login", "登录成功"]
```

那么：

```python
dict(zip(keys, row))
```

就会得到：

```python
{
    "method": "post",
    "path": "/login",
    "expected": "登录成功"
}
```

所以 `zip()` 是 Excel 行数据转测试用例字典的关键桥梁。

## 7. 这层对整个框架的价值

如果没有 `utils` 层，执行层就得自己处理：

- 打开 Excel
- 解析表头
- 逐行读取
- 过滤用例

这样职责会混乱。

把这些动作抽到 `utils` 之后，好处是：

- `testcases` 层更专注执行
- 数据来源更容易替换
- 后续可以继续扩展更多工具方法

## 8. 当前实现的不足

- Excel 路径写死
- 只支持 `Sheet1`
- 没有异常处理
- 强依赖 `openpyxl`
- 返回的数据后续仍要靠 `eval()` 做二次解析

所以它适合教学和入门，但工程化上还可以继续拆分。

## 9. 一句话总结

`utils` 层在这套自动化框架里负责“把 Excel 原始数据加工成 `list[dict]` 测试用例集合”，是数据驱动执行前的第一道公共封装。
