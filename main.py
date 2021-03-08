from flask import Flask
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask import escape

import os
import sys
import json

import models.DBconnect as DBconnect
import models.testDB as testDB

import control.OPcontrol as OPcontrol
from control.Msession import MySessionInterface

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# session
# 随机生成SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)

'''
# 强制 指定session时间，如果不指定则关闭浏览器自动清除
session.permanent = True
# session 删除时间 15 mins
app.permanent_session_lifetime = timedelta(minutes = 15) 
'''

# 错误报错内部传递参数，作为响应数组
errorCode = [
    "0",
    "1",
    "2",
    "3",
    "4",
]
# 详细错误信息
errorCodeinfo = [
    "You should use POST",
    "Can not get information, please recheck the input",
    "Wrong password or something else",
    "can not register new account, please recheck.",
    "You are not login in"
]

# 成功代码
successCode = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
]

# 成功详细信息
successCodeinfo = [
    "success login",
    "success log out",
    "success register new account",
    "You are already login in.",
    "success get subject",
    "success get chapter",
    "success get title",
]

# 根目录，还没有想好放什么
@app.route('/')
def index():
    # 首页
    return "hello world"

# 检查登陆状态
@app.route('/checklogin', methods=['GET', 'POST'])
def checklogin():
    if 'user_id' in session:
        return jsonify({
            "success": successCode[3],
            "success_info": successCodeinfo[3],
            "info":'Logged in as %s' % escape(session['user_id'])
        })
        #return 'Logged in as %s' % escape(session['user_id'])
    #return 'You are not logged in'
    return jsonify({
        "error": errorCode[4],
        "error_info": errorCodeinfo[4]
    })


# 彩蛋
@app.route('/Easter_eggs', methods=['GET', 'POST'])
def miaozi_hello():
    miaozi = "年轻人恭喜你发现这个彩蛋，喵子是最可爱的人，不是么？"
    return jsonify({
        "Easter_eggs": miaozi
    })

# 登陆
# user_id - 用户登陆ID
# user_pwd - 用户登陆密码
# user_wx_id - 用户微信pid
@app.route('/login', methods=['GET', 'POST'])
def Login_():
    if request.method == 'POST':
        try:
            user_id = str(request.json.get('user_id'))
            user_pwd = str(request.json.get('user_pwd'))
            user_wx_id = str(request.json.get('user_wx_id'))
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            retrunDic = op.check_login(user_id,user_pwd,user_wx_id)
            # 判断登陆是否成功 - r0 登陆失败 , a0 登陆成功 
            if retrunDic['returnCode'] == "r0":
                # 登陆失败，抛出错误代码
                return jsonify({
                    "error": errorCode[2],
                    "error_info": errorCodeinfo[2]
                })
            elif retrunDic['returnCode'] == "a0":
                # 登陆成功 - 添加进入session
                session["user_id"] = user_id
                # 返回正确代码和信息
                return jsonify({
                    "user_id": user_id,
                    "user_wx_id":user_wx_id,
                    "success": successCode[0],
                    "success_info": successCodeinfo[0]
                })
        except:
            return jsonify({
                "error": errorCode[1],
                "error_info": errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": errorCode[0],
            "error_info": errorCodeinfo[0]
        })

# 登出 - 直接关闭浏览器或者微信小程序断开连接也算登出了，session会自动清除的
# user_id - 用户登陆ID
@app.route('/logout', methods=['GET', 'POST'])
def Logout_():
    if request.method == 'POST':
        try:
            # 登出主要是为了删除session
            user_id = str(request.json.get('user_id'))
            print(user_id)
            session.pop('user_id', None)
            #print(session.get('user_id'), session.pop('user_id', None))
            return jsonify({
                    "user_id": user_id,
                    "success": successCode[1],
                    "success_info": successCodeinfo[1]
                })
        except:
            return jsonify({
                "error": errorCode[1],
                "error_info": errorCodeinfo[1]
            })
    else :
        return jsonify({
            "error": errorCode[0],
            "error_info": errorCodeinfo[0]
        })


