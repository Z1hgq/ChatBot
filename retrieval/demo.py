# coding: utf-8
import json
import nltk
import numpy as np
import scipy.spatial.distance as distance
# from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt
import jieba

# '停用词列表'为所有函数共用(使用nltk停用词)
# nltk.download('stopwords')
# nltk.download('wordnet')
# stopWords = stopwords.words("chinese")

# customStopWords = ["when", "what", "how", "where","the"]
# stopWords.extend(customStopWords)

# 创建停用词list
def stopwordslist(filepath):
    stopWords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopWords
stopWords = stopwordslist('stopWords')  # 这里加载停用词的路径
#预处理 数据清洗 停用词 小写 去标点
def clean_words(sentence):
    # wordList = nltk.word_tokenize(strWords)
    # lemmatizer = WordNetLemmatizer()
    # filteredWords = [lemmatizer.lemmatize(word.lower()) for word in wordList if word.isalpha() and word.lower() not in stopWords]
    # return filteredWords
    # print(filteredWords)
    sentence_seged = jieba.cut(sentence.strip())
    
    outstr = ''
    for word in sentence_seged:
        if word not in stopWords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
    
# 读取数据生成新的字典
def read_corpus(filePath):
    # 问题列表
    qList = []
    # 问题的关键词列表
    qList_kw = []
    # 答案列表
    aList = []
    count = 0
    with open(filePath) as f:
        for line in f:
            if count % 2 == 0:
                qList.append(line)
                qList_kw.append(clean_words(line))
            if count % 2 == 1:
                aList.append(line)
            print(count)
            count += 1
    return qList_kw, qList, aList

qList_kw, questionList, answerList = read_corpus("./data/data")

#根据下标把问题和答案关联一起以下标方式输出
print(questionList[0])
print(answerList[0])


#通过观察词频的分布类似有zip's law, 是一个很著名的现象，包括在社交网络里面（比如大V的好友数非常多，其他人的好友数指数级下降）
def plot_words(wordList):
    fDist = FreqDist(wordList)
    #print(fDist.most_common())
    print("单词总数: ",fDist.N())
    print("不同单词数: ",fDist.B())
    # fDist.plot(10)
all_question = " ".join(questionList)
qWordLst = clean_words(all_question)
plot_words(qWordLst)


#把每一个文本转换成向量。
def calculate_sparse(questionList):
    # 每一个问题转换成tf-idf向量
    vectorizer = TfidfVectorizer(smooth_idf=False, lowercase=True, stop_words=stopWords)
    # 得到的是csr_matrix型矩阵（压缩后的稀疏矩阵）
    vectorizer.fit_transform(questionList)
    # 获取词列表
    keywordList = vectorizer.get_feature_names()
    wordNum = len(keywordList)
    # 获取文档总数（问题总数）
    docNum = len(questionList)
    #print(docNum)
    # 计算矩阵大小
    matrixSize = wordNum * docNum
    #print(matrixSize)
    # 计算零元素个数
    zeroElementNum = 0
    for question in questionList:
        for tmpWord in keywordList:
            if tmpWord not in question:
                zeroElementNum += 1

    # 根据tf-idf公式，若tf为0，那么其tf-idf值必然为零 tf-idf矩阵的稀疏度为
    return zeroElementNum / matrixSize
sparseDeg = calculate_sparse(questionList)
print (sparseDeg)  # 打印出稀疏度


# 两个问题之间的相似度(余弦相似度计算)
def calcaute_cosSimilarity(inputQuestion, questionDict):
    simiVDict = {}
    vectorizer = TfidfVectorizer(smooth_idf=False, lowercase=True, stop_words=stopWords)
    for idx, question in questionDict.items():
        tfidf = vectorizer.fit_transform([inputQuestion, question])
        simiValue = ((tfidf * tfidf.T).A)[0, 1]
        if simiValue > 0:
            simiVDict[idx] = simiValue
    return simiVDict


#找到相似度最高的TOP5问题，并把5个潜在的答案做返回 
def top5results(inputQuestion):
    questionDict = {}
    for idx, question in enumerate(questionList):
        questionDict[idx] = question
    simiVDict = calcaute_cosSimilarity(inputQuestion, questionDict)
    d = sorted(simiVDict, key=simiVDict.get, reverse=True)
    #print(d)
    # Top5最相似问题和对应的答案
    print("Top5相似-基于余弦相似度")
    for idx in d[:5]:
        print("问题： " + questionList[idx])
        print("答案： " + answerList[idx])

print (top5results("嗨，最近如何?"))

#利用倒排表的优化。 
def invert_idxTable(qList_kw):  # 定一个一个简单的倒排表
    invertTable = {}
    for idx, tmpLst in enumerate(qList_kw):
        for kw in tmpLst:
            if kw in invertTable.keys():
                invertTable[kw].append(idx)
            else:
                invertTable[kw] = [idx]
    return invertTable
# 计算倒排表
invertTable = invert_idxTable(qList_kw) 
def filter_questionByInvertTab(inputQuestionKW, questionList, invertTable):
    idxLst = []
    questionDict = {}
    for kw in inputQuestionKW:
        if kw in invertTable.keys():
            idxLst.extend(invertTable[kw])
    idxSet = set(idxLst)
    for idx in idxSet:
        questionDict[idx] = questionList[idx]
    return questionDict

def top5results_invidx(inputQuestion):
    inputQuestionKW = clean_words(inputQuestion)
    filteredQuestionDict = filter_questionByInvertTab(inputQuestionKW, questionList, invertTable)
    # 计算相似度
    simiVDict = calcaute_cosSimilarity(inputQuestion, filteredQuestionDict)
    d = sorted(simiVDict, key=simiVDict.get, reverse=True)
    #print(d)
    # Top5最相似问题，及它们对应的答案
    print("Top5相似-基于倒排表")
    for idx in d[:5]:
        print("问题： " + questionList[idx])
        print("答案： " + answerList[idx])
print (top5results_invidx("嗨，最近如何?"))
