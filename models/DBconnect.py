import pymysql
import datetime

class DBconnect:
    """
    数据库连接类，初始化将会连接数据库，其中的方法是增删改查，析构将会关闭数据库连接

    Attributes:
        None

    """
    def __init__(self):
        """
        初始化数据库链接地址，连接数据库
        host='159.75.72.254',port=3306, user='root', passwd="HHM135#", db='HHM'
        """
        try:
            self.conn = pymysql.connect(
                host='159.75.72.254',port=3306, user='root', passwd="HHM135#", db='HHM'
                )
            '''
            # 本地数据库连接地址
            self.conn = pymysql.connect(
                host='127.0.0.1',port=3306, user='root', passwd="HHM135#", db='HHM'
                )
            '''
            self.cur = self.conn.cursor()
        except e:
            print(e)

    def dbQuery(self,dbTable):
        """
        数据库查询代码，将需要查询的表名传入

        Args:
            dbTable: 需要查询的表名
        
        Returns:
            一个查询结果的List，没有任何数据过滤，存粹”SELECT * FROM “返回表
        """
        cur = self.cur
        sql = "SELECT * FROM "+dbTable
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
            #print(r)
        return returnList
        


    # -这几个特殊查询最好别合并，因为参数传递很多，这样做就不需要手动指定那么多的参数了
    # 特殊查询 -
    # 根据 subject 编号查询到该编号下的 chapter 信息
    def dbQuery_chapter_according_to_subject(self,sub_id):
        """
        特殊查询，不这样设计API的话，可能该API传入参数会过多，所以这样设计的传入的API。
        通过subject_id 查询 chapter_id

        Args：
            sub_id： 需要查询的 科目ID

        Returns:
            返回章节列表

        """
        cur = self.cur
        dbTable = "chapters_info"
        sql = "SELECT * FROM "+dbTable +" WHERE subjectId='"+sub_id+"'"
        #print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
            #print(r)
        return returnList
    
    # 特殊查询 - 
    # 根据 chapter 编号查询该编号下的 title 信息
    def dbQuery_title_according_to_chapter(self,chp_id):
        """
        通过chapter_id 查询 title_id，通过章节ID查询到题目ID

        Args：
            chp_id 需要查询的 章节ID

        Returns:
            返回题目列表

        """
        cur = self.cur
        dbTable = "titlenumber_info"
        sql = "SELECT * FROM "+dbTable +" WHERE chaptersId='"+chp_id+"'"
        print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
        return returnList
    
    # 特殊查询 - 反向查询
    # 根据 title 编号查询该编号下的 chapter 编号
    def dbQuery_chapter_by_title(self,tit_id):
        """
        根据 title 编号反向查询该编号下的 chapter 编号

        Args：
            tit_id 需要查询的 题目ID

        Returns:
            返回题目列表

        """
        cur = self.cur
        dbTable = "titlenumber_info"
        sql = "SELECT chaptersId FROM "+dbTable +" WHERE titleId='"+tit_id+"'"
        print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
        return returnList


    # 特殊查询 - 反向查询
    # 根据 chapter 编号查询该编号下的 subject 编号
    def dbQuery_subject_by_chapter(self,chp_id):
        """
        根据 chapter 编号反向查询该编号下的 subject 编号

        Args：
            chp_id 需要查询的 章节ID

        Returns:
            返回题目列表

        """
        cur = self.cur
        dbTable = "chapters_info"
        sql = "SELECT subjectId FROM "+dbTable +" WHERE chaptersId='"+chp_id+"'"
        print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
        return returnList
    
    # 特殊查询 - 
    # 根据 title 编号查询该编号下的 title 的详细信息
    def dbQuery_title_according_to_title(self,tit_id):
        """
        通过题目ID查询到这个题目对应的具体题目内容

        Args：
            tit_id 需要查询的 题目ID

        Returns:
            返回题目具体信息，具体信息有：

        """
        cur = self.cur
        dbTable = "title_info"
        sql = "SELECT * FROM "+dbTable +" WHERE titleId='"+tit_id+"'"
        print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
        return returnList


    def dbQuery_title_len(self,dbTable):
        """
        查询表中长度

        Args:
            dbTable 需要查询的表

        Returns:
            返回一个数字，即拥有多少已经存储的内容
        """
        cur = self.cur
        sql = "select  count(*) from `"+dbTable+"`"
        print(sql)
        cur.execute(sql)
        for r in cur:
            return r[0]
    

    def dbQuery_userLogin(self, user_name ,user_pwd):
        """
        通过用户名密码进行登陆判断，准备改成使用用户账户名和密码登陆的方式
        Update:
            已修改为用户名和密码的登录方式。

        Args:
            user_name 用户名
            user_pwd 用户密码

        Returns:
            返回一个查询结果，即存在该用户ID和其对应的密码则为登陆成功，否则为失败。
        """
        conn = self.conn
        cur = self.cur
        dbTable = "user_info"
        sql  = "SELECT * FROM "+dbTable+" WHERE userName='"+user_name+"' and userPwd='"+user_pwd+"'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
            return e
        # 返回第一个合适的信息 - 也只有一个合适的信息
        for r in cur:
            return r


    def dbQuery_user_is_already(self,user_id):
        """
        判断一个用户ID是否已经存在了，在注册的时候使用

        Args:
            user_id 用户ID

        Returns:
            返回查询到的user_id内容

        """
        conn = self.conn
        cur = self.cur
        dbTable = "user_info"
        sql  = "SELECT * FROM "+dbTable+" WHERE userId='"+user_id+"'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
            return e
        # 返回第一个合适的信息 - 也只有一个合适的信息
        for r in cur:
            return r
    
    # 特殊查询 
    # 查询一个账户是否是管理员
    def dbQuery_is_administrator(self, user_id):
        """
        查询一个用户是不是管理员

        Args：
            user_id 用户ID

        Returns:
            返回题目列表

        """
        cur = self.cur
        dbTable = "user_info"
        sql = "SELECT isAdministrator FROM "+dbTable +" WHERE userId='"+user_id+"'"
        print(sql)
        cur.execute(sql)
        returnList = []
        for r in cur:
            returnList.append(r)
        return returnList


    def dbDelete(self,dbTable,needId,inputId):
        """
        删除表中特定字段以及对应该字段的值的记录
        Args:
            needId 需要查询的字段，比如说user_id
            inputId 需要删除该对应字段的记录，比如说 momon1
        
        """
        conn = self.conn
        cur = self.cur
        sql = "DELETE from "+dbTable+" where "+needId+"="+inputId
        #sql = 'DELETE from user_info where userId='+inputId
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
    

    def dbInsert(self,dbTable,*args):
        """
        插入数据库代码，根据表名称自动产生对应该表名称的插入代码，
        但是前提是传入的args的值必须合适，不能多也不能少

        Args:
            dbTable 数据表
            args 多参数传入值，必须要和数据库字段一一对应
        """
        conn = self.conn
        cur = self.cur

        # python没有switch，本身switch需要哈希比较的，这和Python倡导的灵活性相互驳斥，反而会退化到IF-ELIF-ELSE级别
        # 所以就用if-elif-else进行特判表对应的sql语句
        sql = ""
        print(args)
        if dbTable == "user_info":
            sql = "INSERT INTO "+dbTable+" VALUES(%s,%s,%s,%s,%s,%s,%s);"
        elif dbTable == "titlenumber_info":
            sql = "INSERT INTO "+dbTable+" VALUES(%s,%s);"
        elif dbTable == "titlenote_info":
            # 这个表格第四个是时间参数，待处理 - 特判解决
            #datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            #print(args)
            #sql = "INSERT INTO "+dbTable+" VALUES('{0}','{1}','{2}',str_to_date('{3}','%%Y-%%m-%%d %%H:%%i:%%s'),'{4}');".format(*args)
            sql = "INSERT INTO "+dbTable+" VALUES('{0}','{1}','{2}','{3}','{4}');".format(*args)
        elif dbTable == "title_info":
            sql = "INSERT INTO "+dbTable+" VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        elif dbTable == "subject_info":
            sql = "INSERT INTO "+dbTable+" VALUES(%s,%s,%s);"
        elif dbTable == "load_info":
            sql = "INSERT INTO "+dbTable+" VALUES('{0}','{1}','{2}');".format(*args)
        elif dbTable == "chapters_info":
            sql = "INSERT INTO "+dbTable+" VALUES(%s,%s,%s);"

        print(sql)
        try:
            if dbTable == "titlenote_info" or dbTable == "load_info" : 
                cur.execute(sql)
            else:
                cur.execute(sql,args)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
            return False
        return True


    def dbUpdate_user_answer(self,isRight,user_id):
        """
        根据用户做题的情况对用户答对字段或者是用户答错字段进行加一或者减一
        
        Args:
            isRight 是否答对了，bool 变量
            user_id 用户ID
        """
        conn = self.conn
        cur = self.cur
        if isRight:
            sql = "update HHM.user_info set userRightAnswer=userRightAnswer+1 where userId='"+user_id+"'"
        else:
            sql = "update HHM.user_info set userWrongAnswer=userWrongAnswer+1 where userId='"+user_id+"'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()


    def dbUpdate_title_info(self, title_id, titleAveracc, titleRight, titleWrong):
        """
        更新题目表中的正确与否的记录，将数据写入titlenote_info表
        会自动生成一个responTime信息

        Args:
            user_id 用户ID
            title_id 标题ID
            isRight 是否正确
            personNote
        """
        conn = self.conn
        cur = self.cur
        sql = "update HHM.title_info set titleAveracc=" + titleAveracc + ",titleRight=" + titleRight + "titleWrong=" + titleWrong + " where titleId='" + title_id + "'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()




    # 测试更新、修改代码 - 完成
    # 封装更新，修改代码 - 完成
    # dbTable 表名称 -  needValue 需要修改的值名 - inputValue 需要修改的值 - needId 查询的ID名 - inputId 查询的ID具体内容
    def dbUpdate_signled(self,dbTable,needValue,inputValue,needId,inputId):
        """
        对数据库中单个表的参数进行修改，
        Args：
            needValue 需要修改的值名 
            inputValue 需要修改的值 
            needId 查询的ID名 
            inputId 查询的ID具体内容
        """
        conn = self.conn
        cur = self.cur
        sql = "update "+ dbTable+" set "+needValue+"=\'"+inputValue+"\' where " + needId + "=" + inputId
        #sql = "update user_info set userPwd='666666' where userId='1111'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
            return False

    def update_title_all(self, dbTable, title_id, titleHead, titleCont, titleAnswer, titleAnalysis, titlespaper, specialNote):
        """
        对数据库中题目表中的题目内容进行修改 - 但是不修改答题数量，以及正确率等内容，这些东西能够被修改就会有作弊嫌疑

        Args：
            dbTable 需要修改的题目表
            title_id 题目ID
            titleHead 题目标题
            titleCont 题目内容
            titleAnswer 题目答案
            titleAnalysis 题目分析
            titlespaper 题目出处
            specialNote 特殊注解

        Returns:
            True - 成功更新
            False - 失败更新
        """
        conn = self.conn
        cur = self.cur
        sql = "UPDATE HHM.title_info SET titleHead='"+ titleHead +"',titleCont='"+ titleCont +"',titleAnswer='"+ titleAnswer +"',titleAnalysis='"+ titleAnalysis +"',titleIspaper='"+ titlespaper +"',specialNote='"+ specialNote +"' WHERE titleId='"+ title_id +"'"
        print(sql)
        try:
            cur.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print("操作异常：%s"%str(e))
            #错误回滚
            conn.rollback()
            return False

    
    def dbUpdate_all(self,dbTable):
        """
        批量更新，还没有写，我觉得批量修改表中某个记录的代码需要特判，所以应该在后续重新创建
        """
        pass

    def __del__(self):
        """
        析构函数，关闭表和查询
        """
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    db = DBconnect()

    chooseTable = "load_info"
    inputDataTime = datetime.datetime.now().strftime("%Y-%m-%d")
    args = ("1010","1",inputDataTime)
    db.dbInsert(chooseTable,"1010","1",inputDataTime)
    print(inputDataTime)
    #db.dbQuery(chooseTable)
    