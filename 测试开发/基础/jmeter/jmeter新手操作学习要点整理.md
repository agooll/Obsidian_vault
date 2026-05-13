# JMeter 操作

> 适合场景：接口测试入门、JMeter 作业复盘、登录 token 传递、多接口串联、JSON 断言、JSON 提取器、跨线程组变量传递、JDBC 预处理器取数据库数据。

---

## 1. JMeter 做接口测试的基本流程

JMeter 做接口测试时，核心流程一般是：

```text
测试计划
  ↓
线程组
  ↓
HTTP 请求
  ↓
参数 / 请求头 / 请求体
  ↓
断言
  ↓
监听器查看结果
```

常见步骤：

1. 新建测试计划 `Test Plan`
2. 添加线程组 `Thread Group`
3. 添加 HTTP 请求默认值，统一设置 IP、端口、协议等
4. 添加 HTTP 信息头管理器，统一设置请求头
5. 添加具体 HTTP 请求，例如登录、查询用户、添加用户、修改状态等
6. 添加 JSON 提取器，从上一个接口响应中提取 token、userId、roleId 等
7. 添加 JSON 断言，判断接口返回是否符合预期
8. 添加察看结果树、聚合报告等监听器查看结果

---

## 2. 线程组里的三个核心参数

线程组中最重要的是：

```text
线程数
Ramp-up 时间
循环次数
```

### 2.1 线程数 Number of Threads / Users

线程数表示模拟多少个虚拟用户。

例如：

```text
线程数 = 10
```

表示 JMeter 模拟 10 个用户访问接口。

在 JMeter 中，可以把一个线程简单理解为一个虚拟用户。

### 2.2 启动时间 Ramp-up Period

Ramp-up 表示这些用户在多少秒内全部启动完成。

例如：

```text
线程数 = 10
Ramp-up = 5 秒
```

意思是：JMeter 会在 5 秒内启动完 10 个用户，平均每 0.5 秒启动 1 个用户。

注意：

```text
Ramp-up 不是接口运行总时间，而是用户逐步启动的时间。
```

### 2.3 循环次数 Loop Count

循环次数表示每个虚拟用户重复执行测试请求多少次。

例如：

```text
线程数 = 10
循环次数 = 3
```

总请求数大约是：

```text
10 × 3 = 30 次
```

如果线程组下面有多个 HTTP 请求，那么每个用户会按顺序执行这些请求，然后根据循环次数重复。

---

## 3. HTTP 请求方法基础

JMeter 接口测试中经常会用到 HTTP 请求方法。

| 方法 | 常见作用 | 举例 |
|---|---|---|
| GET | 查询 / 获取数据 | 查询用户列表、获取商品信息 |
| POST | 新增 / 提交数据 | 登录、注册、提交订单、添加用户 |
| PUT | 完整更新资源 | 修改用户完整信息、分配角色 |
| PATCH | 局部更新资源 | 只修改用户状态、只改手机号 |
| DELETE | 删除资源 | 删除用户、删除订单 |
| HEAD | 只获取响应头 | 检查资源是否存在 |
| OPTIONS | 查看支持的方法 / 跨域预检 | 浏览器跨域预检请求 |

面试口语版：

> HTTP 接口常见类型可以按请求方法划分，常用的有 GET、POST、PUT、PATCH、DELETE。GET 一般用于查询数据，POST 用于提交或新增数据，PUT 用于完整更新，PATCH 用于局部更新，DELETE 用于删除资源。

---

## 4. GET 和 POST 的区别

| 对比点 | GET | POST |
|---|---|---|
| 主要用途 | 查询 / 获取数据 | 提交 / 新增数据 |
| 参数位置 | 通常放在 URL 后面 | 通常放在请求体 body 中 |
| 数据量 | 受 URL 长度限制 | 更适合传较多数据 |
| 安全性表现 | 参数暴露在 URL 中 | 参数在请求体中，相对不直接暴露 |
| 幂等性 | 一般是幂等的 | 一般不是幂等的 |

