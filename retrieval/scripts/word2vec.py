# -*- coding: utf-8 -*-
from gensim.models import word2vec
import gensim
# 导入训练好的词向量
# model = word2vec.Word2Vec.load('./word_vector/Word60.model')

# model = gensim.models.Word2Vec([b],min_count=1,size=32)
inputFile = open('../data/QingYun_wordlist.txt', 'r',encoding='utf-8')
outputFile = open('../data/QingYun_zh_vec.txt','w', encoding='utf-8')
arr = []
for line in inputFile:
    arr.append(str(line).strip('\n'))

# modelSingle = gensim.models.Word2Vec(arr,min_count=1,size=100)
modelMultiple = gensim.models.Word2Vec([arr],min_count=1,size=100)
count = 0
for word in arr:
    print(word)
    vec = []
    # if len(word) > 1:
    #     vec = modelMultiple[word]
    # if len(word) == 1:
    #     vec = modelSingle[word]
    vec = modelMultiple[word]
    vec_ = ''
    for e in vec:
        vec_ += ' '+str(e)
    res = word + vec_ + '\n'
    outputFile.writelines(res)
    print(count)
    count += 1


inputFile.close()
outputFile.close()
