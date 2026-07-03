# 第六章 DOM（上）练习题｜含答案解析

> 复习范围：Web API、DOM 简介、获取元素、事件基础、元素内容操作、元素样式操作、元素属性操作、显示和隐藏密码案例。

---

## 一、练习题

### 1. 填空题

DOM 的中文全称是：__________。

在 DOM 中，一个页面可以看作一个 __________，页面中的标签称为 __________，页面中的所有内容都可以称为 __________。

---

### 2. 简答题

请简述 Web API 的作用是什么？并举出一个你学过的 Web API 对象。

---

### 3. 选择题

下面哪个方法是根据 **id 属性** 获取元素的？

A. `document.getElementsByClassName()`

B. `document.getElementById()`

C. `document.querySelectorAll()`

D. `document.getElementsByTagName()`

---

### 4. 判断题

`document.getElementsByTagName('li')` 返回的是一个元素集合，所以如果要操作第一个 `li`，需要通过下标访问。

对 / 错

---

### 5. 代码题

请补全下面代码，实现点击按钮后，修改 `div` 中的文本内容为“JavaScript”。

```js
var btn = document.querySelector('button');
var div = document.querySelector('div');

btn.onclick = function () {
  ________________________;
};
```

---

### 6. 简答题

事件的三要素分别是什么？请分别说明它们的含义。

---

### 7. 代码阅读题

阅读下面代码，写出点击按钮后页面会发生什么变化。

```html
<button>点击</button>
<div>原来的内容</div>

<script>
  var btn = document.querySelector('button');
  var div = document.querySelector('div');

  btn.onclick = function () {
    div.innerHTML = '<strong>新的内容</strong>';
  };
</script>
```

---

### 8. 选择题

下面哪个属性可以设置或获取元素中的 HTML 内容，并且可以识别 HTML 标签？

A. `innerText`

B. `textContent`

C. `innerHTML`

D. `className`

---

### 9. 代码题

请写出 JavaScript 代码，实现点击按钮后，把盒子的背景颜色改成红色。

```html
<button>改变颜色</button>
<div class="box">盒子</div>
```

要求使用 `style` 属性操作样式。

---

### 10. 综合题

请根据下面需求写出完整 JavaScript 代码：

页面中有一个密码输入框和一个按钮。

点击按钮时，如果密码框当前是隐藏状态，就显示密码；如果当前是显示状态，就再次隐藏密码。

```html
<input type="password" id="pwd">
<button id="btn">显示/隐藏密码</button>
```

---

# 二、答案与解析

## 1. 填空题答案

DOM 的中文全称是：**文档对象模型**。

在 DOM 中，一个页面可以看作一个 **文档**，页面中的标签称为 **元素**，页面中的所有内容都可以称为 **节点**。

### 解析

DOM 会把整个 HTML 页面看成一个树形结构。

常见的三个概念：

| 名称 | 含义 |
|---|---|
| document | 文档，一个页面就是一个文档 |
| element | 元素，页面中的标签就是元素 |
| node | 节点，页面中的所有内容都是节点 |

例如：

```html
<div>你好</div>
```

这里的 `div` 是元素，也是节点。

---

## 2. 简答题答案

Web API 是 Web 开发中用到的 API。

在 JavaScript 中，Web API 通常被封装成对象，用来帮助开发者实现某些功能。开发者不需要知道对象内部是怎么实现的，只需要知道它的属性和方法怎么用。

例如：

```js
console.log('Hello JavaScript');
```

这里的 `console` 就是一个 Web API 对象，`log()` 是它的方法，用来在控制台输出内容。

### 解析

API 可以理解成“别人提前写好的功能接口”。

我们写代码时直接调用即可。

例如：

```js
document.querySelector('div');
```

这里的 `document` 也是对象，`querySelector()` 是它的方法。

---

## 3. 选择题答案

答案：**B**

```js
document.getElementById()
```

### 解析

`getElementById()` 是根据 id 获取元素的方法。

例如：

```html
<div id="box">盒子</div>
```

```js
var box = document.getElementById('box');
```

注意：参数里面只写 id 名，不需要写 `#`。

错误写法：

```js
document.getElementById('#box');
```

正确写法：

```js
document.getElementById('box');
```

---

## 4. 判断题答案

答案：**对**

### 解析

`getElementsByTagName()` 返回的是一个元素集合，不是单个元素。

例如：

```html
<ul>
  <li>第一项</li>
  <li>第二项</li>
</ul>
```

```js
var lis = document.getElementsByTagName('li');
```

如果要操作第一个 `li`，需要写：

```js
lis[0].innerText = '修改后的第一项';
```

不能直接写：

```js
lis.innerText = '修改后的第一项';
```

因为 `lis` 是集合，不是具体某一个元素。

---

## 5. 代码题答案

```js
var btn = document.querySelector('button');
var div = document.querySelector('div');

btn.onclick = function () {
  div.innerText = 'JavaScript';
};
```

### 解析

`innerText` 是属性，不是方法。

所以应该使用赋值：

```js
div.innerText = 'JavaScript';
```

不能写成：

```js
div.innerText('JavaScript');
```

错误原因：

```js
innerText()
```

这种写法把 `innerText` 当成函数调用了，但它不是函数。

---

## 6. 简答题答案

事件的三要素是：

1. **事件源**
2. **事件类型**
3. **事件驱动程序**

### 具体含义

| 事件要素 | 含义 | 例子 |
|---|---|---|
| 事件源 | 触发事件的元素对象 | 按钮、输入框、div |
| 事件类型 | 用户发生的行为动作 | click、mouseover、blur |
| 事件驱动程序 | 事件触发后执行的代码 | 事件处理函数 |

例如：

