### 182 Git-1-总体介绍



### 183 Git-2-安装



### 184 Git-3-配置

因为 git 是分布式版本控制系统, 所以, 每个人(每部pc)都必须自报家门: 需要配置你的名字和Email地址

```
git config --global user.name "xxx"
git config --global user.email "xxxx@xxx.com"
```

> 校验方式:
>
> 命令行执行 git config --list 可以查看



### 185 Git-4-工作流-1-介绍

**介绍**

- 工作区, 就是你平时存放项目代码的地方
- 暂存区, 用于临时存放你的改动, 事实上她只是一个文件, 保存即将提交的文件列表信息
- 本地仓库, 就是安全存放数据的位置, 这里有你提交的所有版本的数据
- 远程仓库, 托管代码的服务器

**核心流程**

1. 工作区 ---> 远程仓库 
2. 远程仓库 ---> 工作区



### 186 Git-4-工作流-2-准备工作

```
远程仓库有哪些
	gitee
		码云
	gitlab
	github
创建github远程仓库
	1. 进入首页: https://github.com
	2. 注册用户
	3. 登录并创建远程仓库
```



### 187 Git-4-工作流-3-工作区-->远程仓库

```
1. 创建工作区
	git init
2. 把工作区的文件添加在暂存区
	git add .
		添加所有文件到暂存区
	git add 文件名
		添加指定到暂存区
3. 把暂存区文件提交到本地仓库
	git commit -m "xxx"
		"xxx"对于本次提交的描述
4. 把本地仓库的文件提交到远程仓库
	1. 首次提交
		git push -u 远程仓库地址 master
		-u 参数表示首次提交携带用户名和密码
	2. 非首次提交
		git push 远程仓库地址
```



### 189 Git-4-工作流-4-远程仓库-->工作区

```
1. 首次从远程仓库下载代码到本地仓库和工作区
	git clone 远程仓库地址
2. 从远程仓库更新代码到本地仓库和工作区
	git pull
```



### 190 Git-5-分支管理

```
查看本地分支
	git branch
创建本地分支
	git branch 自定义分支名
切换本地分支
	git checkout 目标分支名
合并本地分支
	git merge 被合并到master的分支名
```



### 191 Git-6-版本回退

```
步骤
	1. 列表展示当前git仓库的操作记录
		git reflog
	2. 回退到某一版本
		git reset --hard 对应版本hash值
```



### 192 Git-7-pycharm和git结合

```
GUI工具
	图像用户接口
	列举
		1. 自带的
		2. 小乌龟
		3. SourceTree
		4. pycharm
```

**pycharm+git的使用步骤**

1. 配置 git, 让 pycharm 能使用 git

   File -> Settings -> Version Control -> Git -> Path to Git executable

2. 初始化仓库, 相当于 git init

   VCS -> Import into Version Control -> Create Git Repository

3. 配置忽略文件 .gitignore

   1. 安装 .gitignore 插件

      File -> Settings -> Plugins -> 搜索 .gitignore 并安装 -> 重启IDE

   2. 新增或复制 .gitignore 文件

      > 新增:
      >
      > 右键项目 -> New -> .ignore file -> .gitignore file -> Ignore File Generator -> 选 Example user template -> Generate
      >
      > 复制:
      >
      > 把 .gitignore 文件复制到项目根目录下

4. 添加文件到暂存区, 相当于 git add

   右键文件 -> Git -> Add

5. 添加文件到本地仓库, 相当于 git commit -m "xxx"

   右键文件 -> Git -> Commit File -> 填写 Commit Message -> Commit

6. 推送到远程仓库, 相当于 git push xxx

   右键文件 -> Git -> Repository -> Push -> Define remote -> URL 填写远程仓库地址 -> Push



### 195 Charles-1-总体介绍

```
charles 是一款抓包工具
对比 fiddler, charles 有如下优点
	体积小巧
	专一: 只抓http/https 的包
	界面清爽
	易上手
	用户量大
```



### 196 Charles-2-安装过程

```
总体介绍
	charles 是一款抓包工具
	对比 fiddler, charles 有如下优点
		体积小巧
		专一: 只抓http/https 的包
		界面清爽
		易上手
		用户量大
	使用抓包工具会用到工具的代理上网功能
		用不好, 可能会影响网络
安装过程
	1. 下载, 地址: https://www.charlesproxy.com/download/
	2. 双击 exe 文件进行安装
	3. 破解
```



### 197 Charles-3-界面功能介绍



### 198 Charles-4-抓包配置

**charles配置**

- http 代理配置

  - Proxy -> Proxy Settings -> Proxies -> 在 HTTP Proxy 中填写端口号并在Enable... 处打钩

- https 代理配置

  - Proxy -> SSL Proxying Settings -> SSL Proxying -> 添加代理拦截的网址和端口并在 Enable... 处打钩

- https 抓包, 安装客户端证书

  - PC客户端安装证书

    Help -> SSL Proxying -> Install Charles Root Certificate -> 进行安装

  - 移动端安装证书

    Help -> SSL Proxying -> Install Charles Root Certificate on a Mobile Device or Remote Browser -> 查看移动端安装证书的注意事项

    - Android 安装
    - iOS 安装

