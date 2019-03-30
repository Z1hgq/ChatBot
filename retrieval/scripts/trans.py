import numpy as np
import jieba 
def QingYun():
    fout = open('../data/QingYun','w')
    with open('../data/QingYun.yml',encoding='utf-8') as f:
        count = 0
        for line in f:
            if count%2==0:
                fout.writelines(line.lstrip('- - '))
            if count%2==1:
                fout.writelines(line.lstrip('  - '))
        count += 1
    fout.close()

def xiaohuangji():
    fout = open('../data/xiaohuangji','w')
    with open('../data/xiaohuangji.yml',encoding='utf-8') as f:
        count = 0
        for line in f:
            if count%2==0:
                fout.writelines(line.lstrip('- - '))
            if count%2==1:
                fout.writelines(line.lstrip('  - '))
        count += 1
    fout.close()

questionListPath = '../data/questionList'
zh_vectorPath = '../data/QingYun_zh_vec.txt'
questionListVecPath = './questionListVec'
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
def get_vectorValue(keywordList):
    # s = datetime.datetime.now()
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
    # e = datetime.datetime.now()
    # print('向量计算用时:',e-s)
    return vectorSum / len(vectorValueList) 
print('-----------问题列表转向量-----------')
f_out = open(questionListVecPath,'w',encoding='utf-8')
with open(questionListPath,encoding='utf-8') as f:
    count = 0
    for line in f:
        if count >= 56726:
            strl = ''
            for e in get_vectorValue(clean_words(line)):
                strl += str(e) + ' '
            f_out.writelines(strl+'\n')
        print('进度：',count,'/117537')
        count += 1
f_out.close()
