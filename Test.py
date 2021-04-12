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

def modification_():
    # 输入筛查
    tit_id = "1"
    user_id = "1000003"
    answer = "B"
    user_note = "None"

    # 调用answerCorrectJudgment获取正确与否
    op = OPcontrol.OPcontrol()

    isRight = op.answerCorrectJudgment(
        user_id, tit_id, answer, user_note)
    #7 - wrong ; 8 - right
    if isRight:
        return {
            "success": config.successCode[8],
            "success_info": config.successCodeinfo[8],
        }
    else:
        return {
            "success": config.successCode[7],
            "success_info": config.successCodeinfo[7],
        }


if __name__ == '__main__':
    print(modification_())