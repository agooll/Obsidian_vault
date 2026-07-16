### 32 app自动化入门-1-自动化环境搭建-1-基本概念



### 33 app自动化入门-1-自动化环境搭建-2-环境分析



### 34 app自动化入门-1-自动化环境搭建-3-安装配置-1-JDK



### 35 app自动化入门-1-自动化环境搭建-3-安装配置-2-AndroidSDK



### 36 app自动化入门-1-自动化环境搭建-3-安装配置-3-夜神模拟器



### 38 app自动化入门-1-自动化环境搭建-3-安装配置-4-Appium



### 39 app自动化入门-1-自动化环境搭建-3-安装配置-5-python相关



### 40 app自动化入门-1-自动化环境搭建-4-工具介绍-1-AndroidSDK



### 41 app自动化入门-1-自动化环境搭建-4-工具介绍-2-Appium



### 42 app自动化入门-2-adb调试工具-1-总体介绍



### 44 app自动化入门-2-adb调试工具-2-常用命令-1-获取包名和界面名



### 46 app自动化入门-2-adb调试工具-2-常用命令-2-文件传输



### 48 app自动化入门-2-adb调试工具-2-常用命令-3-获取app启动时间



### 50 app自动化入门-2-adb调试工具-2-常用命令-4-获取手机日志



### 51 app自动化入门-2-adb调试工具-2-常用命令-5-安装卸载



### 52 app自动化入门-2-adb调试工具-2-常用命令-6-其他命令



### 53 app自动化入门-3-Hello Appium-1-快速体验

**代码**

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



### 54 app自动化入门-3-Hello Appium-2-参数详解

**代码**

```
# 导包
from appium import webdriver
# 初始化一个空字典, 变量名叫 desired_caps
desired_caps = dict()
# 系统名, 不区分大小写  用 android Android anDroiD
desired_caps["platformName"] = "android"
# 系统版本号, 可以简写 如, 5.1.1 可以写成 5.1 或者 5 都可以
desired_caps["platformVersion"] = "5.1"
# 设备名, 可以通过 adb devices 获取, 注意: 在 Android平台下设备名可以是任何字符, 但是不能不写
desired_caps["deviceName"] = "*"
# 要自动化打开的程序包的包名
desired_caps["appPackage"] = "com.android.settings"
# 要自动化打开的程序的界面名
desired_caps["appActivity"] = ".Settings"

# 获取驱动对象
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# 关闭驱动对象
driver.quit()
```



### 55 app自动化入门-4-小结



































































