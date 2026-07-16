### 56 appium-api-1-appium基础操作API-1-总体介绍

**内容**

```
使用 appium 在脚本内启动其他的 app
使用 appium 获取包名和界面名
使用 appium 关闭 app 和驱动对象
使用 appium 安装卸载 app 以及判断app是否已安装
使用 appium 将应用置于后台
```

**前置代码**

```
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

driver.quit()
```



### 57 appium-api-1-appium基础操作API-2-在脚本内启动其他app

```
应用场景
	1. 需要启动另一个app时
	2. 需要模拟中断的状态时 (交叉事件)
命令
	driver.start_activity("要启动的程序包的包名", "要打开的页面")
示例
	需求
		在 "设置" 中打开 "浏览器"
	步骤
		1. 获取浏览器的包名和启动名  com.android.browser    .BrowserActivity
		2. 调用 start_activity 的方法, 打开浏览器应用
	代码
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

time.sleep(3)
driver.start_activity("com.android.browser", ".BrowserActivity")

time.sleep(3)
driver.quit()

```



### 58 appium-api-1-appium基础操作API-3-获取包名和界面名

```
应用场景
	用于支付场景是否跳转成功的断言
属性
	# 获取包名
driver.current_package
# 获取界面名
driver.current_activity
示例
	需求
		打开"设置", 获取包名和界面名
	步骤
		1. 打开 "设置"
		2. 调用属性去获取即可
	代码
扩展
	appium和adb都可以获取包名和界面名, 有什么区别?
	区别
		1 使用阶段不同
			adb方式, 在测试脚本执行之前使用
			appium方式, 在测试脚本开始编写之后
		2 用途不同
			通过adb方式获取, 是用于把获取结果放到前置代码中, 可以用于启动app
			通过appium方式, 用于校验
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 获取包名, 预期结果: com.android.settings
print("包名:", driver.current_package)
# 获取界面名, 预期结果: .Settings
print("界面名:", driver.current_activity)

time.sleep(3)
driver.quit()

```



### 59 appium-api-1-appium基础操作API-4-关闭app和驱动对象

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 关闭app
time.sleep(3)
print(1)
driver.close_app()

print(2)
time.sleep(3)
# 关闭驱动对象driver
driver.quit()
print(3)

# # 可否先关闭driver 再关闭app ?
# driver.quit()
# driver.close_app()
```



### 60 appium-api-1-appium基础操作API-5-安装卸载以及判断是否安装

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 关闭"设置", 取消对屏幕的遮挡
driver.close_app()

# 包名: cn.goapk.market
# 1.判断"安智市场"是否已经安装
if driver.is_app_installed("cn.goapk.market"):
# 2.如果已安装, 则卸载
    driver.remove_app("cn.goapk.market")
# 3.如果未安装, 则安装
else:
    driver.install_app("C:\\Users\\57769\\Desktop\\anzhishichang.apk")

time.sleep(3)
driver.quit()

```



### 61 appium-api-1-appium基础操作API-6-将应用置于后台

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

time.sleep(3)
driver.background_app(5)

time.sleep(3)
driver.quit()

# 补充概念
# 冷
#     电脑关机的状态下, 按开机键, 为冷启动
#     手机关机状态下, 插拔卡槽, 为冷插拔
#     手机未运行app的情况下, 点击并运行app, 为冷启动
# 热
#     电脑开机状态下, 重启电脑, 为热启动
#     手机开机状态下, 插拔卡槽, 为热插拔
#     手机的app置于后台的情况下, 让app重回前台视野, 为热启动
```



### 62 appium-api-2-UIAutomatorViewer使用

```
简介
	用来扫描和分析 Android 应用程序 UI 控件的工具
路径
	在SDK下的 tools 目录下
		uiautomatorviewer.bat
示例
	使用 UIAutomatorviewer 工具获取 "设置" 中, 放大镜图标的元素特征
	步骤
		1. adb服务和移动端已经联通
			adb devices 能查到设备
		2. 打开 ui...工具 
		3. 进入移动端的"设置"
		4. 在 ui... 工具中, 点击左上角第二个小图标
		5. 单击 ui... 工具中的界面上的放大镜图标
		6. ui... 工具右下角的 Node Detail 中就可以看到元素的特征
