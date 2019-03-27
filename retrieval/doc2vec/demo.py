import gensim
# import jieba
import pandas as pd
import os
import gensim.models as g
# import stopwordslist from main
from main import clean_words 

def cut_sentence():
    count = 0
    f_out = open('./data/xhj_cut','w')
    with open('./data/xhj_data') as f_in:
        for line in f_in:
            print(clean_words(line))
            f_out.writelines(str(clean_words(line)))
            print(count)
            count += 1
            if count == 10000:
                break
    f_out.close()
cut_sentence()
TaggededDocument = gensim.models.doc2vec.TaggedDocument
def X_train(cut_sentence):
    x_train = []
    for i,text in enumerate(cut_sentence):
        word_list = text.split(' ')
        l = len(word_list)
        word_list[l-1] = word_list[l-1].strip()
        document = TaggededDocument(word_list,tags=[i])
        x_train.append(document)
    return x_train
sentences = []
with open('./data/xhj_cut') as f:
    for line in f:
        sentences.append(line.rstrip('\n'))
print(X_train(sentences))

def train(x_train,size = 300):
    model = g.Doc2Vec(x_train,dm=1,size=size,window=8,min_count=5,workers=4)
    model.train(x_train,total_examples=model.corpus_count,epochs=10)
    return model

model_dm = train(X_train(sentences))

strl = '木兰当户织'
test_text = strl.split(' ')

inferred_vector = model_dm.infer_vector(doc_words=test_text,alpha=0.025,steps=500)

sims = model_dm.docvecs.most_similar([inferred_vector],topn=10)

for count,sim in sims:
    print(count,sim)
    sentence = sentences[count].strip(' ')
    words = ''
    for word in sentence:
        words = words+word
    print(words,sim,len(sentence))

# # 模型训练
# model = g.Doc2Vec(X_train(sentences), dm=1, size=100, window=8, min_count=5, workers=4)
# # 保存模型
# model.save('models/ko_d2v.model')

# def test_doc2vec():
#     # 加载模型
#     model = g.Doc2Vec.load('models/ko_d2v.model')
#     # 与标签‘0’最相似的
#     print(model.docvecs.most_similar('0'))
#     # 进行相关性比较
#     print(model.docvecs.similarity('0','1'))
#     # 输出标签为‘10’句子的向量
#     print(model.docvecs['10'])
#     # 也可以推断一个句向量(未出现在语料中)
#     words = "今天中午你吃饭了吗"
#     print(model.infer_vector(words.split()))
#     # 也可以输出词向量
#     print(model['吃饭'])

# test_doc2vec()


