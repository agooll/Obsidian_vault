⌕
🛒项目实战📦资料包🛠测试神器AIAI路线CV简历测评🧭入行测评🧪测开测评🎯训练营🏆案例❤赞赏我

# Linux测试环境面试题

## 一.100个高频面试Linux命令

### 1. **ls** - 列出目录内容

```text
ls-la# 列出所有文件（包括隐藏文件）的详细信息
```

### 2. **cd** - 切换目录

```text
cd /var/log  # 切换到/var/log目录
```

### 3. **pwd** - 显示当前工作目录

```text
pwd# 显示当前所在目录的完整路径
```

### 4. **cat** - 查看文件内容

```text
cat config.yml  # 查看配置文件内容
```

### 5. **grep** - 文本搜索

```text
grep-n"error" app.log  # 在日志中搜索"error"并显示行号
```

### 6. **tail** - 查看文件尾部

```text
tail-f application.log  # 实时监控日志文件变化
```

### 7. **head** - 查看文件头部

```text
head-20 app.log  # 查看日志前20行
```

### 8. **cp** - 复制文件或目录

```text
cp-r source_dir/ dest_dir/  # 递归复制目录
```

### 9. **mv** - 移动或重命名文件

```text
mv old_name.txt new_name.txt  # 重命名文件
```

### 10. **rm** - 删除文件或目录

```text
rm-rf directory/  # 强制递归删除目录
```

### 11. **mkdir** - 创建目录

```text
mkdir-p parent/child  # 创建多级目录
```

### 12. **rmdir** - 删除空目录

```text
rmdir empty_dir  # 删除空目录
```

### 13. **touch** - 创建空文件或更新文件时间戳

```text
touch new_file.txt  # 创建新文件
```

### 14. **find** - 查找文件

```text
find /home -name"*.log"# 查找所有.log文件
```

### 15. **which** - 查找命令路径

```text
which python  # 查找python命令位置
```

### 16. **whereis** - 查找命令相关文件

```text
whereisjava# 查找java相关文件
```

### 17. **locate** - 快速查找文件

```text
locate nginx.conf  # 查找nginx配置文件
```

### 18. **chmod** - 修改文件权限

```text
chmod +x script.sh  # 添加执行权限
```

### 19. **chown** - 修改文件所有者

```text
chown user:group file.txt  # 修改文件所有者和组
```

### 20. **ps** - 查看进程状态

```text
ps aux |grep nginx  # 查看nginx进程
```

### 21. **top** - 实时显示进程状态

```text
top# 查看系统进程和资源使用情况
```

### 22. **kill** - 终止进程

```text
kill-91234# 强制终止PID为1234的进程
```

### 23. **killall** - 终止同名进程

```text
killall chrome  # 终止所有chrome进程
```

### 24. **pkill** - 按模式终止进程

```text
pkill-f"python script"# 终止匹配模式的进程
```

### 25. **bg** - 将进程放到后台运行

```text
bg %1  # 将作业1放到后台运行
```

### 26. **fg** - 将进程放到前台运行

```text
fg %1  # 将作业1放到前台运行
```

### 27. **jobs** - 查看后台作业

```text
jobs# 查看当前终端后台作业
```

### 28. **nohup** - 使进程在退出终端后继续运行

```text
nohup python server.py &# 后台运行并不受终端退出影响
```

### 29. **df** - 显示磁盘空间使用情况

```text
df-h# 以易读格式显示磁盘空间
```

### 30. **du** - 显示目录空间使用情况

```text
du-sh /var/log  # 显示/var/log目录总大小
```

### 31. **free** - 显示内存使用情况

```text
free-h# 以易读格式显示内存使用
```

### 32. **uname** - 显示系统信息

```text
uname-a# 显示所有系统信息
```

### 33. **uptime** - 显示系统运行时间

```text
uptime# 显示系统运行时间和负载
```

### 34. **who** - 显示当前登录用户

```text
who# 显示当前登录用户信息
```

### 35. **w** - 显示登录用户及活动

```text
w  # 显示登录用户及其活动
```

### 36. **last** - 显示登录历史

```text
last  # 显示用户登录历史
```

### 37. **history** - 显示命令历史

```text
history# 显示命令历史记录
```

### 38. **tar** - 打包压缩文件

```text
tar-czvf archive.tar.gz directory/  # 创建gzip压缩包
```

### 39. **gzip** - 压缩文件

```text
gzip file.txt  # 压缩文件
```

### 40. **gunzip** - 解压缩文件

```text
gunzip file.txt.gz  # 解压缩文件
```

### 41. **zip** - 创建zip压缩包

```text
zip archive.zip file1.txt file2.txt  # 创建zip压缩包
```

### 42. **unzip** - 解压zip文件

```text
unzip archive.zip  # 解压zip文件
```

### 43. **ssh** - 远程登录

```text
ssh user@hostname  # 远程登录到主机
```

### 44. **scp** - 安全复制文件

```text
scp file.txt user@hostname:/path/  # 复制文件到远程主机
```

### 45. **rsync** - 远程同步文件

```text
rsync-av source/ user@hostname:destination/  # 同步文件到远程主机
```

### 46. **ping** - 测试网络连接

```text
ping example.com  # 测试与example.com的网络连接
```

### 47. **traceroute** - 显示数据包路径

```text
traceroute example.com  # 显示到example.com的网络路径
```

### 48. **netstat** - 显示网络状态

```text
netstat-tuln# 显示所有监听端口
```

### 49. **ss** - 显示套接字统计

```text
ss -tuln# 显示监听端口(比netstat更快)
```

### 50. **ifconfig** - 配置网络接口