注意：

```text
POST 不是服务端向客户端发送数据。
POST 是客户端向服务端提交数据。
```

面试口语版：

> GET 一般用于从服务端获取数据，参数通常放在 URL 中；POST 一般用于向服务端提交数据，参数通常放在请求体中。GET 更适合查询，POST 更适合新增、登录、注册、提交表单等操作。POST 不是服务端向客户端发送数据，而是客户端向服务端提交数据。

### 4.1 JMeter 里什么时候用“消息体数据”

先记一句话：

```text
消息体数据 = HTTP Body（请求体）
只有接口文档要求“参数在 body 里”时，才填这个区域。
```

按请求方法快速判断：

| 请求方法 | JMeter 常用填写位置 | 是否常用“消息体数据” |
|---|---|---|
| GET | `参数`页签（query 参数）或直接拼在 URL | 一般不用 |
| POST（JSON） | `消息体数据`页签 | 常用 |
| POST（表单） | `参数`页签（x-www-form-urlencoded） | 视接口而定 |
| PUT / PATCH | 多数接口放 body | 常用 |
| DELETE | 看接口文档，有的放 query，有的放 body | 不固定 |

结合你截图这个场景：

- 你当前是 `GET` 请求，路径是查询字典类型，通常是“查数据”接口。
- 这种接口一般不用 `消息体数据`，优先放在 `参数`页签（例如 `dictType=wms_receipt_type`）或 URL 查询串。
- 如果你在 GET 里填了 `消息体数据`，很多后端会忽略，可能看起来“发了但没生效”。

什么时候必须填“消息体数据”：

1. 接口文档明确写了 `Body` / `Request Body`
2. 文档给的是 JSON 示例
3. 请求头要求 `Content-Type: application/json`

典型 JSON body 示例（放在“消息体数据”）：

```json
{
  "username": "test01",
  "password": "123456",
  "rememberMe": true
}
```

常见错误排查：

- 明明填了 JSON，但没设置 `Content-Type: application/json`
- 把 query 参数错填到“消息体数据”
- GET 接口误用 body，后端不解析
- 字段名大小写、层级和文档不一致

面试表达：

> 我会先看接口文档参数位置。如果是 query/path 参数，我在 JMeter 的参数或路径里填；如果是 Request Body（尤其 JSON），我会在消息体数据里填，并配套设置 Content-Type 为 application/json。

---

## 5. HTTP 状态码和业务状态码

### 5.1 HTTP 状态码分类

| 状态码 | 含义 |
|---|---|
| 1XX | 信息提示，实际接口测试中较少关注 |
| 2XX | HTTP 请求成功，例如 200、201 |
| 3XX | 重定向，例如 301、302 |
| 4XX | 客户端错误，例如 400、401、403、404 |
| 5XX | 服务端错误，例如 500、502、503 |

### 5.2 重点：HTTP 成功不等于业务成功

接口测试中要特别注意：

```text
HTTP 状态码 200 只代表 HTTP 请求成功。
不一定代表业务成功。
```

例如响应：

```json
{
  "data": null,
  "meta": {
    "msg": "用户名或密码错误",
    "status": 400
  }
}
```

即使 HTTP 状态码是 200，业务也可能失败。

所以接口测试通常要同时断言：

```text
HTTP 状态码
业务状态码
业务提示信息
关键业务字段
```

---

## 6. 请求头和响应头常见字段

### 6.1 请求头常见字段

| 字段             | 含义                  |
| -------------- | ------------------- |
| Host           | 请求的服务器域名或 IP        |
| User-Agent     | 客户端信息，例如浏览器、操作系统    |
| Accept         | 客户端希望接收的数据类型        |
| Content-Type   | 请求体的数据格式，例如 JSON、表单 |
| Content-Length | 请求体长度               |
| Authorization  | 身份认证信息，例如 token     |
| Cookie         | 客户端携带的 Cookie       |
| Referer        | 请求来源页面              |
| Origin         | 请求来源，常用于跨域校验        |
| Cache-Control  | 缓存控制                |