```



### 63 appium-api-3-元素定位API-1-总体介绍

```
什么样的元素能定位到???
	对比
		Selenium
			页面包含的元素都可以进行定位, 包括视野里没有的
		Appium
			只能定位视野里存在的元素
```



### 64 appium-api-3-元素定位API-2-定位一个元素

**方法**

```
方法
	id
		driver.find_element_by_id("元素的resource-id属性值")
# 返回值: 定位到的这个元素
	class
		driver.find_element_by_class_name("元素的class属性值")
# 返回值: 定位到的这个元素
	xpath
		driver.find_element_by_xpath("xpath表达式")
# 返回值: 定位到的这个元素
			如:
//*[@id = '元素的resource-id属性值']
//*[contains(@attribute, 'x')]
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 通过 id 的形式, 定位 "放大镜" 按钮, 并点击
time.sleep(2)
driver.find_element_by_id("com.android.settings:id/search").click()
# 通过 class 的形式, 定位 "输入框", 输入 hello
time.sleep(2)
driver.find_element_by_class_name("android.widget.EditText").send_keys("hello")
# 通过 xpath 的形式, 定位 "返回" 按钮, 并点击
time.sleep(2)
driver.find_element_by_xpath("//*[@content-desc='收起']").click()

time.sleep(3)
driver.quit()

# 如果有多个元素的特征相同, 使用 find_element_by_xxx 的方法会定位到第一个元素
# 在 html 页面中, id 属性值 是唯一的  (规范)
# 在移动端的页面中, id 属性值可以不唯一, 但是假如 id 值唯一, 推荐通过 id 去定位元素
```



### 66 appium-api-3-元素定位API-3-定位一组元素

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 通过 id 的形式, 获取所有 resource-id 为 "com.android.settings:id/title" 的元素, 并打印文字内容
# elements = driver.find_elements_by_id("com.android.settings:id/title")
# for element in elements:
#     print(element.text)

# 通过 class_name 的形式, 获取所有 class为 "android.widget.TextView" 的元素, 并打印文字内容
# eles = driver.find_elements_by_class_name("android.widget.TextView")
# for el in eles:
#     print(el.text)

# 通过 xpath 的形式, 获取所有 文本内容 包含 "设" 的元素, 并打印文字内容
elements = driver.find_elements_by_xpath("//*[contains(@text, '设')]")
for el in elements:
    print(el.text)

time.sleep(3)
driver.quit()

```



### 67 appium-api-3-元素定位API-4-定位元素的注意点

```
示例
	使用 find_element_by_xxx 或者 find_elements_by_xxx 的方法, 分别传入一个没有的 特征, 会是什么结果
	如, driver.find_element_by_id("xxx")
	driver.find_elements_by_id("xxx")
小结
	使用 find_element_by_xx 的方法, 如果定位失败, 会报 NoSuchElementException 的错误
	使用 find_elements_by_xx 的方法, 如果定位失败, 不会报错, 会返回一个空列表
```



### 68 appium-api-4-元素等待-1-总体介绍

```
概念
	定位页面元素时, 如果未找到, 在指定时间内一直等待的过程
分类
	1. 隐式等待
	2. 显式等待
应用场景
	网络速度慢
	服务器处理请求速度慢
	硬件配置原因
```



### 69 appium-api-4-元素等待-2-隐式等待

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 在 10 秒内, 在 "设置" 中查找 "返回" 按钮, 如果找到则点击, 如果找不到则观察报错信息
driver.implicitly_wait(10)
button = driver.find_element_by_xpath("//*[contains(@content-desc, '收起')]")
button.click()

time.sleep(3)
driver.quit()

