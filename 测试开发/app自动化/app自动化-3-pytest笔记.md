### 99 pytest-1-基本使用-1-对比unittest

**对比**

```
https://blog.csdn.net/weixin_44530778/article/details/86737562
```

**特点**

```
1. 非常容易上手, 入门简单, 文档丰富
2. 支持简单的单元测试和复杂的功能测试
3. 支持运行由 unittest 编写的测试用例
4. 支持测试用例失败重试
5. 支持参数化
6. 执行测试过程中可以将某些测试用例跳过
7.支持对某些预期失败的用例做标记
```



### 100 pytest-1-基本使用-2-安装和运行方式

**安装**

```
pip install pytest
```

> 推荐: pip install pytest==3.10

**校验**

- pip list
- pytest --version

**运行**

```
import pytest


class TestDemo:

    def test_a(self):
        print("test_a")
        assert 1    # 断言成功

    def test_b(self):
        print("test_b")
        assert 0    # 断言失败

# 运行方式1:  命令行模式[推荐] 执行  pytest -s 文件名
# 运行方式2: 主函数模式

if __name__ == '__main__':
    pytest.main(["-s", "test_100_基本使用_安装和运行方式.py"])

# 运行结果
# . 表示成功
# F 表示失败
```



### 101 pytest-1-基本使用-3-前置和后置方法-1-函数级

**代码**

```
class TestDemo:

    # 函数级开始的方法
    def setup(self):
        print("-->setup")

    # 函数级结束的方法
    def teardown(self):
        print("-->teardown")

    def test_a(self):
        print("test_a")

    def test_b(self):
        print("test_b")

```



### 102 pytest-1-基本使用-3-前置和后置方法-2-类级

**代码**

```
class TestDemo:

    # 类级开始的方法
    def setup_class(self):
        print("====>setup_class")

    # 类级结束的方法
    def teardown_class(self):
        print("====>teardown_class")

    # 函数级开始的方法
    def setup(self):
        print("-->setup")

    # 函数级结束的方法
    def teardown(self):
        print("-->teardown")

    def test_a(self):
        print("test_a")

    def test_b(self):
        print("test_b")

```



### 103 pytest-1-基本使用-3-前置和后置方法-3-在什么位置放置驱动对象的获取和关闭

```
如果测试用例比较少, 页面层级不多, 可以放在类级setup_class和teardown_class中
如果测试用例比较多, 页面层级较深, 可以放在函数级setup和teardown中
```

> 推荐: 把驱动对象的获取和关闭, 放在函数级的 setup 和 teardown 中



### 104 pytest-1-基本使用-4-配置文件

pytest.ini

```
[pytest]
addopts = -s
testpaths = ./scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**注意点**

```
1. 运行时可以通过查看 inifile 的值, 来确认是否加载了配置文件
2. windows 下的配置文件中不能出现中文
3. 实际工作中复制粘贴即可, 只需要理解配置项
```



### 105 pytest-2-常用插件-1-测试报告

插件列表网址: <http://plugincompat.herokuapp.com/>

```
安装
	使用命令 pip install pytest-html
	推荐 pip install pytest-html==1.21.1
使用
	在配置文件中的命令行参数增加 --html=用户路径/report.html
```

> 在项目目录下会有一个文件夹对应存放测试报告, 文件夹内的 report.html 就是测试报告



### 106 pytest-2-常用插件-2-控制函数执行顺序

**安装**

```
使用命令 pip install pytest-ordering 进行安装
```

**使用**

```
标记于测试函数, @pytest.mark.run(order=x), 其中, x 是代表执行顺序的数字
```

**代码**

```
import pytest


class TestDemo:

    @pytest.mark.run(order=1)
    def test_demo1(self):
        print("1")

    @pytest.mark.run(order=-1)
    def test_demo2(self):
        print("-1")

    @pytest.mark.run(order=2)
    def test_demo3(self):
        print("2")

    @pytest.mark.run(order=-2)
    def test_demo4(self):
        print("-2")

    @pytest.mark.run(order=0)
    def test_demo5(self):
        print("0")

    @pytest.mark.run(order=1.5)
    def test_demo6(self):
        print("1.5")

    @pytest.mark.run(order=-1.5)
    def test_demo7(self):
        print("-1.5")

    def test_demo8(self):
        print("nothing")

# 根据 order 值排列执行顺序, 由先到后
# 0 > 较小的正数 > 较大的正数 > 什么都不写 > 较小的负数 > 较大的负数

```



### 108 pytest-2-常用插件-3-失败重试

**安装**

```
pip install pytest-rerunfailures
```

**使用**

```
在配置文件中的命令行参数增加  --reruns n, n 是表示失败重试的次数
```

**示例**

pytest.ini 文件中 addopts = -s --html=report/report.html --reruns 3

**代码**

```
class TestDemo:

    def test_a(self):
        print("test_a")
        assert 1

    def test_b(self):
        print("test_b")
        assert 0

