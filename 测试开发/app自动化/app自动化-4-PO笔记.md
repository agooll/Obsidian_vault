### 125 PO-0-总体介绍



### 126 PO-1-PO模式简介

**概念**

PO 是 Page Object 的缩写, PO 模式是自动化测试项目开发实践最佳模式之一

> 核心思想是通过对页面元素的封装减少冗余代码, 以便后期维护

**优点**

- 减少冗余代码
- 业务代码和测试代码被分开, 降低耦合性
- 维护成本低

**缺点**

- 结构复杂: 基于流程做了模块化的拆分

> 任何事物都是有利有弊, 对PO而言, 一定是利大于弊



### 127 PO-2-封装过程-1-项目准备

**需求** 

- 更多-移动网络-首选网络类型-点击2G 
- 更多-移动网络-首选网络类型-点击3G 
- 显示-搜索按钮-输入hello-点击返回

> ```
> # 搜索按钮(放大镜)
> content-desc 值为 搜索
> # 输入框
> resource-id 值为 android:id/search_src_text
> # 返回按钮
> class 值为 android.widget.ImageButton
> # 其余元素都通过 xpath 查找 text 属性即可
> ```

**目录**

```
- scripts
- - test_setting.py
- pytest.ini
```

**代码**

pytest.ini

```
[pytest]
addopts = -s
testpaths = ./scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

test_setting.py

```
import time
from appium import webdriver


class TestSetting:

    def setup(self):
        desired_caps = dict()
        desired_caps["platformName"] = "android"
        desired_caps["platformVersion"] = "5.1"
        desired_caps["deviceName"] = "127.0.0.1:62001"
        desired_caps["appPackage"] = "com.android.settings"
        desired_caps["appActivity"] = ".Settings"
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 2G
        self.driver.find_element_by_xpath("//*[@text='2G']").click()

    def test_more_3g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 3G
        self.driver.find_element_by_xpath("//*[@text='3G']").click()

    def test_display_search(self):
        # 点击 显示
        self.driver.find_element_by_xpath("//*[@text='显示']").click()
        # 点击 搜索(放大镜)
        self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()
        # 输入 hello
        self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")
        # 点击 返回
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()

```

> 思考:
>
> 一个 test_setting.py 脚本放了3条测试用例, 可否按照功能将3个测试用例分开, 以后如果要修改, 只要找到对应的脚本就好了



### 128 PO-2-封装过程-2-把测试脚本按照功能进行拆分

**需求**

将一个脚本, 按照功能, 拆成多个

> 属于两个测试模块的功能, 就应该拆成两个

**好处**

如果以后需要修改 "显示" 相关的内容, 直接去找 test_display.py 就好了

**目录**

```
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```

**代码**

test_more.py

```
import time
from appium import webdriver


class TestMore:

    def setup(self):
        desired_caps = dict()
        desired_caps["platformName"] = "android"
        desired_caps["platformVersion"] = "5.1"
        desired_caps["deviceName"] = "127.0.0.1:62001"
        desired_caps["appPackage"] = "com.android.settings"
        desired_caps["appActivity"] = ".Settings"
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 2G
        self.driver.find_element_by_xpath("//*[@text='2G']").click()

    def test_more_3g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 3G
        self.driver.find_element_by_xpath("//*[@text='3G']").click()
```

test_display.py

```
import time
from appium import webdriver


class TestDisplay:

    def setup(self):
        desired_caps = dict()
        desired_caps["platformName"] = "android"
        desired_caps["platformVersion"] = "5.1"
        desired_caps["deviceName"] = "127.0.0.1:62001"
        desired_caps["appPackage"] = "com.android.settings"
        desired_caps["appActivity"] = ".Settings"
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_display_search(self):
        # 点击 显示
        self.driver.find_element_by_xpath("//*[@text='显示']").click()
        # 点击 搜索(放大镜)
        self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()
        # 输入 hello
        self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")
        # 点击 返回
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

> 思考:
>
> test_display.py 和 test_more.py 都有前置代码, 如果要修改某个参数, 要改两处, 应怎样优化?



### 129 PO-2-封装过程-3-抽取前置代码

**需求**

将前置代码抽取出来, 可以复用

**步骤**

1. 在项目下新建一个 base 包
2. 在 base 中新建一个 base_driver.py
3. 将"前置代码" 放在 base_driver.py 中的 init_driver 函数中
4. 在 test_xxx.py 中的 setup 调用 init_driver 函数即可, 并获取 self.driver

