import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='danmu', charset='utf8')
cur = conn.cursor()
v_sql = "select text,degree from adverb limit 10"
cur.execute(v_sql)
data = cur.fetchall()
print(data)
print(data[0])
print(type(data))
# df = pd.DataFrame(list(data))
# print(df)
# print(type(df))
cur.close()
conn.close()
