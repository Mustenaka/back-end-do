import datetime

from flask import Flask, request, jsonify

import DB.DBconnect as DBconnect

app = Flask(__name__)

# 响应数组
errorCode = [
    "operate failed", "operate successful", "An event is about to expire.",
    "Cannot add job to scheduler", "Cannot del job to scheduler", "both cannot add and del job to scheduler"
]


@app.route('/hello')
def miaozi_hello():
    return '年轻人恭喜你发现这个彩蛋，喵子是最可爱的人，不是么？'



if __name__ == '__main__':
    # 启动Flask服务
    app.run(debug=False, host='127.0.0.1', port=5000)