```text
ifconfig eth0  # 显示eth0接口信息
```

### 51. **ip** - 显示/操作路由、设备等

```text
ip addr show  # 显示所有网络接口信息
```

### 52. **route** - 显示/操作IP路由表

```text
route -n# 显示路由表
```

### 53. **hostname** - 显示或设置主机名

```text
hostname# 显示当前主机名
```

### 54. **curl** - 传输数据

```text
curl-I http://example.com  # 获取HTTP头信息
```

### 55. **wget** - 下载文件

```text
wget http://example.com/file.zip  # 下载文件
```

### 56. **lynx** - 文本浏览器

```text
lynx http://example.com  # 以文本方式浏览网页
```

### 57. **telnet** - 远程登录

```text
telnet hostname22# 测试端口连通性
```

### 58. **nc** - 网络工具

```text
nc-zvhostname80# 测试端口连通性
```

### 59. **ssh-keygen** - 生成SSH密钥

```text
ssh-keygen -t rsa  # 生成RSA密钥对
```

### 60. **ssh-copy-id** - 复制SSH密钥到远程主机

```text
ssh-copy-id user@hostname  # 复制公钥到远程主机
```

### 61. **sed** - 流编辑器

```text
sed's/old/new/g' file.txt  # 替换文件中的文本
```

### 62. **awk** - 文本处理工具

```text
awk'{print $1}' file.txt  # 打印每行第一个字段
```

### 63. **cut** - 剪切文件内容

```text
cut -d: -f1 /etc/passwd  # 提取/etc/passwd中的用户名
```

### 64. **paste** - 合并文件行

```text
paste file1.txt file2.txt  # 合并两个文件的行
```

### 65. **sort** - 排序文件内容

```text
sort file.txt  # 对文件内容排序
```

### 66. **uniq** - 报告或忽略重复行

```text
uniq file.txt  # 去除重复行
```

### 67. **wc** - 统计文件内容

```text
wc-l file.txt  # 统计文件行数
```

### 68. **diff** - 比较文件差异

```text
diff file1.txt file2.txt  # 比较两个文件差异
```

### 69. **patch** - 应用补丁文件

```text
patch -p1< patchfile  # 应用补丁
```

### 70. **ln** - 创建链接

```text
ln-s /path/to/file linkname  # 创建软链接
```

### 71. **readlink** - 显示符号链接值

```text
readlink /usr/bin/python  # 显示符号链接指向的实际路径
```

### 72. **stat** - 显示文件状态

```text
stat file.txt  # 显示文件详细信息
```

### 73. **file** - 确定文件类型

```text
file document.pdf  # 确定文件类型
```

### 74. **md5sum** - 计算MD5校验和

```text
md5sum file.iso  # 计算文件MD5值
```

### 75. **sha256sum** - 计算SHA256校验和

```text
sha256sum file.iso  # 计算文件SHA256值
```

### 76. **date** - 显示或设置系统日期时间

```text
date +"%Y-%m-%d %H:%M:%S"# 显示格式化日期时间
```

### 77. **cal** - 显示日历

```text
cal# 显示当月日历
```

### 78. **time** - 测量命令执行时间

```text
timels-la# 测量命令执行时间
```

### 79. **timeout** - 运行有时间限制的命令

```text
timeout 5s ping example.com  # 5秒后终止ping命令
```

### 80. **watch** - 定期执行命令

```text
watch-n1'date'# 每秒执行一次date命令
```

### 81. **at** - 定时执行任务

```text
echo"ls -la"| at midnight  # 午夜执行命令
```

### 82. **crontab** - 管理定时任务

```text
crontab-l# 列出当前用户的定时任务
```

### 83. **systemctl** - 控制系统服务

```text
systemctl status nginx  # 查看nginx服务状态
```

### 84. **service** - 运行系统服务脚本

```text
service nginx restart  # 重启nginx服务
```

### 85. **journalctl** - 查询系统日志

```text
journalctl -u nginx  # 查看nginx服务日志
```

### 86. **dmesg** - 显示内核消息

```text
dmesg|grep error  # 查找内核错误消息
```

### 87. **lsof** - 列出打开文件

```text
lsof-i :80  # 查找使用80端口的进程
```

### 88. **strace** - 跟踪系统调用

```text
strace-f python script.py  # 跟踪Python脚本的系统调用
```

### 89. **vmstat** - 显示虚拟内存统计

```text
vmstat1# 每秒显示一次虚拟内存统计
```

### 90. **iostat** - 显示CPU和I/O统计

```text
iostat -x1# 每秒显示一次扩展I/O统计
```

### 91. **mpstat** - 显示CPU统计

```text
mpstat 1# 每秒显示一次CPU统计
```

### 92. **pidstat** - 显示进程统计

```text
pidstat -u1# 每秒显示一次进程CPU使用情况
```

### 93. **sar** - 系统活动报告

```text
sar -u13# 每秒显示一次CPU使用，共3次
```

### 94. **ulimit** - 控制shell资源

```text
ulimit-a# 显示所有资源限制
```

### 95. **env** - 显示环境变量

```text
env# 显示所有环境变量
```

### 96. **export** - 设置环境变量

```text
exportPATH=$PATH:/new/path  # 添加新路径到PATH
```

### 97. **unset** - 删除变量或函数

```text
unset VARIABLE  # 删除环境变量
```

### 98. **alias** - 创建命令别名

```text
aliasll='ls -alF'# 创建ll别名
```

### 99. **unalias** - 删除别名

```text
unalias ll  # 删除ll别名
```

### 100. **source** - 执行脚本文件

```text
source ~/.bashrc  # 重新加载bash配置
```