# 执行结果 R 表示需要重试
# 如果, 在重试的过程中, 成功了, 那么最终结果是成功, 后续不再重试
# 如果, 在重试之后, 结果依然是失败的, 那么最终执行结果是失败
```



### 109 pytest-3-高级用法-1-跳过测试函数

**方法**

```
# 跳过测试函数

@pytest.mark.skipif(condition, reason=None)
# 参数:
#	condition: 跳过测试函数的条件, 必传
#	reason: 标注原因, 必传
```

**使用**

```
在需要跳过的测试函数上, 加上装饰器 @pytest.mark.skipif(condition, reason="xxx")
```

**代码**

```
import pytest


class TestDemo:

# 比如: 现在平台是 android, 版本号 6.0
# 需要在 android 平台 版本大于4.0的时候跳过 test_c 函数

    current_platform = "android"
    current_version = 6.0
    flag = (current_platform == "android") and (current_version > 4.0)

    def test_a(self):
        print("test_a")

    @pytest.mark.skipif(True, reason=None)
    def test_b(self):
        print("test_b")

# s 表示测试函数被跳过

    @pytest.mark.skipif(flag, reason=None)
    def test_c(self):
        print("test_c")
```



### 110 pytest-3-高级用法-2-预期失败

**方法**

```
# 预期失败

@pytest.mark.xfail(condition=True, reason=None)
# 参数:
#	condition: 预期失败的条件, 必传
#	reason: 标注原因, 必传
```

**使用**

```
在需要标记预期失败的测试函数上, 加上装饰器 @pytest.mark.xfail(condition, reason="xxx")
```

**代码**

```
import pytest


class TestDemo:

    def test_a(self):
        print("test_a")
        assert 1

    def test_b(self):
        print("test_b")
        assert 0

    @pytest.mark.xfail(condition=True, reason=None)
    def test_c(self):   # 预期失败, 但是结果成功了
        print("test_c")
        assert 1

    @pytest.mark.xfail(condition=True, reason=None)
    def test_d(self):   # 预期失败, 结果失败了
        print("test_d")
        assert 0

# X 表示预期失败, 但结果成功, 结果和预期不一致, 是 bug
# x 表示预期失败, 结果失败, 结果和预期一致, 不是 bug
```



### 111 pytest-3-高级用法-3-数据参数化-1-总体介绍

**方法**

```
# 数据参数化

@pytest.mark.parametrize(argnames, argvalues)
# 参数:
#	argnames: 参数名
#	argvalues: 参数对应的值, 必须为可迭代类型, 一般使用 list
```

**代码**

```
class TestDemo:

# 不使用数据参数化, 分别打印用户名 "zhangsan" 和 "lisi"

    def test_a(self):
        print("zhangsan")

    def test_b(self):
        print("lisi")

```



### 112 pytest-3-高级用法-3-数据参数化-2-单一参数

**代码**

```
import pytest


class TestDemo:

# 使用单一参数的数据参数化, 修改之前的代码
# 分别打印用户名 "zhangsan" 和 "lisi"

    @pytest.mark.parametrize("name", ["zhangsan", "lisi"])
    def test_a(self, name):
        print(name)
```



### 113 pytest-3-高级用法-3-数据参数化-3-多个参数

**代码**

```
import pytest


class TestDemo:

# 使用多个参数的数据参数化, 分别打印 用户名和密码 :  zhangsan / 111111 和 lisi / 222222

    @pytest.mark.parametrize(("name", "password"), [("zhangsan", "111111"), ("lisi", "222222")])
    def test_a(self, name, password):
        print(name + "/" + password)
```



### 114 pytest-3-高级用法-3-数据参数化-4-推荐用法

**代码**

```
import pytest


class TestDemo:

# 增加数据可读性, 使用字典作为参数列表中的元素, 修改下面的内容:
# 分别打印 用户名和密码 :  zhangsan / 111111 和 lisi / 222222

    @pytest.mark.parametrize("info", [{"name": "zhangsan", "password": "111111"}, {"name": "lisi", "password": "222222"}])
    def test_a(self, info):
        print(info)

```



### 115 pytest-4-fixture-1-总体介绍

```
应用场景
	用 fixture 装饰器来标记固定的工厂函数, 在其他函数, 类调用它的时候会被激活并优先执行, 通常用于完成预置处理和重复操作
	
使用步骤
	1. 标记
		某个函数作为工厂, (如: 标记一个函数名为 before 的函数为工厂函数)
	2. 引用
		指定一个函数, 引用这个工厂(如: 制定一个函数名为 test_a 的函数去引用 before)
	备注
		效果: 如 test_a 引用了 工厂函数before, 那么 会先执行 before 再执行 test_a
		
标记方式
# 在函数上使用装饰器 @pytest.fixture() 来标记工厂函数
# 参数:
#      略

@pytest.fixture()
def before(self):
      pass
```



### 116 pytest-4-fixture-2-引用方式-1-通过参数引用

**代码**

```
# 要求: 通过参数的方式引用工厂函数 (如: 工厂函数为 before)
import pytest