# 使用隐式等待, 查找单个元素, 找不到会报错 NoSuchElementException
```



### 70 appium-api-4-元素等待-3-显式等待

**代码**

```
import time
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 在 10 秒内, 每1秒找一次, 在 "设置" 中查找 "返回" 按钮, 如果找到则点击, 如果找不到则观察报错信息
wait = WebDriverWait(driver, 10, poll_frequency=1)
button = wait.until(lambda x: x.find_element_by_xpath("//*[contains(@content-desc, '收起')]"))
button.click()

time.sleep(3)
driver.quit()

# 使用显式等待, 查找单个元素, 找不到会报错 TimeoutException
```



### 71 appium-api-4-元素等待-4-隐式等待和显式等待的选择

```
使用方法
	显示等待的方法封装在 WebDriverWait 类中, 而隐式等待则直接通过 driver 实例化对象调用
作用域
	隐式等待全局有效, 显式等待为单个元素有效
关于 sleep
	sleep 是固定死一个时间, 不是不行, 是不推荐
	元素等待可以让元素出来的第一时间进行操作, sleep 可能造成浪费
```



### 72 appium-api-5-元素操作API-1-总体介绍

```
分类
	1. 操作: 点击, 输入和清空
	2. 获取: 元素的文本内容, 位置, 大小, 根据属性名获取属性值
```



### 73 appium-api-5-元素操作API-2-点击元素

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 打开 "设置", 点击放大镜
time.sleep(2)
driver.find_element_by_id("com.android.settings:id/search").click()

time.sleep(3)
driver.quit()
```



### 74 appium-api-5-元素操作API-3-输入和清空输入框内容

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"
# 支持中文输入
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 需求
# 1.打开 "设置"
# 2.点击 "放大镜"
driver.find_element_by_xpath("//*[@content-desc='搜索']").click()
time.sleep(2)
# 3.输入 "hello"
input = driver.find_element_by_id("android:id/search_src_text")
input.send_keys("hello")
time.sleep(2)
# 4.清空输入框内容
input.clear()
time.sleep(2)
# 5.输入 "你好"
input.send_keys("你好")

time.sleep(3)
driver.quit()
```



### 75 appium-api-5-元素操作API-4-获取元素的文本内容

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"
# 支持中文输入
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 通过 id 的形式, 获取所有 resource-id 为 "com.android.settings:id/title" 的元素, 并打印文字内容
elements = driver.find_elements_by_id("com.android.settings:id/title")
for element in elements:
    print(element.text)

time.sleep(3)
driver.quit()


```



### 76 appium-api-5-元素操作API-5-获取元素的位置

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"
# 支持中文输入
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 获取 "放大镜" 的位置
element = driver.find_element_by_xpath("//*[@content-desc='搜索']")
print(element.location)
print(element.location["x"])
print(element.location["y"])

time.sleep(3)
driver.quit()


```



### 77 appium-api-5-元素操作API-6-获取元素的大小

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"
# 支持中文输入
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 获取 "放大镜" 的大小
element = driver.find_element_by_xpath("//*[@content-desc='搜索']")
print(element.size)
print(element.size["width"])
print(element.size["height"])

time.sleep(3)
driver.quit()


```



### 78 appium-api-5-元素操作API-7-获取元素的属性值

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"
# 支持中文输入
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 1.打开 "设置"
# 2.获取所有 resource-id 为 "com.android.settings:id/title" 的元素
els = driver.find_elements_by_id("com.android.settings:id/title")
# 3.使用 get_attribute 获取这些元素的 enabled, text, content-desc, resource-id, class 属性值
for el in els:
    print(el.get_attribute("enabled"))
    print(el.get_attribute("text"))
    print(el.get_attribute("name"))         # 获取 content-desc 的值 如果没有这个值 就去取 text 的值
    print(el.get_attribute("resourceId"))
    print(el.get_attribute("className"))

time.sleep(3)
driver.quit()
```



### 79 appium-api-6-滑动和拖拽事件-1-总体介绍

```
应用场景
	用于定位: 有些按钮是需要滑动几次屏幕后才出现
	用于业务功能: 比如有些应用存在引导页的功能, 需要翻页才能进入主界面
