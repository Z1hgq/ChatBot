# coding: utf-8

import gensim.models as g
import scipy.spatial.distance as distance

model = g.Doc2Vec.load('models/ko_d2v.model')

# print(model.most_similar('傻逼'))
# print(model.docvecs.most_similar('呵呵'))
# 也可以推断一个句向量(未出现在语料中)
words = u"여기 나오는 팀 다 가슴"

vec1 = model.infer_vector(words.split())

vec2 = model.infer_vector(words.split())


print(1 - distance.cosine(vec1, vec2))


# f_out = open('./data/vecTest','w')
# with open('./data/questionList', 'r', encoding='UTF-8') as r:
#     count = 0
#     for line in r:
#         strl = ''
#         vec = model.infer_vector(line.split())
#         for e in vec:
#             strl += str(e) + ' '
#         print(count)
#         count+=1
#         f_out.writelines(strl+'\n')
# f_out.close()

