import os
import sys
projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import datetime
import models.DBconnect as DBconnect
import random

class OPcontrol:
    """
    control 控制层，承上启下，该层作用为：
    对基本的数据库层代码进行调用，并进行一系列的逻辑处理，并且返回结果给API层

    """
    def __init__(self):
        # 对于数据库而言，不用长连接，怕长时间不操作还占用带宽
        pass
    

    def check_login(self, user_name, user_pwd):
        """
        登陆确认，传递进入用户名，用户密码，并将传递进来的数据和数据库中的记录进行比对
        返回出是否成功登陆内容
        Args:
            user_name 用户名
            user_pwd 用户密码
        
        Returns
            一个字典，返回用户ID，用户名，和用户微信ID
        """
        db = DBconnect.DBconnect()
        info = db.dbQuery_userLogin(user_name, user_pwd)
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


    def __is_already(self, db, user_id):
        """
        内部函数，用来判断该用户是否已经存在，该内部方法的调用时刻在于创建【用户ID】的时候进行判断
        （即使user_id生成8位随机数，但还是不排除有可能有重复）

        Args:
            db 数据库打开的指针
            user_id 用户ID

        Return
            False - 不重复， True - 重复
        """
        db = DBconnect.DBconnect()
        info = db.dbQuery_user_is_already(user_id)
        if info == None:
            return False
        else:
            return True
         

    # 等待重构 - ❌
    def register(self, user_name, user_pwd):
        """
        创建一个新用户, 通过传递进来的用户名和密码注册。
        在旧的版本中，传入的参数是微信ID，可是微信的OpenID是无法通过前端获取的，只能由后端存储传递给前端，
        所以这一部分代码需要进行重构

        Args:
            user_name 用户名
            user_pwd 用户密码
        
        Returns:
            returnCode 正确返回a0，错误返回r0
            user_id 用户ID，通过随机数字生成
            user_name 用户名
            user_pwd   用户密码
            user_wx_id 微信号码
            user_rightAnswer 正确答题数0
            user_wrongAnswer 错误答题数0

        """
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
            
            
    def get_chapter_all(self):
        """
        内部测试API，获取全部的章节信息，返回一个字典
        固定设置的就是四个大科目《数据结构》，《操作系统》，《计算机组成原理》，《计算机网络》
        """
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
        

    def get_subject(self):
        """
        接下来的几段代码的逻辑均为： 科目ID --> 章节ID --> 题目ID --> 题目具体信息 --> 提交题目
        获取科目信息
        
        Returns:
            返回科目编号，科目名称，科目介绍，目前固定只有四个科目
        """
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

    
    def get_chapter(self,sub_id):
        """
        根据科目获取当前章节信息表

        Args:
            sub_id 科目ID
        
        Returns:
            返回 章节编号 ，科目编号，该章节的中文名称
        """
        dbTable = "chapters_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_chapter_according_to_subject(str(sub_id))
        dic = { }
        for i in range(0,len(info)):
            pageNumber = "c" + str(i+1)
            dic_tmp = {
                "chapters_id":info[i][0],    # 章节编号
                "subject_id":info[i][1],    # 科目编号
                "chapters_name":info[i][2]   # 该章节中文名称
            }
            dic.setdefault(pageNumber,dic_tmp)
        return dic


    def get_title(self,chp_id):
        """
        根据章节获取当前题目ID表

        Args:
            chp_id 章节ID
        
        Returns:
            返回 题目ID，章节ID
        """
        dbTable = "titlenumber_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_according_to_chapter(str(chp_id))
        dic = { }
        for i in range(0,len(info)):
            pageNumber = "t" + str(i+1)
            dic_tmp = {
                "title_id":info[i][0],    # 题目ID
                "chapters_id":info[i][1],  # 章节ID
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
        """
        根据题目ID获取题目的具体内容，包括获取到正确答案
        
        Args:
            tit_id 章节ID

        Returns:
            title_id:   输入的titleid  
            titleHead:   题目的标题
            titleCont:  题目的内容
            titleAnswer:    题目的答案（选择填空混合）
            titleAnalysis:  题目的解析
            titleAveracc:   题目的平均正确率
            titlespaper:    题目来自的试卷
            specialNote:    特殊注解（一般没有为None）

        """
        dbTable = "title_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_according_to_title(str(tit_id))
        dic = { }
        '''
        # 原来是多组的形式返回，但是貌似一个ID只有一个信息，所以多组不需要了
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
    
    
    def get_title_len(self):
        """
        获取数据库中题目数量，将会用在随机生成题目的范围中
        """
        dbTable = "title_info"
        db = DBconnect.DBconnect()
        info = db.dbQuery_title_len(dbTable)
        return info

    # 等待升级
    def answerCorrectJudgment(self,user_id,tit_id,answer,user_note):
        """
        验证传递进来的题目内容，过程原理是：
        先提取题号对应的题目信息
        再将输入的答案与实际答案进行对比
        最后根据用户请求写入user_info表中生成总数据记录
        再将数据写入titlenote_info表中做详细记录
        最后返回True or False表示回答正确与否
        """
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
