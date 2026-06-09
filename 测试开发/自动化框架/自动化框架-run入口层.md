# 自动化框架 run 入口层

`run.py` 是这套框架的统一执行入口，主要负责两件事：

- 调用 pytest 跑测试
- 调用 allure 生成测试报告

代码很短，但作用明确。

## 1. pytest 执行部分

```python
pytest.main([
    "-vs",
    "./testcases/test_runner.py",
    "--alluredir",
    "./report/json_report",
    "--clean-alluredir"
])
```

这里的含义是：

- `-v`：显示更详细的测试信息
- `-s`：允许控制台直接打印输出
- `./testcases/test_runner.py`：指定执行测试文件
- `--alluredir`：把原始测试结果写入 allure 的 json 目录
- `--clean-alluredir`：执行前清空旧报告数据

## 2. allure 报告生成部分

```python
os.system("allure generate ./report/json_report -o ./report/html_report --clean")
```

这一步会把 pytest 产生的 allure 原始结果，转成可直接打开的 HTML 报告。

所以整个流程是：

```text
pytest执行测试
    ↓
输出allure原始数据
    ↓
allure生成html报告
```

## 3. 为什么要单独写入口层

如果不写统一入口，每次都要手敲 pytest 命令和 allure 命令，重复且容易出错。

把它们集中到 `run.py` 后，好处是：

- 一键执行
- 新人更容易上手
- 后续方便继续扩展，比如加环境参数、时间戳目录、失败重跑

## 4. 这一层在框架中的位置

可以把 `run.py` 理解成“启动器”：

- `data` 提供数据
- `utils` 负责读取数据
- `testcases` 负责执行逻辑
- `run.py` 负责把整套流程真正跑起来

## 5. 一句话总结

`run.py` 属于自动化框架的入口层，负责统一启动测试执行并产出测试报告。