内容
	swipe
	scroll
	drag_and_drop
```



### 80 appium-api-6-滑动和拖拽事件-2-swipe滑动方法

**方法**

```
# 从一个坐标滑动到另一个坐标, 只能是两个点之间的滑动

driver.swipe(start_x, start_y, end_x, end_y, duration=None)
# 参数:
#	start_x: 起点 x 坐标
#	start_y: 起点 y 坐标
#	end_x: 终点 x 坐标
#	end_x: 终点 y 坐标
#	duration: 滑动这个操作一共持续的时间长度, 单位: 毫秒
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 模拟手指从 (100, 875) 滑动到 (100, 460)     -- 在我的电脑中, 可以理解为从 "存储" 滑动到 "更多"
# 对比 duration 分别设置为 5000 和 100 的两种情况, 查看 "惯性" 的影响
time.sleep(2)
# driver.swipe(100, 875, 100, 460, 5000)
driver.swipe(100, 875, 100, 460, 100)

time.sleep(3)
driver.quit()

# 多数情况下, "惯性" 是我们需要的吗?
# 答案: 不要
```



### 81 appium-api-6-滑动和拖拽事件-3-scroll滑动方法

**方法**

```
# 从一个元素滑动到另一个元素, 直到页面自动停止

driver.scroll(origin_el, destination_el, duration=None)
# 参数:
#	origin_el: 滑动开始的元素
#	destination_el: 滑动结束的元素
#	duration: 滑动的这个操作一共持续的时间长度, 单位: 毫秒 ms
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 模拟手指从 "存储" 滑动到 "更多"
button1 = driver.find_element_by_xpath("//*[@text='存储']")
button2 = driver.find_element_by_xpath("//*[@text='更多']")
driver.scroll(button1, button2)

time.sleep(3)
driver.quit()

```



### 82 appium-api-6-滑动和拖拽事件-4-drag_and_drop拖拽方法

**方法**

```
# 从一个元素滑动到另一个元素, 第二个元素替代第一个元素原本屏幕上的位置

driver.drag_and_drop(origin_el, destination_el)
# 参数:
#	origin_el: 滑动开始的元素
#	destination_el: 滑动结束的元素
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 模拟手指从 "存储" 拖拽到 "更多"
button1 = driver.find_element_by_xpath("//*[@text='存储']")
button2 = driver.find_element_by_xpath("//*[@text='更多']")
driver.drag_and_drop(button1, button2)

time.sleep(3)
driver.quit()

```



### 83 appium-api-6-滑动和拖拽事件-5-滑动和拖拽方法的选择

滑动和拖拽无非就是考虑是否有"惯性", 以及传递的参数是 元素 还是 坐标

- 有 "惯性", 传入 "元素"
  - scroll
- 无 "惯性", 传入 "元素"
  - drag_and_drop
- 有 "惯性", 传入 "坐标"
  - swipe, 并且设置较小的 duration 值
- 无 "惯性", 传入 "坐标"
  - swipe, 并且设置较大的 duration 值



### 84 appium-api-7-高级手势TouchAction-1-总体介绍

```
内容
	轻敲, 按下和抬起, 等待, 长按, 手指移动
应用场景
	如, 手势解锁
使用步骤
	1. 创建 TouchAction 对象
	2. 通过对象调用想执行的手势
	3. 通过 perform() 执行动作
注意点
	所有手势都要通过执行 perform() 才能运行
```



### 85 appium-api-7-高级手势TouchAction-2-轻敲操作

**方法**

```
# 模拟手指对元素或坐标的轻敲操作

TouchAction(driver).tap(element=None, x=None, y=None, count=1).perform()
# 参数:
#	element: 元素
#	x: x坐标
#	y: y坐标
#	count: 点击次数, 默认是1
```

> tap作为高级手势之一, 和 click 有什么区别?
>
> 1. 使用方式不同
> 2. 点击方式不同, click只能点击元素, tap可以同时点击元素和坐标
> 3. tap能控制点击次数, click不能

**代码**

```
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 1.通过 element 轻敲, "设置" 中点击 "WLAN"
# element = driver.find_element_by_xpath("//*[@text='WLAN']")
# TouchAction(driver).tap(element).perform()

