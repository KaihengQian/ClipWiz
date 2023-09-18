import pandas as pd
from sqlalchemy import create_engine

filename = "dict//StopWords.txt"
data_list = []
with open(filename, 'r',encoding='utf-8') as txtfile:
    for line in txtfile:
        data_list.append(line.strip())

# print(data_list[0])
data = pd.DataFrame(data_list[1:], columns=[data_list[0]])
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu?charset=utf8')
data.to_sql('stop', con=engine, if_exists='replace', index=False)
print("导入成功")
# print(data.head())
