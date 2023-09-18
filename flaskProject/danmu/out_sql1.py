import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu')
sql = "select elapse_time,text from record "
data = pd.read_sql(text(sql), engine.connect())
print(data.head())
print(type(data))