注意：

```text
请求方法、请求 URL 不属于请求头。
它们属于请求行。
```

### 6.2 响应头常见字段

| 字段                          | 含义           |
| --------------------------- | ------------ |
| Content-Type                | 响应体的数据格式     |
| Content-Length              | 响应体长度        |
| Set-Cookie                  | 服务端设置 Cookie |
| Cache-Control               | 缓存策略         |
| Location                    | 重定向地址        |
| ETag                        | 资源标识，用于缓存校验  |
| Last-Modified               | 资源最后修改时间     |
| Server                      | 服务端软件信息      |
| Date                        | 服务端响应时间      |
| Access-Control-Allow-Origin | 跨域相关字段       |

注意：

```text
状态码不属于响应头。
状态码属于响应状态行。
```

---

## 7. JSON 断言：判断接口返回是否符合预期

JSON 断言用于判断响应体中的 JSON 字段是否存在、是否等于预期值。

例如登录接口返回：

```json
{
  "data": {
    "username": "admin",
    "token": "Bearer eyJhbGci..."
  },
  "meta": {
    "msg": "登录成功",
    "status": 200
  }
}
```

如果要断言登录成功，可以配置：

```text
Assert JSON Path exists: $.meta.msg
勾选 Additionally assert value
Expected Value: 登录成功
```

如果要断言业务状态码：

```text
Assert JSON Path exists: $.meta.status
勾选 Additionally assert value
Expected Value: 200
```

### 7.1 JSON 断言四个复选框

#### Additionally assert value

意思是：额外断言值。

不勾选时：

```text
只判断 JSONPath 对应字段是否存在。
```

勾选后：

```text
不仅判断字段存在，还判断字段值是否等于 Expected Value。
```

例如：

```text
$.meta.msg
Expected Value: 创建成功
```

如果不勾选 `Additionally assert value`，只要 `msg` 字段存在就通过，不管它是不是“创建成功”。

如果勾选，就必须等于“创建成功”才通过。

#### Match as regular expression

意思是：按正则表达式匹配。

如果只是判断固定值，不建议勾选。

如果勾选，可以写：

```text
^创建成功$
```

表示必须完整等于“创建成功”。

也可以写：

```text
.*成功.*
```

表示只要包含“成功”就可以。

#### Expect null

意思是：期望这个字段值是 null。

例如：

```json
{
  "data": null
}
```

可以断言：

```text
Assert JSON Path exists: $.data
勾选 Expect null
```

普通判断 msg、status 时不要勾选。

#### Invert assertion

意思是：反向断言。

勾选后，条件满足反而失败。

例如：

```text
$.meta.msg = 创建成功
勾选 Invert assertion
```

含义变成：

```text
如果 msg 是 创建成功，则失败。
如果 msg 不是 创建成功，则通过。
```

一般用于判断响应中不能出现某些值。

### 7.2 判断“创建成功”的推荐配置

```text
Assert JSON Path exists: $.meta.msg
勾选 Additionally assert value
不勾选 Match as regular expression
Expected Value: 创建成功
不勾选 Expect null
不勾选 Invert assertion
```

---

## 8. 响应断言和 JSON 断言的区别

### 8.1 响应断言

响应断言一般是判断响应文本中是否包含某个字符串。

例如：

```text
登录成功
```

它会判断响应体中有没有“登录成功”这几个字。

优点：简单。

缺点：不够精确。

它不能保证“登录成功”一定是 `meta.msg` 字段的值。

### 8.2 JSON 断言

JSON 断言可以精确判断某个 JSON 字段。

例如：

```text
$.meta.msg = 登录成功
```

它表示：

```text
取 meta 下面的 msg 字段，判断它是否等于 登录成功。
```

接口测试中更推荐使用 JSON 断言。

---

## 9. JSON 提取器：从响应中提取变量