**电脑端的配置**

配置使用代理 (不同系统/浏览器的设置方式不同, 以我本机为例):

打开IE -> 设置 -> Internet 选项 -> 连接 -> 局域网设置 -> 代理服务器下面打钩 -> 确定保存

**手机端的配置**

- Android

  - 配置使用代理 (以模拟器为例)

    设置 -> WLAN -> 长按连接的网络 -> 修改网络 -> 高级 -> 手动 -> 输入电脑ip地址和端口

  - 安装证书

    手机浏览器打开 chls.pro/ssl 下载并安装证书

- iOS

  - 配置使用代理

    略

  - 安装证书

    1. 手机浏览器打开 chls.pro/ssl 下载描述文件

    2. 设置 -> 通用 -> 描述文件与设备管理, 会多一个证书 

    3. 设置 -> 通用 -> 关于手机 最下方 -> 证书信任设置, 打开对 charles proxy 证书的信任



### 199 Charles-5-常用功能-弱网

**弱网测试**

- 方式1: Proxy -> Throttle Settings -> 勾选 Enable Throttling 并选择弱网环境

- 方式2: 点亮小乌龟图标即可



### 200 Jenkins-1-总体介绍

```
总体介绍
	Jenkins是什么?
		Jenkins是一个开源软件项目, 是基于java开发的一种CI工具
	CI是什么?
		概念
			Continuous Integration 缩写为 CI 意思是持续集成 (频繁的将代码集成到主干(master))
		目的
			使产品能够快速迭代, 同时还能保持高质量
			核心措施: 代码集成到主干之前, 必须通过所有测试用例, 只要有一个测试用例失败, 就不允许集成到主干
		作用
			快速发现错误, 每完成一点更新, 就集成到主干
			防止分支大幅度偏离主干
	CI实践流程
		1. 通过Jenkins监控发现被测程序代码是否有更新
		2. 拉取被测服务代码并部署到测试环境
		3. 自动触发自动化测试代码
		4. 测试通过
		5. 通知开发人员, 告之将代码合并到主干
	Jenkins常用场景
		测试环境, 一键部署
```



### 201 Jenkins-2-安装方式

```
在线安装
	步骤
		1.进入 jenkins.war所在目录, 通过 java -jar jenkins.war 启动服务
		2.浏览器输入 localhost:8080, 访问jenkins服务
		3.输入密码
		4.选择推荐安装的插件进行安装, 等待安装完成
		5.设置管理员的用户名/密码, 即可使用
离线安装[推荐]
	步骤
		1.把.jenkins 文件夹复制到用户目录下
		2.进入 jenkins.war所在目录, 通过 java -jar jenkins.war 启动服务
		3.浏览器输入 localhost:8080, 访问jenkins服务
		4.输入admin/123456 点击登录
```



### 202 Jenkins-3-插件安装

**安装过程**

1. jenkins 安装 allure 插件

   > 插件作用:
   >
   > 生成 allure 的 xml 文件
   >
   > 操作步骤:
   >
   > 进入jenkins -> 系统管理 -> 管理插件 -> 可选插件 -> 搜索 allure -> 勾选第一条并点击"直接安装"

2. jenkins 安装 allure commandline 工具

   > 工具作用:
   >
   > 把 allure 的 xml 文件转化成 html 格式的报告
   >
   > 操作步骤:
   >
   > 进入jenkins -> 系统管理 -> 全局工具配置 -> Allure Commandline 配置"别名"(别名随意), "安装目录", 取消勾选自动安装并点击save

**全局工具配置**

1. 配置JDK
2. 配置Git



### 203 Jenkins-4-持续集成配置-1-总体介绍

```
配置过后, 会自动执行一整套流程
	1. 自动监测远程仓库的代码更新
	2. 自动从 github 下载自动化测试项目代码
	3. 自动执行自动化测试 (自动运行 pytest)
	4. 自动生成 allure 报告
```



### 204 Jenkins-4-持续集成配置-2-项目准备

**目录**

```
- scripts
- - test_demo.py
- .gitignore
- demo.py
- pytest.ini
```

**代码**

test_demo.py

```
class TestDemo:

    def test_a(self):
        assert 1

    def test_b(self):
        assert 0

```

pytest.ini

```
[pytest]
addopts = -s --alluredir report
testpaths = ./scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**手动运行**

1. 执行 pytest 得到测试结果和 xml 报告

2. 得到 html 格式的测试报告

   ```
   allure generate report/ -o report/html --clean
   ```

   

### 205 Jenkins-4-持续集成配置-3-将项目上传到github



### 206 Jenkins-4-持续集成配置-4-新建jenkins项目



### 207 Jenkins-4-持续集成配置-5-配置General



### 208 Jenkins-4-持续集成配置-6-配置源码管理



### 209 Jenkins-4-持续集成配置-7-配置构建



### 210 Jenkins-4-持续集成配置-8-配置后操作



### 211 Jenkins-4-持续集成配置-9-配置构建触发器



### 212 Jenkins-5-小结