# 注册
@app.route('/register', methods=['GET', 'POST'])
def Register_():
    if request.method == 'POST':
        try:
            # 登出主要是为了删除session
            user_wx_id = str(request.json.get('user_wx_id'))
            op = OPcontrol.OPcontrol()
            retrunDic = op.register(user_wx_id)
            if retrunDic['returnCode'] == "a0":
                return jsonify({
                        "user_id": retrunDic['user_id'],
                        "user_name":retrunDic['user_name'],
                        "user_pwd":retrunDic['user_pwd'],
                        "user_wx_id":retrunDic['user_wx_id'],
                        "user_accuracy":retrunDic['user_accuracy'],
                        "success": successCode[2],
                        "success_info": successCodeinfo[2]
                    })
            elif retrunDic['returnCode'] == "r0":
                return jsonify({
                        "error": errorCode[3],
                        "error_info": errorCodeinfo[3]
                    })
        except:
            return jsonify({
                "error": errorCode[1],
                "error_info": errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": errorCode[0],
            "error_info": errorCodeinfo[0]
        })

# 获取全部章节信息（不常用API - 测试用） 
@app.route('/getChaptersall', methods=['GET', 'POST'])
def get_chapter():
    # GET请求 和 POST请求都可以
    try:
        # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
        user = session.get('user_id')
        if not user:
            return jsonify({
                "error": errorCode[4],
                "error_info": errorCodeinfo[4]
            })
        op = OPcontrol.OPcontrol()
        get_dic = op.get_chapter_all()
        get_dic.setdefault("success", successCode[5])
        get_dic.setdefault("success_info", successCodeinfo[5])
        print(get_dic)
        return jsonify(get_dic)
        #return jsonify(json.dumps(get_dic,f, indent = 4, separators = (',', ': ')))
    except:
        return jsonify({
            "error": errorCode[1],
            "error_info": errorCodeinfo[1]
        })
        
# 获取全部书本（科目）信息 
@app.route('/getsubject', methods=['GET', 'POST'])
def get_subject():
    # GET请求 和 POST请求都可以
    try:
        # 需要先判断一次登陆状态 - 确保已经登陆才可以获取信息
        user = session.get('user_id')
        if not user:
            return jsonify({
                "error": errorCode[4],
                "error_info": errorCodeinfo[4]
            })
        op = OPcontrol.OPcontrol()
        get_dic = op.get_subject()
        get_dic.setdefault("success", successCode[4])
        get_dic.setdefault("success_info", successCodeinfo[4])
        print(get_dic)
        return jsonify(get_dic)
    except:
        return jsonify({
            "error": errorCode[1],
            "error_info": errorCodeinfo[1]
        })

# 查询章节信息 - 通过给定科目名称
# 输入 : subject_id - 需要查询的章节名
@app.route('/getchapterfromsub', methods=['GET', 'POST'])
def get_chapters_from_sub():
    if request.method == 'POST':
        try:
            chp_id = str(request.json.get('subject_id'))
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_chapter(chp_id)
            get_dic.setdefault("success", successCode[5])
            get_dic.setdefault("success_info", successCodeinfo[5])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": errorCode[1],
                "error_info": errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": errorCode[0],
            "error_info": errorCodeinfo[0]
        })


# 查询题目信息 - 通过给定章节名 (只显示题目号-不显示详细信息)
# 输入 : chapters_id - 需要查询的章节名
@app.route('/gettitlefromchp', methods=['GET', 'POST'])
def get_title_from_chp():
    if request.method == 'POST':
        try:
            chp_id = str(request.json.get('chapters_id'))
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_title(chp_id)
            get_dic.setdefault("success", successCode[6])
            get_dic.setdefault("success_info", successCodeinfo[6])
            print(get_dic)
            return jsonify(get_dic)
        except:
            return jsonify({
                "error": errorCode[1],
                "error_info": errorCodeinfo[1]
            })
    else:
        return jsonify({
            "error": errorCode[0],
            "error_info": errorCodeinfo[0]
        })



# 获取个人信息
@app.route('/getPersonalInfo', methods=['GET', 'POST'])
def get_PersonalInfo(test):
    pass

# 获取个人签到信息
@app.route('/getPersonalSignin', methods=['GET', 'POST'])
def get_PersonalSignin(test):
    pass



if __name__ == '__main__':
    # 启动Flask服务
    app.run(debug=False, host='127.0.0.1', port=5000)  # 内部测试
    # app.run(debug=False, host='0.0.0.0', port=5000)  # 外部访问