JSON 提取器用于从上一个接口响应中提取数据，给后面的接口使用。

例如登录接口返回：

```json
{
  "data": {
    "token": "Bearer eyJhbGci..."
  },
  "meta": {
    "msg": "登录成功",
    "status": 200
  }
}
```

要提取 token，JSON 提取器配置：

```text
Apply to: Main sample only
Names of created variables: token
JSON Path expressions: $.data.token
Match No.: 1
Default Values: NOT_FOUND
```

### 9.1 Apply to 应该怎么选

常用选择：

```text
Main sample only
```

含义是：从当前请求的主响应中提取。

你之前的问题是选成了：

```text
JMeter Variable Name to use
```

这个选项不是从接口响应体中提取，而是从某个 JMeter 变量里的 JSON 字符串中提取。

如果你填了“登录1.2.1”，JMeter 会理解成：

```text
从一个叫 登录1.2.1 的变量中提取 JSON。
```

但实际上你没有这个变量，所以会提取失败。

所以挂在登录请求下面的 JSON 提取器，一般选：

```text
Main sample only
```

### 9.2 Match No. 怎么填

```text
1：取第一个匹配结果
0：随机取一个匹配结果
-1：取所有匹配结果
```

初学时通常填：

```text
1
```

### 9.3 Default Values 的作用

推荐填：

```text
NOT_FOUND
```

这样如果提取失败，就会显示：

```text
token = NOT_FOUND
```

方便排查。

不要空着，否则提取失败时不容易发现。

---

## 10. 同线程组和跨线程组使用变量的区别

这是你之前 token 传递问题的核心。

### 10.1 同一个线程组：直接用 `${变量名}`

如果结构是：

```text
线程组
  登录接口
    JSON 提取器：提取 token
  用户数据列表接口
```

那么后续接口可以直接使用：

```text
${token}
```

例如 HTTP 信息头管理器：

```text
Authorization    ${token}
```

### 10.2 不同线程组：不能直接用 `${token}`

如果结构是：

```text
线程组1
  登录接口
    JSON 提取器：提取 token

线程组2
  用户数据列表接口
```

这时候不能直接用：

```text
${token}
```

因为 JMeter 变量默认只在当前线程内有效，不能直接跨线程组共享。

跨线程组要用 JMeter Property。

---

## 11. 跨线程组传递 token 的正确做法

跨线程组传 token 的流程：

```text
登录接口返回 token
        ↓
JSON 提取器提取成变量 ${token}
        ↓
后置处理器把 ${token} 保存到 JMeter Property
        ↓
其他线程组通过 ${__P(token,NOT_FOUND)} 使用
```

### 11.1 登录接口下面添加 JSON 提取器

配置：

```text
Apply to: Main sample only
Names of created variables: token
JSON Path expressions: $.data.token
Match No.: 1
Default Values: NOT_FOUND
```

### 11.2 登录接口下面添加 JSR223 后置处理程序

推荐使用 JSR223 PostProcessor，语言选择 Groovy。

脚本：

```groovy
String t = vars.get("token")

if (t == null || t == "NOT_FOUND" || t.trim().length() == 0) {
    log.error("token 提取失败，当前 token = " + t)
} else {
    props.put("token", t)
    log.info("已保存 token 到 JMeter Property = " + props.get("token"))
}
```

结构应该是：

```text
登录接口
  JSON 提取器
  JSR223 后置处理程序
```

注意：JSON 提取器要先执行，JSR223 后置处理程序再把提取结果保存到 property。

### 11.3 后续线程组的请求头中使用 token

HTTP 信息头管理器：

```text
Authorization    ${__P(token,NOT_FOUND)}
```

或者：

```text
Authorization    ${__property(token,,NOT_FOUND)}
```

推荐初学时使用：

```text
${__P(token,NOT_FOUND)}
```

更短，更容易看。

---

## 12. Authorization 携带 token 的注意事项

### 12.1 token 已经带 Bearer