```js
var btn = document.querySelector('button');

btn.onclick = function () {
  alert('按钮被点击了');
};
```

这里：

```js
btn
```

是事件源。

```js
onclick
```

是事件类型。

```js
function () {
  alert('按钮被点击了');
}
```

是事件驱动程序。

---

## 7. 代码阅读题答案

点击按钮后，`div` 原来的内容会变成 **加粗显示的“新的内容”**。

### 解析

原代码：

```js
div.innerHTML = '<strong>新的内容</strong>';
```

`innerHTML` 可以识别 HTML 标签。

所以 `<strong>` 标签会生效，页面显示的文字会加粗。

如果换成 `innerText`：

```js
div.innerText = '<strong>新的内容</strong>';
```

页面会原样显示：

```html
<strong>新的内容</strong>
```

不会加粗。

---

## 8. 选择题答案

答案：**C**

```js
innerHTML
```

### 解析

三个内容操作属性的区别：

| 属性 | 是否识别 HTML 标签 | 特点 |
|---|---|---|
| `innerHTML` | 识别 | 可以设置或获取 HTML 内容 |
| `innerText` | 不识别 | 只处理文本，会去除多余空格和换行 |
| `textContent` | 不识别 | 只处理文本，会保留空格和换行 |

例如：

```js
div.innerHTML = '<strong>你好</strong>';
```

页面显示加粗的“你好”。

```js
div.innerText = '<strong>你好</strong>';
```

页面原样显示 `<strong>你好</strong>`。

---

## 9. 代码题答案

```html
<button>改变颜色</button>
<div class="box">盒子</div>

<script>
  var btn = document.querySelector('button');
  var box = document.querySelector('.box');

  btn.onclick = function () {
    box.style.backgroundColor = 'red';
  };
</script>
```

### 解析

这道题的步骤：

1. 获取按钮
2. 获取盒子
3. 给按钮注册点击事件
4. 点击后修改盒子的背景颜色

核心代码：

```js
box.style.backgroundColor = 'red';
```

注意 CSS 和 JS 写法不同：

CSS 中：

```css
background-color
```

JS 中：

```js
backgroundColor
```

规律：去掉 `-`，后面的单词首字母大写。

---

## 10. 综合题答案

```html
<input type="password" id="pwd">
<button id="btn">显示/隐藏密码</button>

<script>
  var pwd = document.querySelector('#pwd');
  var btn = document.querySelector('#btn');

  btn.onclick = function () {
    if (pwd.type === 'password') {
      pwd.type = 'text';
    } else {
      pwd.type = 'password';
    }
  };
</script>
```

### 解析

密码显示与隐藏的核心是修改 `input` 的 `type` 属性。

```js
pwd.type = 'password';
```

表示密码隐藏。

```js
pwd.type = 'text';
```

表示密码显示。

判断当前状态：

```js
if (pwd.type === 'password') {
  pwd.type = 'text';
} else {
  pwd.type = 'password';
}
```

这段代码的意思是：

如果现在是密码框，就改成文本框，让密码显示出来。

否则就改回密码框，让密码隐藏起来。

---

# 三、考前重点总结

## 1. 第六章核心主线

```js
// 1. 获取元素
var element = document.querySelector('选择器');

// 2. 注册事件
element.onclick = function () {
  // 3. 操作元素内容、样式或属性
};
```

一句话记忆：

> 先获取元素，再注册事件，最后操作元素。

---

## 2. 获取元素常用方法

| 方法 | 作用 | 返回值 |
|---|---|---|
| `getElementById('id')` | 根据 id 获取元素 | 单个元素 |
| `getElementsByTagName('标签名')` | 根据标签名获取元素 | 集合 |
| `getElementsByClassName('类名')` | 根据类名获取元素 | 集合 |
| `getElementsByName('name')` | 根据 name 获取元素 | 集合 |
| `querySelector('选择器')` | 根据 CSS 选择器获取第一个元素 | 单个元素 |
| `querySelectorAll('选择器')` | 根据 CSS 选择器获取所有元素 | 集合 |

---

## 3. 内容操作

| 属性 | 作用 |
|---|---|
| `innerHTML` | 设置或获取 HTML 内容，识别标签 |
| `innerText` | 设置或获取文本内容，不识别标签 |
| `textContent` | 设置或获取文本内容，保留空格和换行 |

---

## 4. 样式操作

### style 写法

```js
element.style.backgroundColor = 'red';
element.style.fontSize = '20px';
element.style.display = 'none';
```

### className 写法

```js
element.className = 'active';
```

### classList 写法

```js
element.classList.add('active');
element.classList.remove('active');
element.classList.toggle('active');
element.classList.contains('active');
```

---

## 5. 属性操作

### 直接操作属性

```js
img.src = 'open.png';
input.type = 'text';
input.disabled = true;
```

### setAttribute / getAttribute

```js
element.setAttribute('index', '1');
element.getAttribute('index');
element.removeAttribute('index');
```

---

## 6. 最容易错的地方

### 错误 1：把属性当函数

错误：

```js
div.innerText('JavaScript');
```

正确：

```js
div.innerText = 'JavaScript';
```

---

### 错误 2：集合没有用下标

错误：

```js
var lis = document.getElementsByTagName('li');
lis.innerText = '第一项';
```

正确：

```js
var lis = document.getElementsByTagName('li');
lis[0].innerText = '第一项';
```

---

### 错误 3：CSS 属性名没有改成小驼峰

错误：

```js
box.style.background-color = 'red';
```

正确：

```js
box.style.backgroundColor = 'red';
```

---

# 四、最终记忆口诀

> DOM 第六章 = 找元素 + 绑事件 + 改内容 / 改样式 / 改属性。