# 2.通过 坐标 轻敲, "设置" 中点击 (250, 250)
TouchAction(driver).tap(x=250, y=250).perform()

time.sleep(3)
driver.quit()

```



### 86 appium-api-7-高级手势TouchAction-3-按下和抬起操作

**方法**

```
# 模拟手指对元素或坐标的按下操作

TouchAction(driver).press(el=None, x=None, y=None).perform()
# 参数:
#	el: 元素
#	x: x坐标
#	y: y坐标

# 一般都是成对使用按下和抬起操作
TouchAction(driver).press(el=None, x=None, y=None).release().perform()
```

**代码**

```
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 1.通过 element 按下, "设置" 中按下 "WLAN" 并抬起
# element = driver.find_element_by_xpath("//*[@text='WLAN']")
# TouchAction(driver).press(element).release().perform()

# 2.通过 坐标 按下, "设置" 中按下 (250, 250) 并抬起
TouchAction(driver).press(x=250, y=250).release().perform()

time.sleep(3)
driver.quit()

```



### 87 appium-api-7-高级手势TouchAction-4-等待操作

**方法**

```
# 模拟手指暂停操作

TouchAction(driver).wait(ms=0).perform()
# 参数
#	ms: 暂停的毫秒数, 默认值是0
```

**代码**

```
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 需求: 打开 "设置", 轻敲 (250, 250) 等待2s, 再次长按 (250, 250), 暂停2s, 并抬起
# (长按 WiredSSID时, 有特殊效果, 具体坐标, 要根据你们的分辨率做调整)
TouchAction(driver).tap(x=250, y=250).perform()
time.sleep(2)
TouchAction(driver).press(x=250, y=250).wait(2000).release().perform()

time.sleep(3)
driver.quit()

```



### 88 appium-api-7-高级手势TouchAction-5-长按操作

**方法**

```
# 模拟手指对元素或坐标的长按操作, 后面最好用 release() 抬起

TouchAction(driver).long_press(el=None, x=None, y=None, duration=1000).perform()
# 参数:
#	el: 元素
#	x: x坐标
#	y: y坐标
#	duration: 长按时间, 单位是毫秒
```

**代码**

```
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 需求: 打开 "设置", 轻敲 (250, 250) 等待2s, 再次长按 (250, 250), 暂停2s, 并抬起
# (长按 WiredSSID时, 有特殊效果, 具体坐标, 要根据你们的分辨率做调整)
TouchAction(driver).tap(x=250, y=250).perform()
time.sleep(2)
TouchAction(driver).long_press(x=250, y=250, duration=2000).release().perform()
# TouchAction(driver).press(x=250, y=250).wait(2000).release().perform()

time.sleep(3)
driver.quit()

```



### 89 appium-api-7-高级手势TouchAction-6-移动操作

**方法**

```
# 模拟手指对元素或坐标的移动操作

# TouchAction(driver).move_to(el=None, x=None, y=None).perform()
# 参数:
#	el: 元素
#	x: x坐标
#	y: y坐标
```

**代码**

```
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
# desired_caps["appActivity"] = ".Settings"
desired_caps["appActivity"] = ".ChooseLockPattern"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 画一个 "L" 图形
# 360 415
# 360 658
# 360 901
# 600 901
TouchAction(driver).press(x=360, y=415).wait(2000).\
    move_to(x=360, y=658).wait(2000).\
    move_to(x=360, y=901).wait(2000).\
    move_to(x=600, y=901).wait(2000).release().perform()

time.sleep(3)
driver.quit()

```



### 91 appium-api-8-手机操作API-1-总体介绍

```
内容
	获取手机分辨率
	获取手机截图
	获取和设置网络状态
	发送键到设备
	打开和关闭手机通知栏