如果登录响应返回的是：

```text
Bearer eyJhbGciOiJIUzI1NiIs...
```

说明 token 本身已经包含 `Bearer`。

请求头应该写：

```text
Authorization    ${token}
```

或者跨线程组写：

```text
Authorization    ${__P(token,NOT_FOUND)}
```

不要写：

```text
Authorization    Bearer ${token}
```

否则会变成：

```text
Bearer Bearer eyJhbGci...
```

这样接口会认证失败。

### 12.2 token 不带 Bearer

如果登录响应返回的是纯 token：

```text
eyJhbGciOiJIUzI1NiIs...
```

才需要手动加：

```text
Authorization    Bearer ${token}
```

或者跨线程组：

```text
Authorization    Bearer ${__P(token,NOT_FOUND)}
```

---

## 13. 为什么全局属性里显示 `token = ${token}` 是错的

你之前在“属性显示”中看到：

```text
token    ${token}
```

这说明保存到 JMeter Property 里的不是实际 token，而是字符串 `${token}`。

正确结果应该类似：

```text
token    Bearer eyJhbGciOiJIUzI1NiIs...
```

错误原因通常是：

```text
1. 直接在全局属性里手动写了 token = ${token}
2. JSON 提取器没有提取成功
3. setProperty 执行时机不对
4. 跨线程组还没登录成功，后面的接口就先执行了
```

正确做法是通过后置处理器写入 property：

```groovy
props.put("token", vars.get("token"))
```

不要在属性显示里手动写：

```text
token = ${token}
```

---

## 14. 线程组顺序问题

跨线程组时，必须保证登录线程组先执行，后面的业务线程组再执行。

否则会出现：

```text
业务接口先执行
登录接口还没生成 token
Authorization = NOT_FOUND 或空
接口认证失败
```

解决方式：

### 方式一：勾选测试计划中的顺序执行线程组

在测试计划中勾选：

```text
Run Thread Groups consecutively
```

中文可能显示为：

```text
独立运行每个线程组 / 按顺序运行线程组
```

### 方式二：使用 setUp Thread Group

更规范的结构：

```text
setUp Thread Group
  登录接口
    JSON 提取器
    JSR223 后置处理程序

普通线程组
  用户数据列表
  添加用户
  修改用户状态
```

`setUp Thread Group` 会在普通线程组之前执行，适合做登录、初始化数据。

---

## 15. JSON 提取器作用域问题

如果 JSON 提取器挂在某个 HTTP 请求下面，例如：

```text
添加用户 1.3.2
  JSON 断言
  JSON 提取器
修改用户状态 1.3.3
```

那么这个 JSON 提取器的作用是：

```text
从 添加用户 1.3.2 的响应结果中提取数据。
```

它不会去提取 1.3.3 的响应。

但是提取出来的变量可以给后面的 1.3.3 使用，前提是：

```text
1.3.2 和 1.3.3 在同一个线程组里
并且 1.3.3 执行顺序在 1.3.2 后面
```

例如添加用户返回：

```json
{
  "data": {
    "id": 501
  },
  "meta": {
    "msg": "创建成功",
    "status": 200
  }
}
```

1.3.2 下的 JSON 提取器：

```text
Names of created variables: userId
JSON Path expressions: $.data.id
Match No.: 1
Default Values: NOT_FOUND
```

那么 1.3.3 可以使用：

```text
${userId}
```

例如路径：

```text
${url}/users/${userId}/state
```

---

## 16. JDBC 预处理程序：从数据库查询数据给接口使用

你之前用 JDBC 预处理程序查询角色 ID：

```sql
select role_id from sp_role;
```

然后在 `Variable names` 里写：

```text
rid
```

JMeter 会自动生成这些变量：

```text
rid_1 = 查询结果第 1 行的 role_id
rid_2 = 查询结果第 2 行的 role_id
rid_3 = 查询结果第 3 行的 role_id
...
rid_# = 查询结果总行数
```

