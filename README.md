# back-end-do

这是一个给女朋友毕业设计的后端计算机复习题小程序的后端，Python3.5以上版本均可以使用（自己用3.7在公司测试用3.8都可以），采用API传递JSON的方式进行连接管理，用到了MYSQL，session等常用技术。

~~采用我也不知道什么的架构（雾）~~

主要的逻辑部分 分为【Model】【Controller】【API】三层

![mainBody](.\doc\pic\mainBody.png)

如何使用本项目：

1. 终端环境下首先安装第三方库pip install -r requirements.txt 
2. 导入sql文件（数据库使用mysql）
3. Windows运行run.cmd；Linux运行run.sh（Linux启动nohub会进行后台运行）

项目整体结构架构如下：

![Architecture](.\doc\pic\Architecture.png)

#### 一.Model - 数据库层

文件 models/DBconnect.py

用来与MySQL的数据库进行交互，主要利用了pymysql模块连接数据库和datetime模块记录时间，内容就是基本的增删改查

- 增加数据
- 删除数据
- 修改数据
- 查询数据
- 特殊查询数据



#### 二.Controller - 控制层

文件 control/OPcontrol.py

用来接受数据库层信息并且处理交给API接口模块，进行返回信息处理，数据库返回信息处理的中间控制层，接受传递数据，进行处理，错误排除，也是主要的逻辑管理层。

- 用户登录，注册，登出控制逻辑
- 科目，章节，题目查询控制逻辑
- 题目信息获取，提交，判断正确与否，等控制逻辑
- 章节，题目增删改查等管理端控制逻辑
- 管理端查看作答情况控制逻辑



#### 三.API - API接口层

详细API介绍可以查看doc文件中的两个API文档

文件为main.py，主要会调用启动session模块，日志模块，进行基本的route配置，进行基本的FLASK的配置选项等等配置启动，随后开始相应API访问响应。

（理论上主函数简洁一些比较好，可以考虑把route转而丢尽route文件夹中新建一个route.py这样，但不同系统之间会有一些区别，所以有的时候这样反而造成了一些路径错误出现，没有太多的时间排查就混在了一起）

【笔者自己电脑编写用Windows，有时候在公司写了一下用macOS，而该代码的生产部署又在Linux】

- 用户登录，注册，登出管理API
- 科目，章节，题目查询API
- 题目信息获取，提交API
- 章节，题目增删改查等管理API
- 管理端查看作答情况API

session技术是一个可以判断该用户是否存活的技术，一旦用户从浏览器退出了，就自动需要重新登陆）



### 四.log - 日志管理模块

文件Log/loguti2.py

主要是对Logging的再封装，调用logging，loging.handlers日志句柄，以及系统函数os和时间函数time以进行创建和写入，以及自动创建以日期为目标的日志文件，日志分为四个等级【info】【debug】【warning】【error】越后越严重，进行记录



### 五.其他文件

run.cmd / run.sh 运行文件，直接在系统中执行即可

requirements.txt 第三方库的配置安装文件

doc/ 文档文件，包含说明文档，截图，API接口介绍等等



### 附录 1 - 正确码及其含义

| successCode | 成功详细信息                         | 含义                           |
| ----------- | ------------------------------------ | ------------------------------ |
| 0           | success login                        | 成功登陆                       |
| 1           | success log out                      | 成功登出                       |
| 2           | success register new account         | 成功注册新账号                 |
| 3           | You are already login in.            | 你已经登陆了                   |
| 4           | success get subject                  | 成功获取科目                   |
| 5           | success get chapter                  | 成功获取章节                   |
| 6           | success get title                    | 成功获取题目                   |
| 7           | success, but answer is wrong         | 成功提交，但是你的回答错误了   |
| 8           | success, and answer is right         | 成功提交，并且你的回答是正确的 |
| 9           | success daily attendance             | 成功每日签到（已作废）         |
| 10          | success create or update new title   | 成功创建或者修改新的题目       |
| 11          | success create or update new chapter | 成功创建或者修改新的章节       |
| 12          | success remove title                 | 成功删除题目                   |
| 13          | success remove chapter               | 成功删除章节                   |

### 附录 2 - 错误码及其含义

| errorCode | 详细错误信息                                                 | 含义                                                         |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 0         | You should use POST                                          | 你需要使用POST（检查一下是否使用了GET）                      |
| 1         | Can not get information, please recheck the input            | 无法获取信息，错误原因很多，很有可能是传输失败了             |
| 2         | Wrong password or something else                             | 错误的用户名密码，登陆出错了                                 |
| 3         | can not register new account, please recheck.                | 你无法注册一个新账号，请重试                                 |
| 4         | You are not login in.                                        | 你还没有登陆呢                                               |
| 5         | Missing the necessary incoming parameters                    | 缺少必要的传入参数                                           |
| 6         | you are not administrator.                                   | 你不是管理员，请确认管理员账户，如果需要提升为管理员，请联系后台管理提升权限 |
| 7         | failed to insert new title. please recheck the title_id is repeated. | 失败插入新题目，请重新插入                                   |
| 8         | failed to insert new chapter. please recheck the chapters_id is repeated. | 失败插入新章节，请重新插入                                   |
| 9         | failed to remove title from title_id, plz rechack"           | 失败删除记录通过title_id，请重试                             |
| 10        | failed to remove chapter from chapters_id, plz recheck       | 失败删除记录通过chapters_id，请重试                          |