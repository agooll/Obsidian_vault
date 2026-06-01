
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
print(s.startswith("听君"))​
print(s.endswith("话"))
```