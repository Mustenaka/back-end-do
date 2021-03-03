import os
import sys

import models.DBconnect as DBconnect

print(sys.path)
sys.path.append("..")

class OPcontrol:
    def __init__(self):
        pass
    
    def __del__(self):
        pass

    # 检查登陆信息
    def check_login(user_id,user_pwd,user_wx_id):
        user_id = "1001"
        user_pwd = "123123"
        user_wx_id ="momotou1" 


