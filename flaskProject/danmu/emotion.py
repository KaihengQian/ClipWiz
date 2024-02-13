from collections import defaultdict
import jieba
jieba.setLogLevel(jieba.logging.INFO)
from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu')


# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.lcut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    stopwords = set()

    with open('dict/stopwords.txt', 'r', encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    return list(filter(lambda x: x not in stopwords, seg_result))


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    with open('dict/BosonNLP.txt', 'r', encoding='utf-8') as sen_file:
        sen_list = sen_file.readlines()     # 获取字典文件内容
        sen_dict = defaultdict()            # 创建情感字典
        for i in sen_list:
            if len(i.split(' ')) == 2:
                sen_dict[i.split(' ')[0]] = i.split(' ')[1]
    with open('dict/NegativeWords.txt', 'r', encoding='utf-8') as not_word_file:
        not_word_list = not_word_file.readlines()
    with open('dict/AdverbOfDegree.txt', 'r', encoding='utf-8') as degree_file:
        degree_list = degree_file.readlines()
        degree_dict = defaultdict()
        for i in degree_list:
            degree_dict[i.split(',')[0]] = i.split(',')[1]
    sen_word = dict()
    not_word = dict()
    degree_word = dict()

    for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
            sen_word[i] = sen_dict[word]
        elif word in not_word_list and word not in degree_dict.keys():
            not_word[i] = -1
        elif word in degree_dict.keys():
            degree_word[i] = degree_dict[word]

    return sen_word, not_word, degree_word


# 计算情感词的分数
# 伪代码 finalScore = (-1) ^ (num of not_words) * degreeNum * sentiScore
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    w = 1
    score = 0
    sentiment_index = -1     # 情感词下标初始化
    sentiment_index_list = list(sen_word.keys())
    # 遍历分词结果(为了定位两个情感词之间的程度副词和否定词)
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score += w*float(sen_word[i])
            sentiment_index += 1
            # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
            if sentiment_index < len(sentiment_index_list)-1:
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index+1]):
                    if j in not_word.keys():
                        w *= -1
                    elif j in degree_word.keys():
                        w *= float(degree_word[j])
        if sentiment_index < len(sentiment_index_list)-1:
            i = sentiment_index_list[sentiment_index+1]
    return score


# 计算得分
def sentiment_score(sentence):
    seg_list = seg_word(sentence)
    sen_word, not_word, degree_word = classify_words(seg_list)
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score