class TestDemo:

    @pytest.fixture()
    def before(self):
        print("before")

    def test_a(self, before):   # test_a 以参数的形式引用工厂函数 before
        print("test_a")

    def test_b(self, before):   # test_b 以参数的形式引用工厂函数 before
        print("test_b")
```



### 117 pytest-4-fixture-2-引用方式-2-通过装饰器引用

**代码**

```
# 要求: 通过装饰器的方式引用工厂函数 (如: 工厂函数为 before)
import pytest


class TestDemo:

    @pytest.fixture()
    def before(self):
        print("before")

    def test_a(self, before):   # test_a 以参数的形式引用工厂函数 before
        print("test_a")

    @pytest.mark.usefixtures("before")
    def test_b(self):   # test_b 以装饰器的形式引用工厂函数 before
        print("test_b")
```



### 118 pytest-4-fixture-2-引用方式-3-扩展

**代码**

```
import pytest

# 1.使用 test_a 和 test_b 引用 before, 使用 fixture 方式
# 2.使用 test_a 和 test_b 引用 before, 使用 setup 方式

class TestDemo:

# 1. 使用 fixture 方式引用 before
    @pytest.fixture()
    def before(self):
        print("before")

    def test_a(self, before):
        print("test_a")

    def test_b(self, before):
        print("test_b")

# # 2. 使用 setup 方式引用 before
#     def before(self):
#         print("before")
#
#     def setup(self):
#         self.before()
#
#     def test_a(self):
#         print("test_a")
#
#     def test_b(self):
#         print("test_b")

# 思考: 此时如果 test_b 不想引用 before 了呢???
# 结论: fixture 方式 比 setup 方式更为灵活
```



### 119 pytest-4-fixture-3-参数-1-默认运行

**代码**

```
import pytest

class TestDemo:

    @pytest.fixture(autouse=True)
    def before(self):
        print("before")

    def test_a(self):
        print("test_a")

    def test_b(self):
        print("test_b")

# @pytest.fixture(autouse=Flase)
# 参数: autouse, 默认值为 Flase   表示不会自动引用
# 如果 autouse=True, 表示测试函数可以自动引用工厂函数
```



### 120 pytest-4-fixture-3-参数-2-作用域

**代码**

```
import pytest


@pytest.fixture(autouse=True, scope="function")
def before2():
    print("before2--类外部的--函数级")

@pytest.fixture(autouse=True, scope="class")
def before3():
    print("before3--类外部的--类级")

class TestDemo:

    def setup_class(self):
        print("setup_class")

    def setup(self):
        print("setup")

    @pytest.fixture(autouse=True, scope="function")
    def before(self):
        print("before--类内部的--函数级")

    @pytest.fixture(autouse=True, scope="class")
    def before1(self):
        print("before1--类内部的--类级")

    def test_a(self):
        print("test_a")

class TestDemo1:

    def test_b(self):
        print("test_b")

# 写在测试类里面的工厂函数: 只对所在的测试类有效
# 写在测试类外面的工厂函数: 对该 py 文件内的所有测试类有效

# 推荐用法:
#   作用域为 function 的工厂函数, 写在类的内部
#   作用域为 class 的工厂函数, 写在类的外部

# @pytest.fixture(scope="function")   作用域的默认值是 function,  可以改为  class
```



### 121 pytest-4-fixture-3-参数-3-参数化

**方法**

```
# 参数化

@pytest.fixture(params=None)
# 参数:
# 	params,  默认值为 None
```

> params 是一个列表, 列表中有多少个元素, 脚本就会运行多少次
>
> 如果想要获取 params 中的数据,  需要在 fixture 里面加上 request 参数, 这个参数名必须叫  request, 通过这个参数的 param 属性获取值 (通过request.param获取对应的参数值)

**代码**

```
import pytest


class TestDemo:

    @pytest.fixture(params=[1, 2])
    def before(self, request):
        print("before")
        print(request.param)

    def test_a(self, before):
        print("test_a")
```



### 122 pytest-4-fixture-4-返回值

**代码**

```
import pytest


class TestDemo:

    @pytest.fixture(params=[1, 2])
    def before(self, request):
        print("before")
        return request.param + 5

    def test_a(self, before):
        print("test_a")
        print(before)
```



### 123 pytest-4-fixture-4-返回值[拓展]

**代码**

```
import pytest


class TestDemo:

    @pytest.fixture(params=[1, 2, 3])
    def before(self, request):
        return request.param

    @pytest.mark.parametrize("num", [4, 5, 6, 7])
    def test_a(self, before, num):
        print("%d --- %d" % (before, num))
```

> 如果使用 fixture 参数化的同时, 也是用了 @pytest.mark.parametrize 这种参数化, 可以达到 "量量组合" 的效果, 比如, fixture 的 params 里有3个元素, 脚本参数化里有4个元素, 那么这个脚本会运行 12 次



### 124 pytest-5-小结





















































