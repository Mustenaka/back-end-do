import os
import sys
projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import models.DBconnect as DBconnect

class OPcontrol:
    def __init__(self):
        pass
    
    def __del__(self):
        pass

    # 检查登陆信息 - 输入 user_id 返回user_pwd
    # 返回一个字典 - 成功登陆：
    # "user_id"
    # "user_name"
    # "user_wx_id"
    # "user_accuracy"
    # 失败登陆：
    # error : 0
    def check_login(self,user_id,user_pwd,user_wx_id):
        db = DBconnect.DBconnect()
        info = db.dbQuery_userLogin(user_id,user_pwd)
        if info == None:
            dic = {"returnCode":"r0"}
        else:
            dic = {
                "returnCode":"a0",
                "user_id":info[0],
                "user_name":info[1],
                "user_wx_id":info[3],
                "user_accuracy":info[4]
            }
        print(dic)
        return dic



if __name__ == '__main__':
    op = OPcontrol()
    op.check_login("1001","123123","momotou1")
