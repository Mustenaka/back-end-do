# back-end-do

这是一个我家可爱的喵子做的后端计算机复习题小程序的后端，

~~采用我也不知道什么的架构（雾）~~

主要分为【数据库操作】【控制层】【API接口】三大部分

所需第三方库：

直接输入 pip install -r requirements.txt 批量安装第三方库即可

#### 一.数据库层

文件夹 models/下

已完成，主要是 连接 + 增删改查等基本功能

#### 二.控制层

文件夹 control/下主要是OPcontrol.py文件

#### 三.API接口

本地测试:http://127.0.0.1:5000/

外网测试将127.0.0.1修改为自己的IP地址即可，传递方式统统使用json方式

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

获取章节信息：http://127.0.0.1:5000/register

说明：（前提条件 - 已登陆），获取当前数据库中存在的全部章节内容，主要有四个大模块《数据结构》，《操作系统》，《计算机组成原理》，《计算机网络》，返回三种状态码及一个中文标题，分别为章节序数以及书本从属，以及章节序和丛书合成出的一个唯一编码ID，中文就是章节名称

方法：POST，GET

正常返回：

```json
全部章节信息，
success：”4“
success_info：”success get chapter“
```

错误返回 - 会有错误代码 和 错误代码解释，主要错误来自于不登陆访问该接口