所以你在 HTTP 请求里写：

```text
rid    ${rid_1}
```

是可以取到的。

### 16.1 为什么没有定义 rid_1 也能用

因为 `rid_1` 是 JDBC 预处理程序运行 SQL 后自动生成的变量。

它不是你手动在用户定义变量里定义的。

执行顺序是：

```text
分配用户角色接口
  ↓
先执行 JDBC 预处理程序
  ↓
查询数据库 select role_id from sp_role;
  ↓
生成 rid_1、rid_2、rid_# 等变量
  ↓
再执行 HTTP 请求
  ↓
HTTP 请求中使用 ${rid_1}
```

### 16.2 查询结果不稳定的问题

如果 SQL 是：

```sql
select role_id from sp_role;
```

数据库有多行角色时，第一行不一定永远稳定。

更稳的写法是加排序或条件：

```sql
select role_id from sp_role order by role_id limit 1;
```

或者指定角色名：

```sql
select role_id from sp_role where role_name = '普通用户';
```

具体字段名要根据你的数据库表结构调整。

---

## 17. HTTP 信息头管理器常见配置

接口测试中常用请求头：

```text
Content-Type      application/json
Authorization     ${token}
```

如果是 JSON 请求体，通常需要：

```text
Content-Type: application/json
```

如果需要登录 token：

同线程组：

```text
Authorization: ${token}
```

跨线程组：

```text
Authorization: ${__P(token,NOT_FOUND)}
```

如果接口要求表单格式，可能是：

```text
Content-Type: application/x-www-form-urlencoded
```

你截图里的三个头含义：

- `content-type: application/json;charset=UTF-8`：告诉后端“我发的是 JSON 请求体，编码 UTF-8”。
- `Accept: application/json`：告诉后端“我希望你返回 JSON”。
- `authorization: ${__property(token,,)}`：从 JMeter 全局属性读取 token 做身份认证。

### 17.1 认证头推荐模板（不会错版）

模板 A（token 已自带 Bearer）：

```text
content-type    application/json;charset=UTF-8
Accept          application/json
Authorization   ${__P(token,NOT_FOUND)}
```

模板 B（token 不带 Bearer，需要手动补）：

```text
content-type    application/json;charset=UTF-8
Accept          application/json
Authorization   Bearer ${__P(token,NOT_FOUND)}
```

怎么判断用 A 还是 B：

- 登录响应里如果是 `Bearer eyJ...`，用模板 A。
- 登录响应里如果只是 `eyJ...`，用模板 B。

补充：`__P` 和 `__property` 都能取属性，初学建议统一用 `__P`，更短更直观。

注意：

```text
Content-Type 要和请求体格式一致。
```

如果你发送 JSON，但 Content-Type 写错，后端可能无法解析。

---

## 18. 常见错误排查清单

### 18.1 token 没有带上

检查：

```text
1. 登录接口是否成功
2. JSON 提取器 JSONPath 是否正确
3. Default Values 是否显示 NOT_FOUND
4. 后置处理器是否把 token 存入 props
5. 属性显示中 token 是否是真实 token
6. 后续请求头 Authorization 是否写对
7. 是否重复写了 Bearer
8. 线程组是否按顺序执行
```

### 18.2 JSON 提取器提取不到

检查：

```text
1. Apply to 是否选择 Main sample only
2. JSONPath 是否和响应结构一致
3. Match No. 是否填 1
4. Default Values 是否填 NOT_FOUND
5. 登录响应中是否真的有 data.token
```

如果响应是：

```json
{
  "data": {
    "token": "Bearer xxx"
  }
}
```

JSONPath 应该是：

```text
$.data.token
```

如果响应是：

```json
{
  "token": "Bearer xxx"
}
```

JSONPath 应该是：

```text
$.token
```

### 18.3 JSON 断言没有失败

如果你希望判断：

```text
msg 必须等于 创建成功
```

但返回其他 msg 也通过了，通常是因为没有勾选：

