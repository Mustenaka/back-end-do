import datetime

from flask import Flask, request, jsonify

import models.DBconnect as DBconnect
import control.OPcontrol as OPcontrol

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# 错误报错内部传递参数，作为响应数组
errorCode = [
    "0",
    "1"
]
# 详细错误信息
errorCodeinfo = [
    "You should use POST",
    "Can not login in, Please recheck the information",
]

# 成功代码
successCode = [
    "0",
]

# 成功详细信息
successCodeinfo = [
    "success login",
]

# home page is nothing.
@app.route('/')
def home_page():
    pass



# 彩蛋
@app.route('/Easter_eggs')
def miaozi_hello():
    miaozi = "年轻人恭喜你发现这个彩蛋，喵子是最可爱的人，不是么？"
    return jsonify({
        "Easter_eggs": miaozi
    })

# 登陆
# user_id - 用户登陆ID
# user_pwd - 用户登陆密码
# user_wx_id - 用户微信pid
@app.route('/Login', methods=['GET', 'POST'])
def Login_(test):
    if request.method == 'POST':
        try:
            user_id = str(request.json.get('user_id'))
            user_pwd = str(request.json.get('user_pwd'))
            user_wx_id = str(request.json.get('user_wx_id'))
            # 登陆验证
            return jsonify({
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
            "error": errorCode[0]
            "error_info": errorCodeinfo[0]
        })

# 注册
@app.route('/register', methods=['GET', 'POST'])
def Register_(test):
    pass

# 获取章节
@app.route('/getChapter', methods=['GET', 'POST'])
def get_Chapter(test):
    pass

# 获取题目
@app.route('/getQuestion', methods=['GET', 'POST'])
def get_Question(test):
    pass

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
    app.run(debug=False, host='127.0.0.1', port=5000)
