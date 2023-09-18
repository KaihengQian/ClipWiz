import pandas as pd
from sqlalchemy import create_engine

# data = pd.read_csv("dict//BosonNLP.txt", delim_whitespace=True)
data = pd.read_csv("dict//NegativeWords.txt")
# data = pd.read_csv("D://桌面//halftime//danmu.csv")
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu?charset=utf8')
data.to_sql('record', con=engine, if_exists='replace', index=False)
print("导入成功")
print(data.head())
