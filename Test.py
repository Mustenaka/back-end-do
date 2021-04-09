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
    """
    修改用户信息
    可以修改，用户名，密码，是否提升管理员权限。

    """
    try:
        # 传递进来用户名和密码
        user_id = "28283029"
        user_name = "lyb"
        user_pwd = "123123"
        isAdministrator = ""
        print(user_id, user_name, user_pwd, isAdministrator)

        op = OPcontrol.OPcontrol()
        returnDic = op.update_user_info(user_id, user_name, user_pwd, isAdministrator)
        print(returnDic)
        if returnDic['returnCode'] == "a0":
            return {
                "user_id": returnDic['user_id'],
                "user_name": returnDic['user_name'],
                "user_pwd": returnDic['user_pwd'],
                "isAdministrator": returnDic['isAdministrator'],
                "success": config.successCode[15],
                "success_info": config.successCodeinfo[15]
            }
        elif returnDic['returnCode'] == "r0":
            return {
                "error": config.errorCode[11],
                "error_info": config.errorCodeinfo[11]
            }
    except Exception as e:
        print(e)
        return {
            "error": config.errorCode[1],
            "error_info": config.errorCodeinfo[1]
        }



if __name__ == '__main__':
    print(modification_())