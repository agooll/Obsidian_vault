### 146 扩展-1-yaml-1-总体介绍

**概念**

```
yaml 和 json 一样, 是一种数据格式
yaml 是一种所有编程语言可用的友好的数据序列化标准. 在 python 中, 可以表达字典/列表/基本数据类型
```

**应用场景**

```
1. 通用场景, 用于数据序列化
2. 在自动化测试中, 用于数据驱动
	数据驱动指的就是测试数据的参数化, 且测试数据和代码分离
```

**[扩展]序列化和反序列化**

```
背景
	计算机硬件中, 和数据存储有关的硬件
		内存
		硬盘
	其中, 内存的读写速度要比硬盘快得多
		内存用于做临时计算
		硬盘用于持久化保存计算结果
概念
	序列化
		将内存中的对象 (编程语言可以识别的数据类型) 写入到硬盘的过程, 即文件写操作
	反序列化
		将硬盘中的数据 (恢复为可运行的数据格式) 读取到内存中的过程, 即文件读操作
```



### 148 扩展-1-yaml-2-快速体验

```
语法规则
	大小写敏感
	使用缩进表示层级关系
	缩进时不允许使用Tab键, 只允许使用空格
	缩进的空格数据不重要, 只要相同层级的元素左对齐即可
需求
	读 yaml 格式的文件
		name: "xiaoming"
		age: "18"
```

**代码**

```
# 如果没有 yaml 这个包, 使用 pip install pyyaml 去安装即可
import yaml

# with open("./data.yaml", "r", encoding="utf-8") as f:
#     data = yaml.load(f)
#     print(data)

# yaml.load 方法在 yaml 5.1 以上的版本中, 不安全, 不推荐使用, 应该用 yaml.full_load
with open("./data.yaml", "r", encoding="utf-8") as f:
    data = yaml.full_load(f)
    print(data)

with open("./data.yml", "r", encoding="utf-8") as f:
    data = yaml.full_load(f)
    print(data)

```

> 注意点:
>
> 1. 导包问题, 如果没有 yaml 包, 可以通过 pip install pyyaml 进行安装
> 2. 出去安全考虑, 使用 full_load 替换 load
> 3. 文件后缀问题  yaml 和 yml 格式 都可以



### 149 扩展-1-yaml-3-数据表示-1-字典和列表



### 150 扩展-1-yaml-3-数据表示-2-字典和列表相互嵌套



### 152 扩展-1-yaml-3-数据表示-3-练习

**需求**

使用 yaml 编写

["1", "2", {"name": ["xiaoming", "xiaohong"], "age": "18"}, [{"name": "xiaoqiang", "age": "28"}, "3", "4"], "5", ["7", "8"]]

```
- "1"
- "2"
- 
  name: 
    - "xiaoming"
    - "xiaohong"
  age: "18"
- 
  - 
    name: "xiaoqiang"
    age: "28"
  - "3"
  - "4"
- "5"
- 
  - "7"
  - "8"
```



### 153 扩展-1-yaml-3-数据表示-4-基本数据类型



### 154 扩展-1-yaml-3-在python中的读写-1-读yaml文件

```
# 导包
import yaml

# 打开要读取的文件
with open("./data.yaml", "r", encoding="utf-8") as f:
    # 加载文件内容
    data = yaml.full_load(f)
    # 打印结果
    print(data)
```



### 155 扩展-1-yaml-3-在python中的读写-2-写yaml文件

**数据**

{'search_data': {'search_test_001': {'expect': {'value': '你好'}, 'value': 'hello'}}}

```
import yaml


# 准备要写入的数据
data = {'search_data': {'search_test_001': {'expect': {'value': '你好'}, 'value': 'hello'}}}

# 将数据写入
with open("./dump.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True)

# 注意, 写入中文内容到 yaml 中, 需要在 dump 方法中指定参数 allow_unicode=True
```



### 156 扩展-1-yaml-4-数据驱动-1-项目准备



### 157 扩展-1-yaml-4-数据驱动-2-yaml数据和脚本的对应关系

**思考**

- 一个项目有多个 “模块”
- 一个模块有多个 “测试脚本”

> 那么读取yaml数据时, 就需要知道, 读的是属于哪个模块, 哪个脚本的数据

