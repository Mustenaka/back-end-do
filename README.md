# back-end-do

这是一个我家可爱的喵子做的后端计算机复习题小程序的后端，Python3.5以上版本均可以使用（自己用3.7在公司测试用3.8都可以）

~~采用我也不知道什么的架构（雾）~~

主要分为【数据库操作】【控制层】【API接口】三大部分

如何使用本项目：

1. 首先安装第三方库pip install -r requirements.txt 
2. 导入sql文件（数据库使用mysql）
3. python main.py运行（如果是Linux服务器需要使用nohup在后台启动程序）

项目介绍如下：

#### 一.数据库层

文件夹 models/下

已完成，主要是 连接 + 增删改查等基本功能，返回值，返回list给OPcontrol.py

#### 二.控制层

文件夹 control/下主要是OPcontrol.py文件，用来接受数据库层信息并且处理交给API接口模块

接受DBconnect.py传递进来的数据，经过处理，错误排除，返回给API模块，

#### 三.API接口

本地测试:http://127.0.0.1:5000/

外网测试将127.0.0.1地址修改为自己的IP地址即可，传递方式统统使用json方式

对下面的统一说明：sX,cX,tX分别表示 科目，章节，题目，X表示从1开始n的数量

------

登陆：http://127.0.0.1:5000/login

说明：登陆账户，会在后端生成一个session，将会使用session判断是否保持着登陆状态，注意默认方式是退出浏览器或者小程序就会清除这个session，也就需要重新登陆了，之后的所有功能相关的内容均需要使用到登陆状态判断。

方法：POST

输入json

```json
user_id - 用户登陆ID
user_pwd - 用户登陆密码
user_wx_id - 用户微信pid
```

正常返回：

```json
"user_id": user_id,
"user_wx_id":user_wx_id,
"success": "0"
"success_info": "success login"
```

错误返回 - 会有错误代码 和 错误代码解释

------

登陆检测：http://127.0.0.1:5000/checklogin

说明：判断账户是否处于已登陆状态（应该没有前端主动用到的机会，测试可以用的端口）

方法：GET，POST

正常返回：

```
"success": “3”,
"success_info": ”You are already login in.“,
"info": user_id值
```

错误返回 - 会有错误代码 和 错误代码解释

------

登出检测：http://127.0.0.1:5000/logout

说明：让账户登出，不过又session机制，这个登出应该也没啥必要，该API后端主要也就是把对应的session删除解除登陆状态了。

方法：POST

输入json

```json
user_id - 用户登陆ID
```

正常返回：

```json
"user_id": user_id,
"success": "1",
"success_info": "success log out"
```

错误返回 - 会有错误代码 和 错误代码解释

------

创建新账号：http://127.0.0.1:5000/register

说明：因为是使用微信小程序作为账户的，所以很多人喜欢更加快速的注册，因此就默认只需要输入微信账号，再由计算机自动生成user_id以及相关的密码，名称等基本信息，过后写一个修改账户信息的接口即可

默认

```json
user_id - 随机生成
user_name - 同 user_id
user_pwd - 默认123456
```

方法：POST

输入json

```json
user_wx_id - 用户微信ID
```

正常返回：

```json
"user_id": user_id, 		#随机生成的8位ID
"user_name":user_name, 		#同user_id
"user_pwd":user_pwd,		#用户密码，默认是123456
"user_wx_id":user_wx_id,	#wechat - ID
"user_accuracy":user_accuracy,	#正确率，默认是0，自动生成
"success": "2",
"success_info":"success register new account"
```

错误返回 - 会有错误代码 和 错误代码解释

------

直接获取全部章节信息（不常用API）：http://127.0.0.1:5000/getChaptersall

说明：（前提条件 - 已登陆），获取当前数据库中存在的全部章节内容，主要有四个大模块《数据结构》，《操作系统》，《计算机组成原理》，《计算机网络》，返回三种状态码及一个中文标题，分别为章节序数以及书本从属，以及章节序和丛书合成出的一个唯一编码ID，中文就是章节名称

方法：POST，GET

正常返回：

```json
全部章节信息，
success：”4“
success_info：”success get chapter“
```

例：