```text
Additionally assert value
```

正确配置：

```text
Assert JSON Path exists: $.meta.msg
勾选 Additionally assert value
Expected Value: 创建成功
```

### 18.4 JDBC 查询变量取不到

检查：

```text
1. JDBC Connection Configuration 的变量名是否和 JDBC 请求里一致
2. SQL 是否能查出结果
3. Variable names 是否写了 rid
4. 使用时是否写 ${rid_1}，而不是 ${rid}
5. JDBC 预处理程序是否放在 HTTP 请求下面
```

---

## 19. 推荐的接口测试结构示例

### 19.1 登录后跨线程组使用 token

```text
测试计划
  HTTP 请求默认值
  HTTP 信息头管理器
  察看结果树

  setUp Thread Group
    登录 1.2.1
      JSON 提取器：提取 token
      JSR223 后置处理程序：props.put("token", vars.get("token"))
      JSON 断言：$.meta.msg = 登录成功

  线程组
    用户数据列表 1.3.1
      HTTP 信息头管理器：Authorization = ${__P(token,NOT_FOUND)}
      JSON 断言

    添加用户 1.3.2
      HTTP 信息头管理器：Authorization = ${__P(token,NOT_FOUND)}
      JSON 断言：$.meta.msg = 创建成功
      JSON 提取器：提取 userId

    修改用户状态 1.3.3
      HTTP 信息头管理器：Authorization = ${__P(token,NOT_FOUND)}
      使用 ${userId}
      JSON 断言
```

### 19.2 分配角色时结合 JDBC

```text
分配用户角色 1.3.7
  JDBC 预处理程序
    SQL: select role_id from sp_role order by role_id limit 1;
    Variable names: rid

  HTTP 请求
    PUT ${url}/users/${uid}/role
    参数 rid = ${rid_1}

  JSON 断言
    $.meta.msg = 设置角色成功
```

---

## 20. 新手记忆口诀

```text
JSON 断言：判断返回对不对
JSON 提取器：提取返回里的值给后面用
同线程组：直接用 ${变量名}
跨线程组：先 props.put，再用 ${__P(变量名,默认值)}
Authorization：看 token 是否自带 Bearer
JDBC 查询：Variable names 写 rid，使用 ${rid_1}
断言具体值：必须勾选 Additionally assert value
JSON 提取响应体：Apply to 选 Main sample only
```

---

## 21. 你当前最需要掌握的核心点

你现在作为 JMeter 新手，优先掌握这几件事就够了：

1. 会创建线程组和 HTTP 请求
2. 会设置 HTTP 请求默认值
3. 会设置 HTTP 信息头管理器
4. 会用 JSON 断言判断接口是否成功
5. 会用 JSON 提取器提取 token、id 等字段
6. 会理解同线程组变量 `${token}` 和跨线程组 property `${__P(token,NOT_FOUND)}` 的区别
7. 会用 Debug Sampler 或属性显示检查变量值
8. 会用 JDBC 预处理程序从数据库取数据
9. 会根据察看结果树定位失败原因

---

## 22. 一句话总结

JMeter 接口测试的核心不是点按钮，而是理解这条链路：

```text
发请求
  ↓
拿响应
  ↓
断言响应是否正确
  ↓
提取关键字段
  ↓
把字段传给后续接口
  ↓
多个接口串成完整业务流程
```

只要你掌握了：

```text
JSON 断言 + JSON 提取器 + 请求头 token + 变量作用域 + JDBC 取数
```

就已经进入接口自动化测试的核心区域了。
## 图谱关联

- 主题入口：[[04_接口测试MOC]]
- 对应作业：[[第七天作业_接口测试]]
- 对应笔记：[[接口测试]]
- 对应面试题：[[4.接口测试_面试题]]
- 项目实战：[[wms项目]]
- 关联数据库：[[第六天作业_MySQL_接口]]、[[数据库]]
- 总览入口：[[00_测试开发总览MOC]]