**举例**

> 测试用例如下

| 用例编号                  | 用例模块 | 用例名称       | 测试数据              |
| ------------------------- | -------- | -------------- | --------------------- |
| test_login_001            | 登录     | 张三登录       | zhangsan, zhangsan123 |
| test_login_002            | 登录     | 李四登录       | lisi, lisi123         |
| test_login_003            | 登录     | 王五登录       | wangwu, wangwu123     |
| test_username_sign_up_001 | 注册     | 张三用户名注册 | zhangsan, zhangsan321 |
| test_username_sign_up_002 | 注册     | 李四用户名注册 | lisi, lisi321         |
| test_phone_sign_up_001    | 注册     | 小明手机号注册 | 13333333333, 123000   |
| test_phone_sign_up_002    | 注册     | 小红手机号注册 | 18888888888, 321000   |

yaml数据如下:

login_data.yaml

```
test_login:
	test_login_001:
		username: "zhangsan"
		password: "zhangsan123"
	test_login_002:
		username: "lisi"
		password: "lisi123"
	test_login_003:
		username: "wangwu"
		password: "wangwu123"
```

sign_up_data.yaml

```
test_username_sign_up:
	test_username_sign_up_001:
		username: "zhangsan"
		password: "zhangsan321"
	test_username_sign_up_002:
		username: "lisi"
		password: "lisi321"
test_phone_sign_up:
	test_phone_sign_up_001:
		username: "13333333333"
		password: "123000"
	test_phone_sign_up_002:
		username: "18888888888"
		password: "321000"
```

**小结**

- 一个 yaml 数据文件 对应 一个模块
  - sign_up_data.yaml 对应 注册 模块
- 数据内容中最外层 key 对应 一个模块下的脚本名
  - test_username_sign_up 对应 函数 test_username_sign_up
  - test_phone_sign_up 对应 函数 test_phone_sign_up
- 数据内容中第二层的 key 对应 用例编号
  - test_username_sign_up_001 对应 编号 test_username_sign_up_001
  - test_username_sign_up_002 对应 编号 test_username_sign_up_002
- 数据内容中最里层的 key 对应 用例的具体测试数据
  - username 对应 用户名
  - password 对应 密码



### 159 扩展-1-yaml-4-数据驱动-3-yaml数据编写



### 160 扩展-1-yaml-4-数据驱动-4-yaml数据解析

**代码**

test_contact.py

```
import time
import pytest
import yaml
from VV_综合案例_数据驱动.base.base_driver import init_driver
from VV_综合案例_数据驱动.page.page import Page

def analyze_file():
    with open("./data/contact_data.yaml", "r", encoding="utf-8") as f:
        data = yaml.full_load(f)
        dict_data = data["test_contact"]
        list_data = list()
        for i in dict_data.values():
            list_data.append(i)
        return list_data

class TestContact:

    # def setup(self):
    #     self.driver = init_driver()
    #     self.page = Page(self.driver)
    #
    # def teardown(self):
    #     time.sleep(3)
    #     self.driver.quit()

# [{"name": "zhangsan", "phone": "18888888888"}, {"name": "lisi", "phone": "13333333333"},{"name": "wangwu", "phone": "17777777777"}]

    @pytest.mark.parametrize("args", analyze_file())
    def test_contact(self, args):
        print(args["name"])
        print(args["phone"])

        # # 点击 添加联系人
        # self.page.contact_list.click_add_contact()
        # # 输入 姓名
        # self.page.new_contact.input_name(args["name"])
        # # 输入 电话
        # self.page.new_contact.input_phone(args["phone"])

```



### 161 扩展-1-yaml-4-数据驱动-5-调整测试脚本

**代码**

base/base_analyze.py

```
import yaml


def analyze_file(filename, key):
    with open("./data/" + filename, "r", encoding="utf-8") as f:
        data = yaml.full_load(f)
        dict_data = data[key]
        list_data = list()
        for i in dict_data.values():
            list_data.append(i)
        return list_data
```

test_contact.py