```json
{
    "c1": {
        "chapters_id": "1",
        "subject_id": "1",
        "chapters_name": "数据结构导论"
    },
    "c2": {
        "chapters_id": "1",
        "subject_id": "2",
        "chapters_name": "操作系统的发展史"
    },
    "c3": {
        "chapters_id": "1",
        "subject_id": "3",
        "chapters_name": "计算机网络导论"
    },
    "c4": {
        "chapters_id": "1",
        "subject_id": "4",
        "chapters_name": "计算机组成原理基础"
    },
    "success": "5",
    "success_info": "success get chapter"
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

------

获取科目信息：http://127.0.0.1:5000/getsubject

说明：返回408该考的科目，可以自行添加，但是默认就是这几个，不设定科目添加接口，返回基本上是固定值，参考”正常返回“

方法：POST，GET

正常返回：

```json
{
    "s1": {
        "subject_id": "1",
        "subject_name": "数据结构与算法",
        "subject_brief": "数据结构是计算机存储、组织数据的方式。数据结构是指相互之间存在一种或多种特定关系的数据元素的集合。通常情况下，精心选择的数据结构可以带来更高的运行或者存储效率。数据结构往往同高效的检索算法和索引技术有关。"
    },
    "s2": {
        "subject_id": "2",
        "subject_name": "操作系统",
        "subject_brief": "操作系统（operation system，简称OS）是管理计算机硬件与软件资源的计算机程序。操作系统需要处理如管理与配置内存、决定系统资源供需的优先次序、控制输入设备与输出设备、操作网络与管理文件系统等基本事务。操作系统也提供一个让用户与系统交互的操作界面。"
    },
    "s3": {
        "subject_id": "3",
        "subject_name": "计算机网络",
        "subject_brief": "计算机网络是指将地理位置不同的具有独立功能的多台计算机及其外部设备，通过通信线路连接起来，在网络操作系统，网络管理软件及网络通信协议的管理和协调下，实现资源共享和信息传递的计算机系统。"
    },
    "s4": {
        "subject_id": "4",
        "subject_name": "计算机组成原理",
        "subject_brief": "计算机组成原理介绍了计算机的基本组成原理和内部工作机制。主要内容分成两个部分：介绍计算机的基础知识；介绍计算机的各子系统（包括运算器、存储器、控制器、外部设备和输入输出子系统等）的基本组成原理、设计方法、相互关系以及各子系统互相连接构成整机系统的技术。"
    },
    "success": "4",
    "success_info": "success get subject"
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

------

获取章节信息（这才是常用API）：http://127.0.0.1:5000/getchapterfromsub

说明：输入需要访问的科目编号subject_id，返回相应的章节编号

方法：POST，GET

输入json

```
"subject_id": 1   #1处替换为subjectId号，subjectId号可以由API：getsubject获取
```

正常返回：

```
{
    "c1": {			#根据具体查询到多少题目返回诺干的cX的结构
        "chapters_id": "1",
        "subject_id": "1",
        "chapters_name": "数据结构导论"
    },
    "success": "5",
    "success_info": "success get chapter"
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

------

获取题目标题信息：http://127.0.0.1:5000/gettitlefromchp

说明：输入需要访问的章节编号chapters_id，返回相应的题目编号，注意只是返回题目编号，并不返回题目的详细信息信息，与题目信息一并返回的消息API请看后续更新

方法：POST，GET

输入json

```json
"chapters_id": 1   #输入需要查询的chapters_id，chapters_id可以由API：getchapterfromsub获取
```

正常返回：

```json
{
    "t1": {				#根据具体查询到多少题目返回诺干的tX的结构
        "title_id": "1",
        "chapters_id": "2"
    },
    "t2": {
        "title_id": "3",
        "chapters_id": "2"
    },
    "success": "6",
    "success_info": "success get title"
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

------

获取题目详细信息：http://127.0.0.1:5000/gettitleinfo

说明：输入需要访问的章节编号title_id，返回相应的题目编号的题目详细内容，返回值主要的解释为：\#  title_id:  输入的titleid 

- titleHead:  题目的标题
- titleCont: 题目的内容
- titleAnswer:  题目的答案（选择填空混合）
- titleAnalysis: 题目的解析
- titleAveracc:  题目的平均正确率
- titlespaper:  题目来自的试卷
- specialNote:  特殊注解（一般没有为None）

方法：POST

输入json

```json
"title_id": 1   #输入需要查询的title_id，title_id可以由API：gettitlefromchp获取
```

正常返回：

```json
{
    't1': {
        'title_id': '2', 
        'titleHead': '填空题',
        'titleCont': '导弹系统是属于_______系统', 
        'titleAnswer': '硬时系统', 
        'titleAnalysis': '这是一个解析', 
        'titleAveracc': '89', 
        'titlespaper': 2017, 
        'specialNote': None
    }, 
 	'success': '6', 
    'success_info': 'success get title'
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

------

随机获取题目详细信息：http://127.0.0.1:5000/gettitleinfo

说明：无需输入，直接获取一道题目（有可能是已经做过的题目），同时返回相应的题目编号的题目详细内容，内容完全同上一条API介绍

------

提交题目回答：http://127.0.0.1:5000/submitanswer

说明：输入一个题目的回答，会返回正确与否，将会在后台多个表中记录数据，以便后台访问

方法：POST

输入json

分别是title_id所需要提交题目的ID号，user_id所需要提交题目的用户，answer用户的回答（直接匹配字符串，ABCD，或者填空题答案），user_note用户自己的笔记

```json
{
    "title_id": string，
    "user_id": string，
    "answer": string，
    "user_note": string
}
```

正常返回，有两种，分别是回答正确返回代码 8，回答错误返回代码 7 ：

```json
{
	"success": successCode,
    "success_info": successCodeinfo,
}
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口