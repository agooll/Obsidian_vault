
#### PDF
![](assets/Python笔记/Python笔记.pdf)

#### 字符串API
##### 字符串.replace("要被替换的内容", "替换成什么", 替换次数)

```Python
s = "听君一席话,如听一席话"
print(s.replace("一", "二"))  #听君二席话,如听二席话
print(s.replace("一", "二", 1))  #听君二席话,如听一席话
```

##### 字符串.count("要统计的内容", 开始下标, 结束下标)
```Python
s = "听君一席话,如听一席话"
print(s.count("一席话")) #2
print(s.count("一席话", 6, 11)) #1
```

##### 字符串.split("分隔符", maxsplit)
```python
s = "听君一席话,如听一席话"
print(s.split("一"))  # ['听君', '席话,如听', '席话']
print(s.split("一", 1)) # ['听君', '席话,如听一席话']
```
将一作为分隔符
maxsplit 最多分几次
##### startswith()：判断开头 endswith()：判断结尾
```Python
s = "听君一席话,如听一席话"​
print(s.startswith("听君")) #True​
print(s.endswith("话")) #True
```
##### **lower()：把英文字符变成小写**   **upper()：把英文字符变成大写**
```Python
s = "Hello World"​
print(s.lower()) #hello world  
print(s.upper()) #HELLO WORLD​
```
##### isalpha()判断是不是全是字母  isdigit()判断是不是全是数字  isalnum()判断是不是全是字母或数字
```Python
s1 = "helloworld"​
s2 = "123"​
s3 = "HelloWorld123"​
print(s1.isalpha()) #True​
print(s1.isdigit()) #False​
print(s1.isalnum()) #True
```

##### join()用某个“分隔符”，把一堆字符串拼接成一个新的字符串。
```Python
"分隔符".join(数据)  
```
`join()` 里面的数据必须都是**字符串**。
注意：  
`join()` 前面的那个字符串，是**用来连接数据的分隔符**。
```Python
s = "听君一席话,如听一席话"​
print("~".join(s)) # 听~君~一~席~话~,~如~听~一~席~话​
l = ["广东省", "广州市", "天河区..."]​
print("".join(l)) # 广东省广州市天河区...
print("-".join(l)) # 广东省-广州市-天河区...
```
#### 列表
列表 (List) 是 python 中使用非常频繁的数据类型, 在其他语言中通常叫做 数组
