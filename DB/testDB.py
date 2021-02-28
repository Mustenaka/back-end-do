import pymysql

conn = pymysql.connect(
    host='159.75.72.254',port=3306, user='root', passwd="HHM135#", db='HHM'
    )

cur = conn.cursor()
cur.execute("SELECT * FROM user_info")
for r in cur:
    print(r)
cur.close()
conn.close()