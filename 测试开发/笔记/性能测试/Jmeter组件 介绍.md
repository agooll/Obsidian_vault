### Concurrency Thread Group
![](assets/Jmeter组件%20介绍/file-20260516134707388.png)
### 配置说明
Concurrency Thread Group 控制的是“并发用户数”。
Target Concurrency 决定最终并发多少人；
Ramp Up Time 决定多久升上去；
Ramp-Up Steps Count 决定分几步升上去；
Hold Target Rate Time 决定达到目标并发后保持多久。
总时间=Ramp Up Time + Hold Target Rate Time （25 + 180 = 205 秒）
![](assets/Jmeter组件/file-20260516134736108.png)

### 