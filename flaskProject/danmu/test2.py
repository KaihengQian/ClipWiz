from collections import defaultdict
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import jieba

jieba.setLogLevel(jieba.logging.INFO)

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu')

negative_df = pd.read_sql(text("select * from negative"), engine.connect())
not_word_list = negative_df['text'].tolist()

print(not_word_list)
