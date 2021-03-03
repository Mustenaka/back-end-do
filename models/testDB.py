import pymysql
import datetime

def testMYSQL_isConnect():
    try:
        conn = pymysql.connect(
            host='159.75.72.254',port=3306, user='root', passwd="HHM135#", db='HHM'
            )
        cur = conn.cursor()
        cur.close()
        conn.close()
        return "successful connect mysql"
    except e:
        print(e)
        return "can not connect mysql"

print(testMYSQL_isConnect())