```
import time
import pytest

from VV_综合案例_数据驱动.base.base_analyze import analyze_file
from VV_综合案例_数据驱动.base.base_driver import init_driver
from VV_综合案例_数据驱动.page.page import Page


class TestContact:

    # def setup(self):
    #     self.driver = init_driver()
    #     self.page = Page(self.driver)
    #
    # def teardown(self):
    #     time.sleep(3)
    #     self.driver.quit()

# [{"name": "zhangsan", "phone": "18888888888"}, {"name": "lisi", "phone": "13333333333"},{"name": "wangwu", "phone": "17777777777"}]

    @pytest.mark.parametrize("args", analyze_file("contact_data.yaml", "test_contact"))
    def test_contact(self, args):
        print(args["name"])
        print(args["phone"])

        # # 点击 添加联系人
        # self.page.contact_list.click_add_contact()
        # # 输入 姓名
        # self.page.new_contact.input_name(args["name"])
        # # 输入 电话
        # self.page.new_contact.input_phone(args["phone"])

```



### 162 扩展-1-yaml-4-数据驱动-6-增加断言

**核心代码**

base_action.py

```
    def click_back(self):
        self.driver.press_keycode(4)
```

page/saved_contact_page.py

```
from selenium.webdriver.common.by import By
from VV_综合案例_数据驱动.base.base_action import BaseAction


class SavedContactPage(BaseAction):

    title = By.ID, "com.android.contacts:id/large_title"

    def get_title(self):
        return self.find_el(self.title).text
```

page/page.py

```
    @property
    def saved_contact(self):
        return SavedContactPage(self.driver)
```

scripts/test_contact.py

```
    @pytest.mark.parametrize("args", analyze_file("contact_data.yaml", "test_contact"))
    def test_contact(self, args):
        # 点击 添加联系人
        self.page.contact_list.click_add_contact()
        # 输入 姓名
        self.page.new_contact.input_name(args["name"])
        # 输入 电话
        self.page.new_contact.input_phone(args["phone"])
        # 按 返回 按钮
        self.page.saved_contact.click_back()
        # 断言
        # print(self.page.saved_contact.get_title())
        assert self.page.saved_contact.get_title() == args["name"]
```



### 163 扩展-2-allure-1-总体介绍

```
allure是一个独立的报告插件, 生成美观易读的报告,  目前支持 java, python, ruby, php, C#等
帮助文档
步骤
	最终我们会生成一个 html 格式的报告, 中间需要操作两步
	1. 生成 xml
		前提: 安装
			pip install pytest-allure-adaptor
	2. 将 xml 转成 html
		前提: 安装
			1. 下载 allure-2.6.0.zip
			2. 解压缩到一个目录
			3. 将解压目录下的 bin 目录配置到环境变量 path 中
			4. 在命令行输入 allure 命令, 如果提示是有这个命令, 说明成功
```



### 164 扩展-2-allure-2-基本使用

```
生成 xml 步骤
	1. 将 pytest.ini 中的命令行参数加上  --alluredir report
	2. 正常运行 pytest 即可
	3. 程序运行结束后, 会在对应的 report 目录下生成一个 xml 文件
生成 html 步骤
	1. 进入report 上级目录, 执行命令
		allure generate report/ -o report/html --clean
	2. report 目录下会生成 html 文件夹, 文件夹下会有一个 index.html , 用浏览器打开即可
```



### 165 扩展-2-allure-3-参数和命令详解

- addopts = -s --alluredir report 中的 --alluredir report 是什么意思?
  - --alluredir 后面的 report 为 xml 输出的目录名
  - 如果希望目录名叫 result 那么可以将命令行参数改为 --allure result

- allure generate report/ -o report/html --clean 是什么意思?
  - report/ 表示 xml 所在的目录
  - -o 表示output 输出
  - report/html 表示将 index.html 报告生成到哪个文件夹
  - --clean 表示清除缓存内容



### 166 扩展-2-allure-4-与pytest结合-1-项目准备

```
项目准备
	使用 PO 模式 + pytest 框架来制作程序, 实现"设置"应用中, 搜索 "hello1" 和 "xiaoming"
	项目的实现过程不作为重点, 能理解即可
```

**代码**

page/setting_page.py

```
from selenium.webdriver.common.by import By

from base.base_action import BaseAction


class SettingPage(BaseAction):

    # 放大镜 按钮
    search_buttion = By.XPATH, "//*[@content-desc='搜索']"

    # 点击 搜索(放大镜)
    def click_search(self):
        self.click(self.search_buttion)

```

