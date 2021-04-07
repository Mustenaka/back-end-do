from flask import Flask
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask_cors import CORS

import os
import sys
import json
import random

import models.DBconnect as DBconnect
import models.testDB as testDB

import control.OPcontrol as OPcontrol
import routes.config as config
import Log.logutil2 as log
from control.Msession import MySessionInterface

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['JSON_SORT_KEYS'] = False

# session
# 随机生成SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)

# 启动日志服务
logger = log.logs()
'''
# 强制 指定session时间，如果不指定则关闭浏览器自动清除
session.permanent = True
# session 删除时间 15 mins
app.permanent_session_lifetime = timedelta(minutes = 15) 
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    根目录-首页，无论任何方法都可以返回一个英文的测试json
    """
    # 首页
    return jsonify({
        "index": "There is no index page, just the json."
    })


# 检查登陆状态
@app.route('/checklogin', methods=['GET', 'POST'])
def check_login():
    """
    验证登陆状态
    API: http://localhost/checklogin

    Args:
        user_id  用户ID

    Returns:
        错误返回错误码，成功返回登陆情况
    """
    if 'user_id' in session:
        return jsonify({
            "success": config.successCode[3],
            "success_info": config.successCodeinfo[3],
            "info": 'Logged in as %s' % escape(session['user_id'])
        })
        # return 'Logged in as %s' % escape(session['user_id'])
    # return 'You are not logged in'
    return jsonify({
        "error": config.errorCode[4],
        "error_info": config.errorCodeinfo[4]
    })


# 彩蛋
@app.route('/Easter_eggs', methods=['GET', 'POST'])
def miaozi_hello():
    """
    彩蛋页面，用来验证传输的是否是UTF-8
    """
    miaozi = "年轻人恭喜你发现这个彩蛋，喵子是最可爱的人，不是么？"
    return jsonify({
        "Easter_eggs": miaozi
    })


# 登陆 - 待重写
@app.route('/login', methods=['GET', 'POST'])
def Login_():
    """
    登陆, 验证传入的用户名和密码是否在数据库中匹配
    API: http://localhost/login

    Args:
        user_name - 用户名
        user_pwd - 用户登陆密码

    Returns:
        返回用户id，用户名，是否是管理员，以及成功码
    """
    if request.method == 'POST':
        try:
            # 获取用户名密码
            user_name = str(request.json.get('user_name'))
            user_pwd = str(request.json.get('user_pwd'))
            logger.debug("login - "+user_name+" and "+user_pwd)
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            returnDic = op.check_login(user_name, user_pwd)

            # 判断登陆是否成功 - r0 登陆失败 , a0 登陆成功
            if returnDic['returnCode'] == "r0":
                # 登陆失败，抛出错误代码
                return jsonify({
                    "error": config.errorCode[2],
                    "error_info": config.errorCodeinfo[2]
                })
            elif returnDic['returnCode'] == "a0":
                # 获取该用户的用户id 以及 用户名
                user_id = returnDic['user_id']
                user_name = returnDic['user_name']
                user_rightAnswer = returnDic['user_rightAnswer']
                user_wrongAnswer = returnDic['user_wrongAnswer']
                isAdministrator = returnDic['isAdministrator']

                # 登陆成功 - 将user_id 添加进入session
                session["user_id"] = user_id

                # 返回正确代码和信息
                return jsonify({
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_rightAnswer": user_rightAnswer,
                    "user_wrongAnswer": user_wrongAnswer,
                    "isAdministrator": isAdministrator,
                    "success": config.successCode[0],
                    "success_info": config.successCodeinfo[0]
                })
        except IOError as exc:
            logger.error(exc)
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 登出
@app.route('/logout', methods=['GET', 'POST'])
def Logout_():
    """
    登出，冷门API, 登出主要是为了删除session

    Args:
        user_id 用户ID
    """
    if request.method == 'POST':
        try:
            # 获取user_id
            user_id = str(request.json.get('user_id'))
            print(user_id)
            session.pop('user_id', None)
            #print(session.get('user_id'), session.pop('user_id', None))
            return jsonify({
                "user_id": user_id,
                "success": config.successCode[1],
                "success_info": config.successCodeinfo[1]
            })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 注册
@app.route('/register', methods=['GET', 'POST'])
def Register_():
    """
    登陆, 注册，需要输入 通过输入的用户名密码生成一个唯一的user_id
    并且返回这些基本信息
    API: http://localhost/login

    Args:
        user_name - 用户登陆ID
        user_pwd - 用户登陆密码

    Returns:
        改用户在user_info表中全部的信息
    """
    if request.method == 'POST':
        try:
            # 传递进来用户名和密码
            user_name = str(request.json.get('user_name'))
            user_pwd = str(request.json.get('user_pwd'))

            op = OPcontrol.OPcontrol()
            returnDic = op.register(user_name, user_pwd)
            if returnDic['returnCode'] == "a0":
                return jsonify({
                    "user_id": returnDic['user_id'],
                    "user_name": returnDic['user_name'],
                    "user_pwd": returnDic['user_pwd'],
                    "user_wx_id": returnDic['user_wx_id'],
                    "user_rightAnswer": returnDic['user_rightAnswer'],
                    "user_wrongAnswer": returnDic['user_wrongAnswer'],
                    "isAdministrator": returnDic['isAdministrator'],
                    "success": config.successCode[2],
                    "success_info": config.successCodeinfo[2]
                })
            elif returnDic['returnCode'] == "r0":
                return jsonify({
                    "error": config.errorCode[3],
                    "error_info": config.errorCodeinfo[3]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


##################################################
##################################################
##################-后台API-#######################
##################################################
##################################################
##################################################


# 获取全部章节
@app.route('/getChaptersall', methods=['GET', 'POST'])
def get_chapter_all():
    """
    获取全部章节信息，管理员查询用API
    API: http://localhost/getChaptersall

    Returns:
        返回数据库中全部的章节信息
    
    Update:
        前端使用cookie，后端取消session验证

    """
    # GET请求 和 POST请求都可以
    try:
        # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
        op = OPcontrol.OPcontrol()
        get_dic = op.get_chapter_all()
        get_dic.setdefault("success", config.successCode[5])
        get_dic.setdefault("success_info", config.successCodeinfo[5])
        print(get_dic)
        return jsonify(get_dic)
        # return jsonify(json.dumps(get_dic,f, indent = 4, separators = (',', ': ')))
    except:
        return jsonify({
            "error": config.errorCode[1],
            "error_info": config.errorCodeinfo[1]
        })


# 获取全部题目
@app.route('/getTitlesall', methods=['GET', 'POST'])
def get_title_all():
    """
    获取全部题目信息，管理员查询用api
    API: http://localhost/getTitlesall

    Returns:
        返回数据库中全部的题目信息
    
    Update:
        前端使用cookie，后端取消session验证
    """
    # GET请求 和 POST请求都可以
    try:
        # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
        op = OPcontrol.OPcontrol()
        get_dic = op.get_title_all()
        get_dic.setdefault("success", config.successCode[6])
        get_dic.setdefault("success_info", config.successCodeinfo[6])
        print(get_dic)
        return jsonify(get_dic)
        # return jsonify(json.dumps(get_dic,f, indent = 4, separators = (',', ': ')))
    except:
        return jsonify({
            "error": config.errorCode[1],
            "error_info": config.errorCodeinfo[1]
        })




# 提交新章节API
@app.route('/setnewchapter', methods=['GET', 'POST'])
def set_new_chapter():
    """
    新增一个章节，管理员才能使用的API。
    首先进行是否登录验证，管理员身份验证，其次进行传入信息完整性验证，随后传递给OPcontrol层进行操作
    API: http://localhost/setnewchapter

    Args:
        user_id        # 用户ID
        chapters_id    # 章节ID
        subject_id     # 科目ID
        chapters_name  # 章节介绍


    Returns:
        成功上传；
        失败上传
            原因1.章节ID提交重复
            原因2.缺少内容
            原因3.使用GET请求
            原因4.传输过程有误
    
    Update:
        前端使用cookie，后端取消session验证

    """
    if request.method == 'POST':
        try:
            # 输入筛查
            user_id = str(request.json.get('user_id'))
            subject_id = str(request.json.get('subject_id'))
            chapters_id = str(request.json.get('chapters_id'))
            chapters_name = str(request.json.get('chapters_name'))

            li = [user_id, subject_id, chapters_id, chapters_name]
            if None in li:
                return jsonify({
                    "error": config.errorCode[5],
                    "error_info": config.errorCodeinfo[5]
                })

            op = OPcontrol.OPcontrol()

            # 验证该账户是否是管理员账户
            is_administrator = op.check_administrator(user_id)
            print(is_administrator)
            if is_administrator == False:
                return jsonify({
                    "error": config.errorCode[6],
                    "error_info": config.errorCodeinfo[6]
                })

            # 传递全部参数进行插入
            is_insert_successful = op.insert_new_chapter(
                 chapters_id, subject_id, chapters_name)
            print("insert or update new chapter")
            if is_insert_successful:
                return jsonify({
                    "success": config.successCode[11],
                    "success_info": config.successCodeinfo[11]
                })
            else:
                return jsonify({
                    "error": config.errorCode[8],
                    "error_info": config.errorCodeinfo[8]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 提交新题目API
@app.route('/setnewtitle', methods=['GET', 'POST'])
def set_new_title():
    """
    新增一个题目，管理员才能使用的API。
    首先进行是否登录验证，管理员身份验证，其次进行传入信息完整性验证，随后传递给OPcontrol层进行操作
    API: http://localhost/setnewtitle

    Args:
        user_id        # 用户ID
        title_id       # 题目ID
        chapters_id    # 章节ID
        titleHead      # 题目标题
        titleCont      # 题目内容
        titleAnswer    # 题目答案
        titleAnalysis  # 题目分析
        titlespaper    # 题目出处
        specialNote    # 特殊注解

    Returns:
        成功上传；
        失败上传
            原因1.题目ID提交重复
            原因2.缺少内容
            原因3.使用GET请求
            原因4.传输过程有误
    
    Update:
        前端使用cookie，后端取消session验证

    """
    if request.method == 'POST':
        try:
            # 输入筛查
            user_id = str(request.json.get('user_id'))
            title_id = str(request.json.get('title_id'))
            chapters_id = str(request.json.get('chapters_id'))
            titleHead = str(request.json.get('titleHead'))
            titleCont = str(request.json.get('titleCont'))
            titleAnswer = str(request.json.get('titleAnswer'))
            titleAnalysis = str(request.json.get('titleAnalysis'))
            titlespaper = str(request.json.get('titlespaper'))
            specialNote = str(request.json.get('specialNote'))

            li = [user_id, title_id, chapters_id, titleHead, titleCont,
                  titleAnswer, titleAnalysis, titlespaper, specialNote]
            if None in li:
                return jsonify({
                    "error": config.errorCode[5],
                    "error_info": config.errorCodeinfo[5]
                })

            op = OPcontrol.OPcontrol()

            # 验证该账户是否是管理员账户
            is_administrator = op.check_administrator(user_id)
            if is_administrator == False:
                return jsonify({
                    "error": config.errorCode[6],
                    "error_info": config.errorCodeinfo[6]
                })

            # 传递全部参数进行插入
            is_insert_successful = op.insert_new_title(li)
            if is_insert_successful:
                return jsonify({
                    "success": config.successCode[10],
                    "success_info": config.successCodeinfo[10]
                })
            else:
                return jsonify({
                    "error": config.errorCode[7],
                    "error_info": config.errorCodeinfo[7]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 修改题目API
@app.route('/updatetitle', methods=['GET', 'POST'])
def update_title():
    """
    修改一个已经存在的题目，管理员才能使用的API。
    首先进行是否登录验证，管理员身份验证，其次进行传入信息完整性验证，随后传递给OPcontrol层进行操作
    API: http://localhost/updatetitle

    Args:
        user_id        # 用户ID
        title_id       # 题目ID
        chapters_id    # 章节ID
        titleHead      # 题目标题
        titleCont      # 题目内容
        titleAnswer    # 题目答案
        titleAnalysis  # 题目分析
        titlespaper    # 题目出处
        specialNote    # 特殊注解

    Returns:
        成功上传；
        失败上传
            原因1.题目ID提交重复
            原因2.缺少内容
            原因3.使用GET请求
            原因4.传输过程有误

    Update:
        前端使用cookie，后端取消session验证
    """
    if request.method == 'POST':
        try:
            # 输入筛查
            user_id = str(request.json.get('user_id'))
            title_id = str(request.json.get('title_id'))
            chapters_id = str(request.json.get('chapters_id'))
            titleHead = str(request.json.get('titleHead'))
            titleCont = str(request.json.get('titleCont'))
            titleAnswer = str(request.json.get('titleAnswer'))
            titleAnalysis = str(request.json.get('titleAnalysis'))
            titlespaper = str(request.json.get('titlespaper'))
            specialNote = str(request.json.get('specialNote'))

            li = [user_id, title_id, chapters_id, titleHead, titleCont,
                  titleAnswer, titleAnalysis, titlespaper, specialNote]
            if None in li:
                return jsonify({
                    "error": config.errorCode[5],
                    "error_info": config.errorCodeinfo[5]
                })

            op = OPcontrol.OPcontrol()

            # 验证该账户是否是管理员账户
            is_administrator = op.check_administrator(user_id)
            if is_administrator == False:
                return jsonify({
                    "error": config.errorCode[6],
                    "error_info": config.errorCodeinfo[6]
                })

            # 传递全部参数进行插入
            is_update_successful = op.update_title(li)
            if is_update_successful:
                return jsonify({
                    "success": config.successCode[10],
                    "success_info": config.successCodeinfo[10]
                })
            else:
                return jsonify({
                    "error": config.errorCode[7],
                    "error_info": config.errorCodeinfo[7]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })



# 删除题目API
@app.route('/removetitle', methods=['GET', 'POST'])
def remove_title():
    """
    删除一个已经存在的题目，管理员才能使用的API。
    首先进行是否登录验证，管理员身份验证，其次进行传入信息完整性验证，随后传递给OPcontrol层进行操作
    API: http://localhost/updatetitle

    Args:
        user_id        # 用户ID
        title_id       # 题目ID

    Returns:
        成功上传；
        失败上传
            原因1.题目ID提交重复
            原因2.缺少内容
            原因3.使用GET请求
            原因4.传输过程有误

    Update:
        前端使用cookie，后端取消session验证
    """
    if request.method == 'POST':
        try:
            # 输入筛查
            user_id = str(request.json.get('user_id'))
            title_id = str(request.json.get('title_id'))

            op = OPcontrol.OPcontrol()

            # 验证该账户是否是管理员账户
            is_administrator = op.check_administrator(user_id)
            if is_administrator == False:
                return jsonify({
                    "error": config.errorCode[6],
                    "error_info": config.errorCodeinfo[6]
                })

            # 传递全部参数进行插入
            is_update_successful = op.remove_title(title_id)
            print("-----------------")
            if is_update_successful:
                return jsonify({
                    "success": config.successCode[12],
                    "success_info": config.successCodeinfo[12]
                })
            else:
                return jsonify({
                    "error": config.errorCode[9],
                    "error_info": config.errorCodeinfo[9]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 删除章节API
@app.route('/removechapter', methods=['GET', 'POST'])
def remove_chapter():
    """
    删除一个已经存在的题目，管理员才能使用的API。
    首先进行是否登录验证，管理员身份验证，其次进行传入信息完整性验证，随后传递给OPcontrol层进行操作
    API: http://localhost/updatetitle

    Args:
        user_id             # 用户ID
        chapters_id       # 章节ID

    Returns:
        成功上传；
        失败上传
            原因1.题目ID提交重复
            原因2.缺少内容
            原因3.使用GET请求
            原因4.传输过程有误

    Update:
        前端使用cookie，后端取消session验证
    """
    if request.method == 'POST':
        try:
            # 输入筛查
            user_id = str(request.json.get('user_id'))
            chapters_id = str(request.json.get('chapters_id'))

            op = OPcontrol.OPcontrol()

            # 验证该账户是否是管理员账户
            is_administrator = op.check_administrator(user_id)
            if is_administrator == False:
                return jsonify({
                    "error": config.errorCode[6],
                    "error_info": config.errorCodeinfo[6]
                })

            # 传递全部参数进行插入
            is_update_successful = op.remove_chapter(chapters_id)
            if is_update_successful:
                return jsonify({
                    "success": config.successCode[13],
                    "success_info": config.successCodeinfo[13]
                })
            else:
                return jsonify({
                    "error": config.errorCode[10],
                    "error_info": config.errorCodeinfo[10]
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })

##################################################
##################################################
##################################################
##################################################
##################################################
##################################################


# 获取全部科目信息
@app.route('/getsubject', methods=['GET', 'POST'])
def get_subject():
    """
    获取全部科目信息，408科目中一共有四个科目，分别是《数据结构》《计算机网络》《计算机操作系统》《计算机组成原理》
    API: http://localhost/getsubject

    Returns:
        科目ID，科目名称，科目简介
    """
    # GET请求 和 POST请求都可以
    try:
        # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
        user = session.get('user_id')
        if not user:
            return jsonify({
                "error": config.errorCode[4],
                "error_info": config.errorCodeinfo[4]
            })
        op = OPcontrol.OPcontrol()
        get_dic = op.get_subject()
        get_dic.setdefault("success", config.successCode[4])
        get_dic.setdefault("success_info", config.successCodeinfo[4])
        print(get_dic)
        return jsonify(get_dic)
    except:
        return jsonify({
            "error": config.errorCode[1],
            "error_info": config.errorCodeinfo[1]
        })


# 查询章节信息
@app.route('/getchapterfromsub', methods=['GET', 'POST'])
def get_chapters_from_sub():
    """
    通过json传入科目ID，获取该科目ID下的全部章节
    API: http://localhost/getchapterfromsub

    Args:
        subject_id 科目ID

    Returns:
        科目ID，章节ID，章节名称

    """
    if request.method == 'POST':
        try:
            # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
            user = session.get('user_id')
            if not user:
                return jsonify({
                    "error": config.errorCode[4],
                    "error_info": config.errorCodeinfo[4]
                })
            # 输入筛查
            sub_id = str(request.json.get('subject_id'))
            if sub_id == "":
                raise NameError("notInput")

            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_chapter(sub_id)
            get_dic.setdefault("success", config.successCode[5])
            get_dic.setdefault("success_info", config.successCodeinfo[5])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 查询题目信息
@app.route('/gettitlefromchp', methods=['GET', 'POST'])
def get_title_from_chp():
    """
    通过json传入章节ID，获取该科目ID下的全部题目ID
    API: http://localhost/gettitlefromchp

    Args:
        chapters_id

    Returns:
        章节ID，题目ID

    """
    if request.method == 'POST':
        try:
            # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
            user = session.get('user_id')
            if not user:
                return jsonify({
                    "error": config.errorCode[4],
                    "error_info": config.errorCodeinfo[4]
                })
            # 输入筛查
            chp_id = str(request.json.get('chapters_id'))
            if chp_id == "":
                raise NameError("notInput")
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_title(chp_id)
            get_dic.setdefault("success", config.successCode[6])
            get_dic.setdefault("success_info", config.successCodeinfo[6])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })

    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 获取题目详细信息
@app.route('/gettitleinfo', methods=['GET', 'POST'])
def get_titleInfo():
    """
    根据题目ID获取题目详细信息，包括题目描述，正确答案，相关的解析等内容
    API：http://localhost/gettitleinfo

    Args:
        title_id 题目ID

    Returns:
        title_id:   输入的题目ID 
        titleHead:   题目的标题
        titleCont:  题目的内容
        titleAnswer:    题目的答案（选择填空混合）
        titleAnalysis:  题目的解析
        titleAveracc:   题目的平均正确率
        titlespaper:    题目来自的试卷
        specialNote:    特殊注解（一般没有为None）

    """
    if request.method == 'POST':
        try:
            # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
            user = session.get('user_id')
            if not user:
                return jsonify({
                    "error": config.errorCode[4],
                    "error_info": config.errorCodeinfo[4]
                })
            # 输入筛查
            tit_id = str(request.json.get('title_id'))
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_title_info(tit_id)
            get_dic.setdefault("success", config.successCode[6])
            get_dic.setdefault("success_info", config.successCodeinfo[6])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 同上，随机获取题目信息
@app.route('/getrandomtitleinfo', methods=['GET', 'POST'])
def get_randomTitleInfo():
    """
    同上，无需传入任何参数，直接获取题目信息
    API：http://localhost/getrandomtitleinfo
    """
    if request.method == 'POST':
        try:
            # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
            user = session.get('user_id')
            if not user:
                return jsonify({
                    "error": config.errorCode[4],
                    "error_info": config.errorCodeinfo[4]
                })

            # 验证账户密码正确性 - 先获取长度，再随机生成
            op = OPcontrol.OPcontrol()
            table_length = op.get_title_len()
            tit_id = random.randint(1, table_length-1)

            get_dic = op.get_title_info(str(tit_id))
            get_dic.setdefault("success", config.successCode[6])
            get_dic.setdefault("success_info", config.successCodeinfo[6])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 提交答案
@app.route('/submitanswer', methods=['GET', 'POST'])
def submit_answer():
    """
    提交题目的回答
    API：http://localhost/submitanswer

    Args:
        title_id 题目ID
        user_id 用户ID
        answer 用户回答
        user_note 用户注解

    Returns:
        title_id:   输入的题目ID 
        titleHead:   题目的标题
        titleCont:  题目的内容
        titleAnswer:    题目的答案（选择填空混合）
        titleAnalysis:  题目的解析
        titleAveracc:   题目的平均正确率
        titlespaper:    题目来自的试卷
        specialNote:    特殊注解（一般没有为None）

    """
    if request.method == 'POST':
        try:
            # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
            user = session.get('user_id')
            if not user:
                return jsonify({
                    "error": config.errorCode[4],
                    "error_info": config.errorCodeinfo[4]
                })
            # 输入筛查
            tit_id = str(request.json.get('title_id'))
            user_id = str(request.json.get('user_id'))
            answer = str(request.json.get('answer'))
            user_note = str(request.json.get('user_note'))

            # 调用answerCorrectJudgment获取正确与否
            op = OPcontrol.OPcontrol()

            isRight = op.answerCorrectJudgment(
                user_id, tit_id, answer, user_note)
            #7 - wrong ; 8 - right
            if isRight:
                return jsonify({
                    "success": config.successCode[8],
                    "success_info": config.successCodeinfo[8],
                })
            else:
                return jsonify({
                    "success": config.successCode[7],
                    "success_info": config.successCodeinfo[7],
                })
        except:
            return jsonify({
                "error": config.errorCode[1],
                "error_info": config.errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })


# 获取个人签到信息
# 待补充
@app.route('/getpersonalsignin', methods=['GET', 'POST'])
def get_PersonalSignin(test):
    """
    代码好像不知道在哪里被give up了
    Update:
        作废此API，微信自带签到接口
    """
    pass


if __name__ == '__main__':
    # 启动Flask服务
    app.run(debug=True, host='127.0.0.1', port=5000)  # 内部测试
    # app.run(debug=False, host='0.0.0.0', port=80)  # 外部访问
