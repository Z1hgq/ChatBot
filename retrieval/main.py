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
import datetime

filePath = './data/xhj_data'
questionListPath = './data/questionList'
answerListPath = './data/answerList'
questionKeyListPath = './data/questionKeyList'
invertTablePath = './data/invertTable.bin'
zh_vectorPath = './data/zh_vec.txt'

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
    # stopWords = stopwordslist('stopWords')
    sentence_seged = jieba.cut(sentence,cut_all=False)
    # print(sentence_seged)
    # outstr = ''
    # for word in sentence_seged:
    #     if word not in stopWords:
    #         if word != '\t':
    #             outstr += word
    #             outstr += " "
    # if outstr == '':
    outstr = ' '.join(sentence_seged)

        # for word in sentence_seged:
        #     outstr += word
        #     outstr += " "
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
def get_vectorValue(keywordList):
        s = datetime.datetime.now()
        filePath = zh_vectorPath
        vectorValueList = []
        with open(filePath, 'r', encoding='UTF-8') as r:
            for line in r.readlines():
                tmpLst = line.rstrip('\n').split(" ")
                word = tmpLst[0]
                # print(tmpLst[1:])
                if word in keywordList:
                    vectorValueList.append([float(x) for x in tmpLst[1:]])
        # 按关键词的平均，算句子的向量
        vectorSum = np.sum(vectorValueList, axis=0)
        e = datetime.datetime.now()
        print('向量计算用时:',e-s)
        return vectorSum / len(vectorValueList) 
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
    print('-----------问题列表转向量-----------')
    f_out = open('./data/questionListVec','w')
    with open('./data/questionList') as f:
        count = 0
        for line in f:
            if count > 4320:
                strl = ''
                for e in get_vectorValue(clean_words(line)):
                    strl += str(e) + ' '
                print('进度：',count,'/10000')
                f_out.writelines(strl+'\n')
            count += 1
    f_out.close()
    print('训练完成')
def filter_questionByInvertTab(inputQuestionKW, questionList, invertTable):
    # print(invertTable)
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
    if inputQuestionKW != '':
        filteredQuestionDict = filter_questionByInvertTab(inputQuestionKW, questionList, invertTable)
        # 计算相似度
        simiVDict = calcaute_cosSimilarity(inputQuestion, filteredQuestionDict)
        d = sorted(simiVDict, key=simiVDict.get, reverse=True)
        #print(d)
        # Top5最相似问题，及它们对应的答案
        if len(d) == 0:
                print('bot:不好意思，我没听懂')
        if len(d) > 0:
            if len(d) > 5:
                index = random.randint(0,4)
                idx = d[index]
                print("bot:" + answerList[idx].rstrip('\n'))
            if len(d) <= 5:
                index = random.randint(0,len(d)-1)
                idx = d[index]
                print("bot:" + answerList[idx].rstrip('\n'))
    else:
        print('bot:能多说一些吗')
# ### 6 基于词向量的文本表示
def top5results_emb(inputQuestion,questionList,answerList,invertTable):
    # print ('inputQuestionKW')
    inputQuestionKW = clean_words(inputQuestion)
    # input Question中的keywords
    input_question_vector = get_vectorValue(inputQuestionKW)
    print (input_question_vector)
    simiVDict = {}
    filteredQuestionDict = filter_questionByInvertTab(inputQuestionKW, questionList, invertTable)
    # print ('filteredQuestionDict')
    for idx, question in filteredQuestionDict.items():
        # 取得当前问题的Vector值
        filtered_question_vector = get_vectorValue(clean_words(question))
        # 计算与输入问句的cos similarity
        simiVDict[idx] = 1 - distance.cosine(input_question_vector, filtered_question_vector)
        print(simiVDict[idx])
    print ('multi')
    d = sorted(simiVDict, key=simiVDict.get, reverse=True)
    print(d)
    # Top5最相似问题对应的答案
    for idx in d[:5]:
        print("bot:" + answerList[idx].rstrip('\n'))  
if __name__ == "__main__":
    if sys.argv[1] == 'Train':
        train(filePath)
    else:
        questionList = readFile(questionListPath)
        answerList = readFile(answerListPath)
        myfile = open(invertTablePath,'rb')
        invertTable  = pickle.load(myfile)
        myfile.close()
        # print(invertTable)
        while True:
            sys.stdout.write("> ")
            sys.stdout.flush()
            input_seq = sys.stdin.readline()
            start = datetime.datetime.now()
            top5results_invidx(input_seq,questionList,answerList,invertTable)
            end = datetime.datetime.now()
            print ('回答用时:',end-start)
            # start2 = datetime.datetime.now()
            # top5results_emb(input_seq,questionList,answerList,invertTable)
            # end2 = datetime.datetime.now()
            # print ('回答用时:',end2-start2)