page/search_page.py

```
from selenium.webdriver.common.by import By

from base.base_action import BaseAction


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

page/page.py

```
from page.search_page import SearchPage
from page.setting_page import SettingPage


class Page:

    def __init__(self, driver):
        self.driver = driver

    @property
    def setting(self):
        return SettingPage(self.driver)

    @property
    def search(self):
        return SearchPage(self.driver)


```

scripts/test_search.py

```
import time
import pytest
from base.base_driver import init_driver
from page.page import Page


class TestSearch:

    def setup(self):
        self.driver = init_driver()
        self.page = Page(self.driver)

    def teardown(self):
        time.sleep(3)
        self.driver.quit()

    @pytest.mark.parametrize("args", ["hello1", "xiaoming"])
    def test_search(self, args):
        # 点击 搜索(放大镜)
        self.page.setting.click_search()
        # 输入 内容
        self.page.search.input_search(args)
        # 点击 返回
        self.page.search.click_back()
```



### 167 扩展-2-allure-4-与pytest结合-2-添加测试步骤

**使用方式**

在 page 中的所有方法上加上 @allure.step(title="测试步骤001")

**核心代码**

page/setting_page.py

```
    # 点击 搜索(放大镜)
    @allure.step(title='点击放大镜')
    def click_search(self):
        self.click(self.search_buttion)
```

page/search_page.py

```
    # 输入 内容
    @allure.step(title='输入文字')
    def input_search(self, content):
        self.input(self.input_button, content)

    # 点击 返回
    @allure.step(title='点击返回')
    def click_back(self):
        self.click(self.back_button)
```



### 168 扩展-2-allure-4-与pytest结合-3-添加测试描述

**核心代码**

```
    # 输入 内容
    @allure.step(title='输入文字')
    def input_search(self, content):
        allure.attach('描述(输入的内容)', content, allure.attach_type.TEXT)
        self.input(self.input_button, content)
        allure.attach('这是一张截图', self.driver.get_screenshot_as_png(), allure.attach_type.PNG)
```



### 169 扩展-2-allure-4-与pytest结合-4-添加优先级

**使用方式**

在测试脚本中, 增加装饰器 @allure.severity(优先级)

> - blocker 阻塞性的
> - critical  关键的
> - normal  普通的(默认的)
> - minor   次要的
> - trivial   不重要的

**核心代码**

scripts/test_search.py

```
    @allure.severity('blocker')
    @pytest.mark.parametrize("args", ["hello1", "xiaoming"])
    def test_search(self, args):
        # 点击 搜索(放大镜)
        self.page.setting.click_search()
        # 输入 内容
        self.page.search.input_search(args)
        # 点击 返回
        self.page.search.click_back()
```



### 170 扩展-3-toast-1-总体介绍

```
概念
	toast 是 android 系统中的一种消息框类型
应用场景
	获取 toast 内容, 用于验证交互逻辑
快速体验
	需求
		打开"文件管理器", 点击 "返回" 按钮, 获取toast 提示内容
```

**快速体验代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
# 打开<文件管理器>
desired_caps["appPackage"] = "com.cyanogenmod.filemanager"
desired_caps["appActivity"] = ".activities.NavigationActivity"
# 使用 uiautomator2 框架
desired_caps["automationName"] = "Uiautomator2"
# 不重置应用
desired_caps["noReset"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

driver.press_keycode(4)
print(driver.find_element_by_xpath("//*[@text='再次点击即可退出.']").text)

time.sleep(2)
driver.quit()
```

> 注意点:
>
> 1. 只有 android 4.0 以上的版本才支持
> 2. 只有 Uiautomator2 才能支持



### 171 扩展-3-toast-2-环境安装

**安装**

```
1. 安装 node.js
2. 安装 cnpm
3. 安装 appium-uiautomator2-driver
```

1. 安装 node.js

   ```
   使用 node-v10.16.0-x64.msi 进行安装
   ```

2. 安装 cnpm

   ```
   npm install -g cnpm --registry=https://registry.npm.taobao.org
   ```

