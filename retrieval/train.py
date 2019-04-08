import gensim
# import jieba
import pandas as pd
import os
import gensim.models as g
# import stopwordslist from main
from main import clean_words 

def cut_sentence():
    count = 0
    f_out = open('./data/qy_cut','w',encoding='utf-8')
    with open('./data/QingYun',encoding='utf-8') as f_in:
        for line in f_in:
            print(clean_words(line))
            f_out.writelines(str(clean_words(line)))
            print(count)
            count += 1
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
with open('./data/qy_cut',encoding='utf-8') as f:
    for line in f:
        sentences.append(line.rstrip(' \n'))
# print(X_train(sentences))

def train(x_train):
    model = g.Doc2Vec(x_train,min_count=1, window=10, vector_size=100, sample=1e-4, negative=5, workers=8)
    model.train(x_train,total_examples=model.corpus_count,epochs=10)
    return model

model_dm = train(X_train(sentences))

model_dm.save('models/ko_d2v.model')

# strl = '木兰当户织'
# test_text = strl.split(' ')

# inferred_vector = model_dm.infer_vector(doc_words=test_text,alpha=0.025,steps=500)

# sims = model_dm.docvecs.most_similar([inferred_vector],topn=10)

# for count,sim in sims:
#     print(count,sim)
#     sentence = sentences[count].strip(' ')
#     words = ''
#     for word in sentence:
#         words = words+word
#     print(words,sim,len(sentence))