```



### 92 appium-api-8-手机操作API-2-获取手机分辨率

**方法**

```
# 获取手机分辨率
driver.get_window_size()
# 返回值: 字典
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 打印当前屏幕的分辨率
print(driver.get_window_size())

time.sleep(3)
driver.quit()

# 随堂作业: 按照坐标, 从 屏幕 y 轴 4分之3 滑动到 4分之1 , 要求横坐标是屏幕的 2分之一
```



### 93 appium-api-8-手机操作API-3-获取手机截图

**方法**

```
# 获取手机截图

driver.get_screenshot_as_file(filename)
# 参数:
#	filename: 指定路径下, 指定格式的图片 (png格式)
```

**代码**

```
import time
from appium import webdriver
from datetime import datetime

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 获取手机截图, 保存到 screenshot 目录
driver.get_screenshot_as_file("./screenshot/screen%s.png" % datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])

time.sleep(3)
driver.quit()
```



### 94 appium-api-8-手机操作API-4-获取和设置手机网络

**属性**

```
# 获取手机网络
driver.network_connection
```

**方法**

```
# 设置手机网络
driver.set_network_connection(connectionType)
# 参数:
#	connectionType: 网络类型
```

**代码**

```
import time
from appium import webdriver
from appium.webdriver.connectiontype import ConnectionType

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 由于在夜神模拟器中执行 设置网络状态 的方法会断开模拟器的adb连接,
# 需要执行设置网络状态的方法时, 同时在命令行执行 nox_adb connect 127.0.0.1:62001 重新连接, 否则会报错

# """Sets the network connection type. Android only.
# Possible values:
#     Value (Alias)      | Data | Wifi | Airplane Mode
#     -------------------------------------------------
#     0 (None)           | 0    | 0    | 0
#     1 (Airplane Mode)  | 0    | 0    | 1
#     2 (Wifi only)      | 0    | 1    | 0
#     4 (Data only)      | 1    | 0    | 0
#     6 (All network on) | 1    | 1    | 0
# These are available through the enumeration `appium.webdriver.ConnectionType`
#
# Args:
#     connection_type (int): a member of the enum appium.webdriver.ConnectionType
#
# Returns:
#     `WebDriver`
# """

# 获取当前网络类型, 并打印
print("设置前:", driver.network_connection)
# 设置当前设备为飞行模式
# driver.set_network_connection(1)    # 1 为飞行模式
driver.set_network_connection(ConnectionType.ALL_NETWORK_ON)    # 可读性更好

print("设置后:", driver.network_connection)

time.sleep(3)
driver.quit()

```



### 96 appium-api-8-手机操作API-5-发送键到设备

**方法**

```
# 发送键到设备
# 可以搜索关键字 "android keycode"
driver.press_keycode(keycode)
# 参数:
#	keycode: 发送给设备的代表按键的代码
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 模拟点击3次音量+ , 再点击返回, 再点击2次音量-
time.sleep(2)
driver.press_keycode(24)
time.sleep(2)
driver.press_keycode(24)
time.sleep(2)
driver.press_keycode(24)
time.sleep(2)
driver.press_keycode(4)
time.sleep(2)
driver.press_keycode(25)
time.sleep(2)
driver.press_keycode(25)

time.sleep(3)
driver.quit()
```



### 97 appium-api-8-手机操作API-6-操作手机通知栏

**方法**

```
# 打开手机通知栏
# appium官方并没有为我们提供关闭通知栏的api, 那么现实生活中怎么关闭, 就怎么操作, 比如, 手指从下往上滑动, 或者, 按返回键
driver.open_notifications()
```

**代码**

```
import time
from appium import webdriver

desired_caps = dict()
desired_caps["platformName"] = "android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "127.0.0.1:62001"
desired_caps["appPackage"] = "com.android.settings"
desired_caps["appActivity"] = ".Settings"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 打开手机通知栏, 2s后, 关闭通知栏
driver.open_notifications()
time.sleep(2)
driver.press_keycode(4)

time.sleep(3)
driver.quit()

```



### 98 appium-api-9-小结





































