import os
import sys
projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import datetime
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
                "user_rightAnswer":info[4],
                "user_wrongAnswer":info[5]
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
        # 对于新用户而言 已经回答的正确数 为 0，错误题目数也为0
        temp_pwd = "123456"
        args = (new_user_id,new_user_id,temp_pwd,user_wx_id,0,0)
        is_successful = db.dbInsert("user_info",new_user_id,new_user_id,temp_pwd,user_wx_id,0,0)
        if is_successful:
            dic = {
                "returnCode":"a0",
                "user_id":new_user_id,
                "user_name":new_user_id,
                "user_pwd":temp_pwd,
                "user_wx_id":user_wx_id,
                "user_rightAnswer":"0",
                "user_wrongAnswer":"0"
            }
        else:
            dic = {
                "returnCode":"r0"
            }
        return dic
            
            
    # 获取章节信息，返回一个字典
    # 固定设置的就是四个大模块《数据结构》，《操作系统》，《计算机组成原理》，《计算机网络》
    def get_chapter_all(self):
        dbTable = "chapters_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery(dbTable)
        dic = { }
        for i in range(0,len(info)):
            #题目编号我不希望从0开始
            pageNumber = "c" + str(i+1) 
            dic_tmp = {
                "chapters_id":info[i][0],    # 章节编号
                "subject_id":info[i][1],  # 属于哪本书的编号
                "chapters_name":info[i][2]   # 该章节中文名称
            }
            dic.setdefault(pageNumber,dic_tmp)
        return dic
        
    # 获取书本信息
    def get_subject(self):
        dbTable = "subject_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery(dbTable)
        dic = { }
        for i in range(0,len(info)):
            pageNumber = "s" + str(i+1)
            dic_tmp = {
                "subject_id":info[i][0],    # 书本<科目>编号
                "subject_name":info[i][1],  # 书本<科目>名称
                "subject_brief":info[i][2]   # 书本<科目>介绍
            }
            dic.setdefault(pageNumber,dic_tmp)
        return dic

    # 根据科目获取当前章节信息表
    def get_chapter(self,sub_id):
        dbTable = "chapters_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_chapter_according_to_subject(str(sub_id))
        dic = { }
        for i in range(0,len(info)):
            pageNumber = "c" + str(i+1)
            dic_tmp = {
                "chapters_id":info[i][0],    # 章节编号
                "subject_id":info[i][1],    # 属于哪本书的编号
                "chapters_name":info[i][2]   # 该章节中文名称
            }
            dic.setdefault(pageNumber,dic_tmp)
        return dic

    # 根据章节表获取标题
    def get_title(self,chp_id):
        dbTable = "titlenumber_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_according_to_chapter(str(chp_id))
        dic = { }
        for i in range(0,len(info)):
            pageNumber = "t" + str(i+1)
            dic_tmp = {
                "title_id":info[i][0],    # 章节编号
                "chapters_id":info[i][1],  # 属于哪本书的编号
            }
            dic.setdefault(pageNumber,dic_tmp)
        return dic

    # 根据题目获得详细信息
    # 说明
    #   title_id:   输入的titleid  
    #   titleHead:   题目的标题
    #   titleCont:  题目的内容
    #   titleAnswer:    题目的答案（选择填空混合）
    #   titleAnalysis:  题目的解析
    #   titleAveracc:   题目的平均正确率
    #   titlespaper:    题目来自的试卷
    #   specialNote:    特殊注解（一般没有为None）

    def get_title_info(self,tit_id):
        dbTable = "title_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_according_to_title(str(tit_id))
        dic = { }
        '''
        for i in range(0,len(info)):
            pageNumber = "t" + str(i+1)
            dic_tmp = {
                "title_id":info[i][0],    
                "titleHead":info[i][1],  
                "titleCont":info[i][2], 
                "titleAnswer":info[i][3],
                "titleAnalysis":info[i][4],
                "titleAveracc":info[i][5],
                "titlespaper":info[i][6],
                "specialNote":info[i][7],
            }
            dic.setdefault(pageNumber,dic_tmp)
        '''
        dic.setdefault("title_id",info[0][0])
        dic.setdefault("titleHead",info[0][1])
        dic.setdefault("titleCont",info[0][2])
        dic.setdefault("titleAnswer",info[0][3])
        dic.setdefault("titleAnalysis",info[0][4])
        dic.setdefault("titleAveracc",info[0][5])
        dic.setdefault("titlespaper",info[0][6])
        dic.setdefault("specialNote",info[0][7])
        return dic
    
    # 获取数据库中题目数量
    def get_title_len(self):
        dbTable = "title_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_len(dbTable)
        return info

    # 将发送过来的回答进行结果验证，并且将回答信息写入
    def answerCorrectJudgment(self,user_id,tit_id,answer,user_note):
        # 先提取题号对应的题目信息
        # 再将输入的答案与实际答案进行对比
        # 最后根据用户请求写入user_info表中生成总数据记录
        # 再将数据写入titlenote_info表中做详细记录
        # 最后返回True or False表示回答正确与否
        dbTable = "titlenote_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_according_to_title(str(tit_id))
        rightAnswer = info[0][3]
        print(answer,rightAnswer)
        isRight = False
        inpRight = "0"
        if str(answer) == str(rightAnswer):
            isRight = True
            inpRight = "1"
        # 更新用户回答总信息
        db.dbUpdate_user_answer(isRight,user_id)
        # 更新用户回答详细内容 - 记录题号和回答时间
        inputDataTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.dbInsert(dbTable,user_id,tit_id,inpRight,inputDataTime,user_note)
        return isRight
        



if __name__ == '__main__':
    op = OPcontrol()
    k = op.answerCorrectJudgment("1001","2","硬时系统","这一道题记录点信息")
    print(k)