3. 安装 appium-uiautomator2-driver

   ```
   cnpm install appium-uiautomator2-driver
   ```

   > 安装完成后, 会提示 All packaeges installed, 说明安装成功了,
   >
   > 如果安装不成功, 就重新执行上面的命令
   >
   > 如果还是安装不成功, 需要清除缓存, 再执行上面的命令
   >
   > ```
   > # 清除 npm 缓存
   > npm cache clean --force
   > npm cache verify
   > npm config set strict-ssl false
   > # 清除 cnpm 缓存
   > cnpm cache clean --force
   > cnpm cache verify
   > cnpm config set strict-ssl false
   > ```



### 172 扩展-3-toast-3-获取toast内容

**步骤**

1. 在前置代码添加

   ```
   desired_caps["automationName"] = "Uiautomator2"
   ```

2. 使用 xpath 找 消息框的 text 即可

   ```
   # 封装 获取 toast 内容的方法
   def find_toast(msg):
       """
       根据部分 toast 信息获取全部 toast 信息
       :param msg: 预期要获取的toast的部分内容
       :return: 全部toast内容
       """
       wait = WebDriverWait(driver, 5, 0.2)
       el = wait.until(lambda x: x.find_element_by_xpath("//*[contains(@text, '%s')]" % msg))
       return el.text
   # 应该把 find_toast 方法, 放到大家自动化框架中的 base_action.py 里面
   # 因为每个页面都继承了 BaseAction 类, 那么就可以使用 find_toast 方法了
   ```

   

### 173 扩展-3-WebView-1-总体介绍

**概念**

webview 是一个基于webkit引擎, 展示html页面控件

它和浏览器展示页面的原理是相同的, 所以可以把它当做浏览器看待

> 说明:
>
> chrome浏览器就是基于webkit引擎开发的, firefox浏览器是基于gecko引擎开发的
>
> 不管是ios还是android, 自带浏览器底层都是基于webkit的, 各自系统中斗带有webview控件, 也是基于webkit引擎, 所以不管通过app调用webview展示html页面还是通过浏览器打开html页面, 效果是一样的

**优缺点**

优点:

1. 由于是运行在浏览器上, 只需要开发一次便可以在不同的操作系统上显示
2. 迭代版本时, 不需要打包便可以发布

缺点:

1. 每次打开页面, 都得重新加载, 获取数据
2. 过于依赖网络, 速度无法保证
3. 无法使用摄像头, 重力/方向传感器, 拨号, GPS, 语音, 短信, 蓝牙等功能



### 174 扩展-3-WebView-2-查看webview元素的方式

```
1. UIAutomatorviewer 查看
	一般行不通, 万一能查看到元素, 那是人品很好
2. 通过chrome直连手机查看
	1. 确保 adb devices 可以发现设备
	2. 移动端打开要查看的webview页面
	3. 在 chrome 中输入 chrome://inpect 地址, 并点击 inspect
	4. 选中要查看的元素即可
3. [推荐]通过 chrome 浏览器查看手机的页面地址
	1. 确保 adb devices 可以发现设备
	2. 移动端打开要查看的webview页面
	3. 复制移动端的地址, 在 chrome 中打开
	4. 选中要查看的元素即可
```



### 175 扩展-3-WebView-3-实现webview自动化

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
# 打开<浏览器>
desired_caps["appPackage"] = "com.android.browser"
desired_caps["appActivity"] = ".BrowserActivity"
# 不重置应用
desired_caps["noReset"] = True
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
driver.implicitly_wait(10)

# 在浏览器中打开百度首页, 并在搜索框输入10086, 再打开知乎

# 打开百度首页
driver.find_element_by_id("com.android.browser:id/url").send_keys("www.baidu.com")
time.sleep(2)
driver.press_keycode(66)    # keycode 66 表示回车
print(driver.contexts)  # 打印上下文环境

# 切换到网页环境
driver.switch_to.context("WEBVIEW_com.android.browser")
# 定位百度输入框, 输入10086
driver.find_element_by_id("word").send_keys("10086")

# 切换到原生环境
driver.switch_to.context("NATIVE_APP")
# 打开知乎
driver.find_element_by_id("com.android.browser:id/url").send_keys("www.zhihu.com")
time.sleep(2)
driver.press_keycode(66)    # keycode 66 表示回车

time.sleep(2)
driver.quit()