**目录**

```
- base
- - base_driver.py
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```

**代码**

base_driver.py

```
from appium import webdriver


def init_driver():
    desired_caps = dict()
    desired_caps["platformName"] = "android"
    desired_caps["platformVersion"] = "5.1"
    desired_caps["deviceName"] = "127.0.0.1:62001"
    desired_caps["appPackage"] = "com.android.settings"
    desired_caps["appActivity"] = ".Settings"
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)
    return driver
```

test_display.py

```
import time
from V3_抽取前置代码.base.base_driver import init_driver


class TestDisplay:

    def setup(self):
        self.driver = init_driver()

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_display_search(self):
        # 点击 显示
        self.driver.find_element_by_xpath("//*[@text='显示']").click()
        # 点击 搜索(放大镜)
        self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()
        # 输入 hello
        self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")
        # 点击 返回
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

test_more.py

```
import time
from V3_抽取前置代码.base.base_driver import init_driver


class TestMore:

    def setup(self):
        self.driver = init_driver()

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 2G
        self.driver.find_element_by_xpath("//*[@text='2G']").click()

    def test_more_3g(self):
        # 点击 更多
        self.driver.find_element_by_xpath("//*[@text='更多']").click()
        # 点击 移动网络
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()
        # 点击 首选网络类型
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()
        # 点击 3G
        self.driver.find_element_by_xpath("//*[@text='3G']").click()
```

> 思考:
>
> 如果元素的 text 内容, 由 "移动网络" 改为 "移动网络1", 脚本需要改动两处, 应如何优化?



### 130 PO-2-封装过程-4-抽取操作到page-1-总体介绍

**需求**

将之前的 "self.driver.find_element_by_xpath("//*[@text='移动网络']").click()" 这种操作, 都写成函数, 并且放在page中, scripts 中的 test 脚本, 负责调用

**好处**

- 代码复用
- 如果 ui 有变更, 去找 page
- 如果 操作的顺序 有变更, 去找 scripts

**目录**

```
- page
- - display_page.py
- - more_page.py
- base
- - base_driver.py
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```



### 131 PO-2-封装过程-4-抽取操作到page-2-抽取操作

display_page.py

```
class DisplayPage:

    # 点击 显示
    def click_display(self):
        self.driver.find_element_by_xpath("//*[@text='显示']").click()

    # 点击 搜索(放大镜)
    def click_search(self):
        self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()

    # 输入 hello
    def input_search(self):
        self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")

    # 点击 返回
    def click_back(self):
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

more_page.py

```
class MorePage:

    # 点击 更多
    def click_more(self):
        self.driver.find_element_by_xpath("//*[@text='更多']").click()

    # 点击 移动网络
    def click_mobile_network(self):
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()

    # 点击 首选网络类型
    def click_first_network(self):
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()

    # 点击 2G
    def click_2g(self):
        self.driver.find_element_by_xpath("//*[@text='2G']").click()

    # 点击 3G
    def click_3g(self):
        self.driver.find_element_by_xpath("//*[@text='3G']").click()
```



### 132 PO-2-封装过程-4-抽取操作到page-3-调用操作

display_page.py

```
class DisplayPage:

    def __init__(self, driver):
        self.driver = driver

    # 点击 显示
    def click_display(self):
        self.driver.find_element_by_xpath("//*[@text='显示']").click()

    # 点击 搜索(放大镜)
    def click_search(self):
        self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()

    # 输入 hello
    def input_search(self):
        self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")

    # 点击 返回
    def click_back(self):
        self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

more_page.py

```
class MorePage:

    def __init__(self, driver):
        self.driver = driver

    # 点击 更多
    def click_more(self):
        self.driver.find_element_by_xpath("//*[@text='更多']").click()

    # 点击 移动网络
    def click_mobile_network(self):
        self.driver.find_element_by_xpath("//*[@text='移动网络']").click()

    # 点击 首选网络类型
    def click_first_network(self):
        self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()

    # 点击 2G
    def click_2g(self):
        self.driver.find_element_by_xpath("//*[@text='2G']").click()

    # 点击 3G
    def click_3g(self):
        self.driver.find_element_by_xpath("//*[@text='3G']").click()
```

test_display.py

```
import time
from V4_抽取操作到page.base.base_driver import init_driver
from V4_抽取操作到page.page.display_page import DisplayPage


