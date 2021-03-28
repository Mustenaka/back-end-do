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
import random

import models.DBconnect as DBconnect
import models.testDB as testDB

import control.OPcontrol as OPcontrol
import routes.config as config
import Log.logutil2 as log
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


@app.route('/')
def index():
    """
    根目录-首页，index.html页面，目前只有一个hello world做返回
    """
    # 首页
    return "hello world"



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
            "info":'Logged in as %s' % escape(session['user_id'])
        })
        #return 'Logged in as %s' % escape(session['user_id'])
    #return 'You are not logged in'
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
    登陆,验证传入
    API: http://localhost/login

    Args:
        user_name - 用户登陆ID
        user_pwd - 用户登陆密码

    Returns:
        返回用户id，是否是管理员，以及成功码
    """
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
                    "error": config.errorCode[2],
                    "error_info": config.errorCodeinfo[2]
                })
            elif retrunDic['returnCode'] == "a0":
                # 登陆成功 - 添加进入session
                session["user_id"] = user_id
                # 返回正确代码和信息
                return jsonify({
                    "user_id": user_id,
                    "user_wx_id":user_wx_id,
                    "success": config.successCode[0],
                    "success_info": config.successCodeinfo[0]
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



# 登出
@app.route('/logout', methods=['GET', 'POST'])
def Logout_():
    """
    登出，冷门API

    Args:
        user_id 用户ID
    """
    if request.method == 'POST':
        try:
            # 登出主要是为了删除session
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
    else :
        return jsonify({
            "error": config.errorCode[0],
            "error_info": config.errorCodeinfo[0]
        })



# 注册 - 待重写
@app.route('/register', methods=['GET', 'POST'])
def Register_():
    """
    登陆, 注册，需要输入 通过输入的用户名密码生成一个唯一的user_id
    API: http://localhost/login

    Args:
        user_name - 用户登陆ID
        user_pwd - 用户登陆密码

    Returns:
        改用户在user_info表中全部的信息
    """
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
                        "user_rightAnswer":retrunDic['user_rightAnswer'],
                        "user_wrongAnswer":retrunDic['user_wrongAnswer'],
                        "success": config.successCode[2],
                        "success_info": config.successCodeinfo[2]
                    })
            elif retrunDic['returnCode'] == "r0":
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



@app.route('/getChaptersall', methods=['GET', 'POST'])
def get_chapter():
    """
    获取全部章节信息（不常用API - 测试用） 
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
        get_dic = op.get_chapter_all()
        get_dic.setdefault("success", config.successCode[5])
        get_dic.setdefault("success_info", config.successCodeinfo[5])
        print(get_dic)
        return jsonify(get_dic)
        #return jsonify(json.dumps(get_dic,f, indent = 4, separators = (',', ': ')))
    except:
        return jsonify({
            "error": config.errorCode[1],
            "error_info": config.errorCodeinfo[1]
        })


  
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
        subject_id

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
            chp_id = str(request.json.get('subject_id'))
            # 验证账户密码正确性
            op = OPcontrol.OPcontrol()
            get_dic = op.get_chapter(chp_id)
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
            tit_id = random.randint(1,table_length-1)

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

            isRight = op.answerCorrectJudgment(user_id,tit_id,answer,user_note)
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
    """
    pass



if __name__ == '__main__':
    # 启动Flask服务
    app.run(debug=True, host='127.0.0.1', port=5000)  # 内部测试
    # app.run(debug=False, host='0.0.0.0', port=80)  # 外部访问