```



### 176 扩展-3-WebView-4-chromedriver问题

```
1. 下载对应的 chromedriver
2. 启动appium 时加载 chromedriver
```



### 177 扩展-4-Monkey-1-总体介绍

```
monkey是什么
	monkey 就是猴子, monkey 测试, 就像一只猴子在设备上乱敲乱点
monkey用来做什么
	monkey 主要用于android的压力/稳定性测试, 目的就是为了测试 app 是否会崩溃 (crash)
```

**monkey程序介绍**

- monkey程序是android系统自带的, 使用 java写的, 在android文件系统中的存放路径:

  /system/framework/monkey.jar

- monkey.jar程序是由一个名为"monkey"的shell脚本来启动执行的, shell脚本在android文件系统中的存放路径

  /system/bin/monkey

- monkey命令启动方式
  - [推荐]通过pc的cmd窗口执行: adb shell monkey +命令参数 来进行monkey测试
  - 在pc上adb shell 进入android系统, 执行 monkey +命令参数 来进行monkey测试
  - 在android真机或者模拟器上执行monkey, 可以安装终端模拟器 (Terminal Emulator for Android)

**monkey输出**

```
adb shell monkey -p cn.goapk.market 100 > 路径/log.txt
```



### 178 扩展-4-Monkey-2-命令参数

- 启动指定app

  > -p 包名
  >
  > 指定一个包: adb shell monkey -p cn.goapk.market 100
  >
  > 指定多个包: adb shell monkey -p 包名1 -p 包名2 100

- 日志级别

  > -v 
  >
  > Level 0: adb shell monkey -p cn.goapk.market -v 100  
  >
  > ​	(默认值, 仅提供启动提示, 测试完成, 最终结果等少量信息)
  >
  > [推荐]Level1: adb shell monkey -p cn.goapk.market -v -v 100 
  >
  > ​	(提供较为详细的日志, 包括每个发送的事件)
  >
  > Level 2: adb shell monkey -p cn.goapk.market -v -v -v 100 
  >
  > ​	(最详细的日志, 包括了测试中选中/未选中的activity信息)

- 随机数种子

  > -s
  >
  > 用于指定seed值, 如果seed相同, 则两次 monkey 测试所产生的事件序列也相同
  >
  > 示例1:
  >
  > 测试1: adb shell monkey -p cn.goapk.market -s 10086 100
  >
  > 测试2: adb shell monkey -p cn.goapk.market -s 10086 100

- 事件时间间隔

  > --throttle
  >
  > adb shell monkey -p cn.goapk.market --throttle 2000 10

- 随机事件百分比

  > --pct-xxx
  >
  > ```
  > --pct-touch <percent> 
  > 调整触摸事件的百分比(触摸事件是一个down-up事件，它发生在屏幕上的某单一位置)
  > 
  > --pct-motion <percent> 
  > 调整动作事件的百分比(动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
  > 
  > --pct-pinchzoom <percent> 
  > 缩放事件百分比
  > 
  > --pct-trackball <percent> 
  > 调整轨迹事件的百分比(轨迹事件由一个或几个随机的移动组成，有时还伴随有点击)
  > 
  > --pct-rotation <percent> 
  > 屏幕旋转事件百分比
  > 
  > --pct-nav <percent>
  > 调整“基本”导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
  > 
  > --pct-majornav <percent> 
  > 调整“主要”导航事件的百分比(这些导航事件通常引发图形界面中的动作，如：回退按键、菜单按键) 
  > 
  > --pct-syskeys <percent> 
  > 调整“系统”按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)
  > 
  > --pct-appswitch <percent> 
  > 调整启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
  > 
  > --pct-flip <percent> 
  > 键盘翻转事件百分比
  > 
  > --pct-anyevent <percent> 
  > 调整其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等
  > ```



### 181 扩展-4-Monkey-3-日志分析

```
正常情况
	如果 monkey 测试顺利执行完成, 在log最后, 会打印出当前执行事件的次数和所花费的时间
异常情况
	monkey测试出现错误, 应该好好分析
		1. 崩溃问题: 在日志中搜索 "Exception"
		2. 程序无响应问题: 在日志中搜索 "ANR"
			可能仅仅是因为程序卡顿
```

[面试时]有没有什么印象比较深的bug?



































