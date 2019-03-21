# coding: utf-8
import json
import nltk
import numpy as np
import scipy.spatial.distance as distance
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt
import jieba
import sys
import random
import pickle

filePath = './data/data'
questionListPath = './data/questionList'
answerListPath = './data/answerList'
questionKeyListPath = './data/questionKeyList'
invertTablePath = './data/invertTable.bin'

#将数组写进文件
def writeFile(filePath,arr):
    with open(filePath,'w') as f:
        for line in arr:
            f.writelines(line)
#将文件转成数组
def readFile(filePath):
    arr = []
    with open(filePath,'r',encoding='utf-8') as f:
        for line in f:
            arr.append(line)
    return arr
# 创建停用词list
def stopwordslist(filepath):
    stopWords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopWords
#预处理 数据清洗 停用词 小写 去标点
def clean_words(sentence):
    stopWords = stopwordslist('stopWords')
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
                qList_kw.append(clean_words(line) + '\n')
            if count % 2 == 1:
                aList.append(line)
            print(count)
            count += 1
    print(qList,aList,qList_kw)
    writeFile(questionListPath,qList)
    writeFile(questionKeyListPath,qList_kw)
    writeFile(answerListPath,aList)

#通过观察词频的分布类似有zip's law, 是一个很著名的现象，包括在社交网络里面（比如大V的好友数非常多，其他人的好友数指数级下降）
def plot_words(wordList):
    fDist = FreqDist(wordList)
    #print(fDist.most_common())
    print("单词总数: ",fDist.N())
    print("不同单词数: ",fDist.B())
    # fDist.plot(10)



#把每一个文本转换成向量。
def calculate_sparse(questionList):
    stopWords = stopwordslist('stopWords')
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



# 这里加载停用词的路径
# stopWords = stopwordslist('stopWords')
#构建字典  
# qList_kw, questionList, answerList = read_corpus("./data/data")
#观察词频的分布
# all_question = " ".join(questionList)
# qWordLst = clean_words(all_question)
# plot_words(qWordLst)
#文本转向量
# sparseDeg = calculate_sparse(questionList)
# print (sparseDeg)  # 打印出稀疏度



# 两个问题之间的相似度(余弦相似度计算)
def calcaute_cosSimilarity(inputQuestion, questionDict):
    stopWords = stopwordslist('stopWords')
    simiVDict = {}
    vectorizer = TfidfVectorizer(smooth_idf=False, lowercase=True, stop_words=stopWords)
    for idx, question in questionDict.items():
        tfidf = vectorizer.fit_transform([inputQuestion, question])
        simiValue = ((tfidf * tfidf.T).A)[0, 1]
        if simiValue > 0:
            simiVDict[idx] = simiValue
    return simiVDict

#利用倒排表的优化。 
def invert_idxTable(qList_kw):  # 定一个一个简单的倒排表
    invertTable = {}
    for idx, tmpLst in enumerate(qList_kw):
        for kw in tmpLst:
            if kw in invertTable.keys():
                invertTable[kw].append(idx)
            else:
                invertTable[kw] = [idx]
    print(invertTable)
    return invertTable
# 计算倒排表
 
def train(filePath):
    # stopWords = stopwordslist('stopWords')
    read_corpus(filePath)
    qList_kw = readFile(questionKeyListPath)
    # questionList =  readFile(questionListPath)
    # answerList = readFile(answerListPath)
    invertTable = invert_idxTable(qList_kw)
    myfile=open(invertTablePath,'wb')
    pickle.dump(invertTable,myfile)
    myfile.close()
    print('训练完成')
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


def top5results_invidx(inputQuestion,questionList,answerList,invertTable):
    inputQuestionKW = clean_words(inputQuestion)
    filteredQuestionDict = filter_questionByInvertTab(inputQuestionKW, questionList, invertTable)
    # 计算相似度
    simiVDict = calcaute_cosSimilarity(inputQuestion, filteredQuestionDict)
    d = sorted(simiVDict, key=simiVDict.get, reverse=True)
    #print(d)
    # Top5最相似问题，及它们对应的答案
    if len(d) == 0:
            print('bot:没听懂')
    if len(d) > 0:
        if len(d) > 5:
            index = random.randint(0,4)
            idx = d[index]
            print("bot:" + answerList[idx].strip('\n'))
        if len(d) <= 5:
            index = random.randint(0,len(d)-1)
            idx = d[index]
            print("bot:" + answerList[idx].strip('\n'))
        
if __name__ == "__main__":
    if sys.argv[1] == 'train':
        train(filePath)
    else:
        questionList = readFile(questionListPath)
        answerList = readFile(answerListPath)
        myfile = open(invertTablePath,'rb')
        invertTable  = pickle.load(myfile)
        myfile.close()
        while True:
            sys.stdout.write("> ")
            sys.stdout.flush()
            input_seq = sys.stdin.readline()
            top5results_invidx(input_seq,questionList,answerList,invertTable)
