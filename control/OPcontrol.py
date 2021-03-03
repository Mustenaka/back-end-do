import os
import sys
projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import models.DBconnect as DBconnect
import random

class OPcontrol:
    def __init__(self):
        # 对于数据库而言，不用长连接，怕长时间不操作还占用带宽
        pass
    
    def __del__(self):
        pass

    # 检查登陆信息 - 输入 user_id 返回user_pwd
    # 返回一个字典 - 成功登陆：
    # returnCode - a0
    # "user_id"
    # "user_name"
    # "user_wx_id"
    # "user_accuracy"
    # 失败登陆：
    # returnCode - r0
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

    # 内部函数，用来判断该用户是否已经存在
    # （即使user_id生成8位随机数，但还是不排除有可能有重复）
    # 输入 - user_id
    # 返回 False - 不重复， True - 重复
    def __is_already(self,db,user_id):
        db = DBconnect.DBconnect()
        info = db.dbQuery_user_is_already(user_id)
        if info == None:
            return False
        else:
            return True
         

    # 创建新用户 - 输入 user_wx_id 自动生成一个 8位数的 user_id 并且返回相关信息
    # 返回一个字典 - 成功登陆：
    # returnCode - a0
    # "user_id"
    # "user_name"
    # "user_pwd"
    # "user_wx_id"
    # "user_accuracy"
    # 失败登陆：
    # returnCode - r0
    def register(self,user_wx_id):
        db = DBconnect.DBconnect()
        new_user_id = str(random.randint(0,99999999)).zfill(8)
        bool_is_already = self.__is_already(db,new_user_id) 
        while bool_is_already:
            new_user_id = str(random.randint(0,99999999)).zfill(8)
            bool_is_already = self.__is_already(db,new_user_id)
        # 插入数据库
        # userName 暂时和 userId 相同，这样只是为了让微信用户快速注册
        # userPwd 暂时设置为 123456
        # 对于新用户而言 userAccuracy 为 0
        temp_pwd = "123456"
        userAccuracy = "0"
        args = (new_user_id,new_user_id,temp_pwd,user_wx_id,userAccuracy)
        is_successful = db.dbInsert("user_info",new_user_id,new_user_id,temp_pwd,user_wx_id,userAccuracy)
        if is_successful:
            dic = {
                "returnCode":"a0",
                "user_id":new_user_id,
                "user_name":new_user_id,
                "user_pwd":temp_pwd,
                "user_wx_id":user_wx_id,
                "user_accuracy":userAccuracy
            }
        else:
            dic = {
                "returnCode":"r0"
            }
        return dic
            

if __name__ == '__main__':
    op = OPcontrol()
    k = op.register("momotou5")
    print(k)