class TestDisplay:

    def setup(self):
        self.driver = init_driver()
        self.display_page = DisplayPage(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_display_search(self):
        # 点击 显示
        self.display_page.click_display()
        # 点击 搜索(放大镜)
        self.display_page.click_search()
        # 输入 hello
        self.display_page.input_search()
        # 点击 返回
        self.display_page.click_back()

```

test_more.py

```
import time
from V4_抽取操作到page.base.base_driver import init_driver
from V4_抽取操作到page.page.more_page import MorePage


class TestMore:

    def setup(self):
        self.driver = init_driver()
        self.more_page = MorePage(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.more_page.click_more()
        # 点击 移动网络
        self.more_page.click_mobile_network()
        # 点击 首选网络类型
        self.more_page.click_first_network()
        # 点击 2G
        self.more_page.click_2g()

    def test_more_3g(self):
        # 点击 更多
        self.more_page.click_more()
        # 点击 移动网络
        self.more_page.click_mobile_network()
        # 点击 首选网络类型
        self.more_page.click_first_network()
        # 点击 3G
        self.more_page.click_3g()
```

> 思考:
>
> 在 xxx_page.py 中, 如果要修改某个元素, 需要到方法中去找对应的元素, 有没有更好的方法?



### 133 PO-2-封装过程-5-抽取元素和定位方法-1-总体介绍

**好处**

- 代码可以复用
- page的代码更简洁

**目录**

```
- base
- - base_driver.py
- - base_action.py
- page
- - display_page.py
- - more_page.py
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```



### 134 PO-2-封装过程-5-抽取元素和定位方法-2-抽取元素

display_page.py

```
from selenium.webdriver.common.by import By


class DisplayPage:

    display_button = By.XPATH, "//*[@text='显示']"

    search_buttion = By.XPATH, "//*[@content-desc='搜索']"

    input_button = By.ID, "android:id/search_src_text"

    back_button = By.CLASS_NAME, "android.widget.ImageButton"

    def __init__(self, driver):
        self.driver = driver

    def find_el(self, feature):
        by, value = feature
        return self.driver.find_element(by, value)

    # 点击 显示
    def click_display(self):
        self.find_el(self.display_button).click()
        # self.driver.find_element(self.display_button[0], self.display_button[1]).click()
        # self.driver.find_element_by_xpath("//*[@text='显示']").click()

    # 点击 搜索(放大镜)
    def click_search(self):
        self.find_el(self.search_buttion).click()
        # self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()

    # 输入 hello
    def input_search(self):
        self.find_el(self.input_button).send_keys("hello")
        # self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")

    # 点击 返回
    def click_back(self):
        self.find_el(self.back_button).click()
        # self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

more_page.py

```
from selenium.webdriver.common.by import By


class MorePage:

    more_button = By.XPATH, "//*[@text='更多']"

    mobile_network_button = By.XPATH, "//*[@text='移动网络']"

    first_network_button = By.XPATH, "//*[@text='首选网络类型']"

    network_2g_button = By.XPATH, "//*[@text='2G']"

    network_3g_button = By.XPATH, "//*[@text='3G']"

    def __init__(self, driver):
        self.driver = driver

    def find_el(self, feature):
        by, value = feature
        return self.driver.find_element(by, value)

    # 点击 更多
    def click_more(self):
        self.find_el(self.more_button).click()
        # self.driver.find_element_by_xpath("//*[@text='更多']").click()

    # 点击 移动网络
    def click_mobile_network(self):
        self.find_el(self.mobile_network_button).click()
        # self.driver.find_element_by_xpath("//*[@text='移动网络']").click()

    # 点击 首选网络类型
    def click_first_network(self):
        self.find_el(self.first_network_button).click()
        # self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()

    # 点击 2G
    def click_2g(self):
        self.find_el(self.network_2g_button).click()
        # self.driver.find_element_by_xpath("//*[@text='2G']").click()

    # 点击 3G
    def click_3g(self):
        self.find_el(self.network_3g_button).click()
        # self.driver.find_element_by_xpath("//*[@text='3G']").click()
```

> 思考:
>
> xxx_page.py 都有 find_el 函数, 该如何优化?



### 135 PO-2-封装过程-5-抽取元素和定位方法-3-抽取定位方法

base_action.py

```
class BaseAction:

    def __init__(self, driver):
        self.driver = driver

    def find_el(self, feature):
        by, value = feature
        return self.driver.find_element(by, value)
```

display_page.py

```
from selenium.webdriver.common.by import By

from V5_抽取元素和定位方法.base.base_action import BaseAction


class DisplayPage(BaseAction):

    display_button = By.XPATH, "//*[@text='显示']"

    search_buttion = By.XPATH, "//*[@content-desc='搜索']"

    input_button = By.ID, "android:id/search_src_text"

    back_button = By.CLASS_NAME, "android.widget.ImageButton"

    # 点击 显示
    def click_display(self):
        self.find_el(self.display_button).click()
        # self.driver.find_element(self.display_button[0], self.display_button[1]).click()
        # self.driver.find_element_by_xpath("//*[@text='显示']").click()

    # 点击 搜索(放大镜)
    def click_search(self):
        self.find_el(self.search_buttion).click()
        # self.driver.find_element_by_xpath("//*[@content-desc='搜索']").click()

    # 输入 hello
    def input_search(self):
        self.find_el(self.input_button).send_keys("hello")
        # self.driver.find_element_by_id("android:id/search_src_text").send_keys("hello")

    # 点击 返回
    def click_back(self):
        self.find_el(self.back_button).click()
        # self.driver.find_element_by_class_name("android.widget.ImageButton").click()
```

more_page.py

```
from selenium.webdriver.common.by import By

from V5_抽取元素和定位方法.base.base_action import BaseAction


class MorePage(BaseAction):

    more_button = By.XPATH, "//*[@text='更多']"

    mobile_network_button = By.XPATH, "//*[@text='移动网络']"

    first_network_button = By.XPATH, "//*[@text='首选网络类型']"

    network_2g_button = By.XPATH, "//*[@text='2G']"

    network_3g_button = By.XPATH, "//*[@text='3G']"

    # 点击 更多
    def click_more(self):
        self.find_el(self.more_button).click()
        # self.driver.find_element_by_xpath("//*[@text='更多']").click()

    # 点击 移动网络
    def click_mobile_network(self):
        self.find_el(self.mobile_network_button).click()
        # self.driver.find_element_by_xpath("//*[@text='移动网络']").click()

    # 点击 首选网络类型
    def click_first_network(self):
        self.find_el(self.first_network_button).click()
        # self.driver.find_element_by_xpath("//*[@text='首选网络类型']").click()

    # 点击 2G
    def click_2g(self):
        self.find_el(self.network_2g_button).click()
        # self.driver.find_element_by_xpath("//*[@text='2G']").click()

    # 点击 3G
    def click_3g(self):
        self.find_el(self.network_3g_button).click()
        # self.driver.find_element_by_xpath("//*[@text='3G']").click()
```

> 思考:
>
> 如何把显示等待封装到 find_el 函数中



### 136 PO-2-封装过程-6-优化base_action-1-增加显式等待

base_driver.py

```
from appium import webdriver


def init_driver():
    desired_caps = dict()
    desired_caps["platformName"] = "android"
    desired_caps["platformVersion"] = "5.1"
    desired_caps["deviceName"] = "127.0.0.1:62001"
    desired_caps["appPackage"] = "com.android.settings"
    desired_caps["appActivity"] = ".Settings"
    return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

```

base_action.py

```
from selenium.webdriver.support.wait import WebDriverWait


class BaseAction:

    def __init__(self, driver):
        self.driver = driver

    def find_el(self, feature, timeout=10, poll=1):
        """
        找一个元素
        :param feature: 元素特征
        :param timeout: 超时时间, 默认是10s
        :param poll: 查找频率, 默认是1s找一次
        :return: 元素
        """
        by, value = feature
        wait = WebDriverWait(self.driver, timeout, poll)
        return wait.until(lambda x: x.find_element(by, value))

    def find_els(self, feature, timeout=10, poll=1):
        """
        找一组元素
        :param feature: 元素特征
        :param timeout: 超时时间, 默认是10s
        :param poll: 查找频率, 默认是1s找一次
        :return: 元素列表
        """
        by, value = feature
        wait = WebDriverWait(self.driver, timeout, poll)
        return wait.until(lambda x: x.find_elements(by, value))
```

> 思考:
>
> 抽取了定位元素和元素等待, 可否抽取元素常用操作到 base_action.py 中



### 137 PO-2-封装过程-6-优化base_action-2-抽取常用元素操作

base_action.py

```
from selenium.webdriver.support.wait import WebDriverWait


class BaseAction:

    def __init__(self, driver):
        self.driver = driver

    def find_el(self, feature, timeout=10, poll=1):
        """
        找一个元素
        :param feature: 元素特征
        :param timeout: 超时时间, 默认是10s
        :param poll: 查找频率, 默认是1s找一次
        :return: 元素
        """
        by, value = feature
        wait = WebDriverWait(self.driver, timeout, poll)
        return wait.until(lambda x: x.find_element(by, value))

    def find_els(self, feature, timeout=10, poll=1):
        """
        找一组元素
        :param feature: 元素特征
        :param timeout: 超时时间, 默认是10s
        :param poll: 查找频率, 默认是1s找一次
        :return: 元素列表
        """
        by, value = feature
        wait = WebDriverWait(self.driver, timeout, poll)
        return wait.until(lambda x: x.find_elements(by, value))

    def click(self, feature):
        self.find_el(feature).click()

    def input(self, feature, content):
        self.find_el(feature).send_keys(content)

    def clear(self, feature):
        self.find_el(feature).clear()

```

display_page.py

```
from selenium.webdriver.common.by import By

from V6_优化base_action.base.base_action import BaseAction


class DisplayPage(BaseAction):

    display_button = By.XPATH, "//*[@text='显示']"

    search_buttion = By.XPATH, "//*[@content-desc='搜索']"

    input_button = By.ID, "android:id/search_src_text"

    back_button = By.CLASS_NAME, "android.widget.ImageButton"

    # 点击 显示
    def click_display(self):
        self.click(self.display_button)
        # self.find_el(self.display_button).click()

    # 点击 搜索(放大镜)
    def click_search(self):
        self.click(self.search_buttion)
        # self.find_el(self.search_buttion).click()

    # 输入 hello
    def input_search(self, content):
        self.input(self.input_button, content)
        # self.find_el(self.input_button).send_keys("hello")

    # 点击 返回
    def click_back(self):
        self.click(self.back_button)
        # self.find_el(self.back_button).click()

```

more_page.py

```
from selenium.webdriver.common.by import By

from V6_优化base_action.base.base_action import BaseAction


class MorePage(BaseAction):

    more_button = By.XPATH, "//*[@text='更多']"

    mobile_network_button = By.XPATH, "//*[@text='移动网络']"

    first_network_button = By.XPATH, "//*[@text='首选网络类型']"

    network_2g_button = By.XPATH, "//*[@text='2G']"

    network_3g_button = By.XPATH, "//*[@text='3G']"

    # 点击 更多
    def click_more(self):
        self.click(self.more_button)
        # self.find_el(self.more_button).click()

    # 点击 移动网络
    def click_mobile_network(self):
        self.click(self.mobile_network_button)
        # self.find_el(self.mobile_network_button).click()

    # 点击 首选网络类型
    def click_first_network(self):
        self.click(self.first_network_button)
        # self.find_el(self.first_network_button).click()

    # 点击 2G
    def click_2g(self):
        self.click(self.network_2g_button)
        # self.find_el(self.network_2g_button).click()

    # 点击 3G
    def click_3g(self):
        self.click(self.network_3g_button)
        # self.find_el(self.network_3g_button).click()

```

test_display.py 核心代码

```
        # 输入 hello
        self.display_page.input_search("hello")
```

> 思考:
>
> 现在的框架是PO模式吗?



### 138 PO-2-封装过程-7-按page页面划分-1-总体介绍

**需求**

让特征和动作, 在对应的page中

需要新建大量的page页面, 在手动点击过程中, 遇到多少个页面, 就应该有多少page文件

**步骤**

1. 观察测试脚本跳转了多少个页面

2. 设置 点击 更多 -> 更多 点击 移动网络 -> 移动网络 点击 首选网络类型 -> 首选网络类型 点击 2g或3g

3. 新建对应的page
4. 元素的特征和动作, 在哪个页面就写在哪个对应的文件中

**目录**

```
- base
- - base_driver.py
- - base_action.py
- page
- - display_page.py
- - more_page.py
- - setting_page.py
- - search_page.py
- - mobile_network_page.py
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```



### 139 PO-2-封装过程-7-按page页面划分-2-编辑page页面

setting_page.py

```
from selenium.webdriver.common.by import By

from V7_按照page页面进行划分.base.base_action import BaseAction


class SettingPage(BaseAction):

    # 显示 按钮
    display_button = By.XPATH, "//*[@text='显示']"

    # 更多 按钮
    more_button = By.XPATH, "//*[@text='更多']"

    # 点击 显示
    def click_display(self):
        self.click(self.display_button)

    # 点击 更多
    def click_more(self):
        self.click(self.more_button)

```

display_page.py

```
from selenium.webdriver.common.by import By

from V7_按照page页面进行划分.base.base_action import BaseAction


class DisplayPage(BaseAction):

    # 放大镜 按钮
    search_buttion = By.XPATH, "//*[@content-desc='搜索']"

    # 点击 搜索(放大镜)
    def click_search(self):
        self.click(self.search_buttion)


```

search_page.py

```
from selenium.webdriver.common.by import By

from V7_按照page页面进行划分.base.base_action import BaseAction


class SearchPage(BaseAction):

    # 输入框
    input_button = By.ID, "android:id/search_src_text"

    # 返回 按钮
    back_button = By.CLASS_NAME, "android.widget.ImageButton"

    # 输入 hello
    def input_search(self, content):
        self.input(self.input_button, content)

    # 点击 返回
    def click_back(self):
        self.click(self.back_button)
```

more_page.py

```
from selenium.webdriver.common.by import By

from V7_按照page页面进行划分.base.base_action import BaseAction


class MorePage(BaseAction):

    # 移动网络 按钮
    mobile_network_button = By.XPATH, "//*[@text='移动网络']"

    # 点击 移动网络
    def click_mobile_network(self):
        self.click(self.mobile_network_button)

```

mobile_network_page.py

```
from selenium.webdriver.common.by import By

from V7_按照page页面进行划分.base.base_action import BaseAction


class MobileNetworkPage(BaseAction):

    # 首选网络类型 按钮
    first_network_button = By.XPATH, "//*[@text='首选网络类型']"

    # 2g 按钮
    network_2g_button = By.XPATH, "//*[@text='2G']"

    # 3g 按钮
    network_3g_button = By.XPATH, "//*[@text='3G']"

    # 点击 首选网络类型
    def click_first_network(self):
        self.click(self.first_network_button)

    # 点击 2G
    def click_2g(self):
        self.click(self.network_2g_button)

    # 点击 3G
    def click_3g(self):
        self.click(self.network_3g_button)
```



### 140 PO-2-封装过程-7-按page页面划分-3-调用

test_display.py

```
import time

from V7_按照page页面进行划分.base.base_driver import init_driver
from V7_按照page页面进行划分.page.display_page import DisplayPage
from V7_按照page页面进行划分.page.search_page import SearchPage
from V7_按照page页面进行划分.page.setting_page import SettingPage


class TestDisplay:

    def setup(self):
        self.driver = init_driver()
        self.setting_page = SettingPage(self.driver)
        self.display_page = DisplayPage(self.driver)
        self.search_page = SearchPage(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_display_search(self):
        # 点击 显示
        self.setting_page.click_display()
        # 点击 搜索(放大镜)
        self.display_page.click_search()
        # 输入 hello
        self.search_page.input_search("hello")
        # 点击 返回
        self.search_page.click_back()


```

test_more.py

```
import time

from V7_按照page页面进行划分.base.base_driver import init_driver
from V7_按照page页面进行划分.page.mobile_network_page import MobileNetworkPage
from V7_按照page页面进行划分.page.more_page import MorePage
from V7_按照page页面进行划分.page.setting_page import SettingPage


class TestMore:

    def setup(self):
        self.driver = init_driver()
        self.setting_page = SettingPage(self.driver)
        self.more_page = MorePage(self.driver)
        self.mobile_network_page = MobileNetworkPage(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.setting_page.click_more()
        # 点击 移动网络
        self.more_page.click_mobile_network()
        # 点击 首选网络类型
        self.mobile_network_page.click_first_network()
        # 点击 2G
        self.mobile_network_page.click_2g()

    def test_more_3g(self):
        # 点击 更多
        self.setting_page.click_more()
        # 点击 移动网络
        self.more_page.click_mobile_network()
        # 点击 首选网络类型
        self.mobile_network_page.click_first_network()
        # 点击 3G
        self.mobile_network_page.click_3g()

```

> 思考:
>
> 创建页面对象时, 涉及多少个页面就要创建多个对象, 有没有优化的办法?



### 141 PO-2-封装过程-8-page统一入口-1-总体介绍

**需求**

方便测试脚本调用页面, 不需要每次都在 setup 中创建page对象

**步骤**

1. 在 page 包中, 新建一个 page.py 文件, 包含一个 Page 类
2. 有多少个页面, 就写多少个方法
3. 每一个方法都去创建对应的 page 对象
4. 在测试脚本中创建入口Page对象, 再通过对象去调用里面的具体的方法来生成页面对象, 再调用动作

**目录**

```
- base
- - base_driver.py
- - base_action.py
- page
- - page.py
- - display_page.py
- - more_page.py
- - setting_page.py
- - search_page.py
- - mobile_network_page.py
- scripts
- - test_more.py
- - test_display.py
- pytest.ini
```



### 142 PO-2-封装过程-8-page统一入口-2-编写代码

page.py

```
from V8_page统一入口.page.display_page import DisplayPage
from V8_page统一入口.page.mobile_network_page import MobileNetworkPage
from V8_page统一入口.page.more_page import MorePage
from V8_page统一入口.page.search_page import SearchPage
from V8_page统一入口.page.setting_page import SettingPage


class Page:

    def __init__(self, driver):
        self.driver = driver

    @property
    def setting(self):
        return SettingPage(self.driver)

    @property
    def display(self):
        return DisplayPage(self.driver)

    @property
    def search(self):
        return SearchPage(self.driver)

    @property
    def more(self):
        return MorePage(self.driver)

    @property
    def mobile_network(self):
        return MobileNetworkPage(self.driver)

```

test_display.py

```
import time
from V8_page统一入口.base.base_driver import init_driver
from V8_page统一入口.page.page import Page


class TestDisplay:

    def setup(self):
        self.driver = init_driver()
        self.page = Page(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_display_search(self):
        # 点击 显示
        self.page.setting.click_display()
        # 点击 搜索(放大镜)
        self.page.display.click_search()
        # 输入 hello
        self.page.search.input_search("hello")
        # 点击 返回
        self.page.search.click_back()

```

test_more.py

```
import time
from V8_page统一入口.base.base_driver import init_driver
from V8_page统一入口.page.page import Page


class TestMore:

    def setup(self):
        self.driver = init_driver()
        self.page = Page(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    def test_more_2g(self):
        # 点击 更多
        self.page.setting.click_more()
        # 点击 移动网络
        self.page.more.click_mobile_network()
        # 点击 首选网络类型
        self.page.mobile_network.click_first_network()
        # 点击 2G
        self.page.mobile_network.click_2g()

    def test_more_3g(self):
        # 点击 更多
        self.page.setting.click_more()
        # 点击 移动网络
        self.page.more.click_mobile_network()
        # 点击 首选网络类型
        self.page.mobile_network.click_first_network()
        # 点击 3G
        self.page.mobile_network.click_3g()

```



### 143 PO-3-总结

**工作中的步骤**

1. 把之前的 base 和 ini 复制到新项目中
2. 创建 page 和 scripts
3. 先写page, 测试的过程需要用到多少个页面, 就在page包中创建多少个文件
4. 在对应的page文件中, 写元素特征和对应这个特征的动作
5. 记得: page需要继承 BaseAction
6. page统一入口, 有多少个页面, 就写多少个函数, 函数的功能是用于创建页面对象
7. 回到test脚本, setup中连接手机并获取driver对象, 创建page入口对象, 并且传入刚刚获取的driver
8. 在test函数中, 调用不同页面的不同的动作

**模块在项目中的角色**

scripts 注重 操作的先后顺序 测试数据

page 注重 UI 动作

base_action 动作 (所有的page或者其他的项目可能用到的公共的方法)



### 144 PO-4-综合案例

**需求** 

在《通讯录》应用中，进入添加联系人页面，在姓名和电话栏中，输入对应的数据。 

> 包名界面名：com.android.contacts/.activities.PeopleActivity 
>
> 添加联系人按钮：resource-id，com.android.contacts:id/floating_action_button 
>
> 姓名输入框：text，姓名 
>
> 电话输入框：text，电话 
>
> 因为appium每次启动应用时都会"重置应用"，才会出现本地保存，若不想重置，可直接在启动参数加一行代码 
>
> desired_caps['noReset'] = True 即可 

**数据** 

[zhangsan, 18888888888] 

[lisi, 13333333333] 

[wangwu, 17777777777]

**要求** 

使用 pytest框架 + PO模式 + 数据参数化

























