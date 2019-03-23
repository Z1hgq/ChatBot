import gensim
# import jieba
import pandas as pd
import os
import gensim.models.doc2vec as Doc2Vec
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
            if count == 10:
                break
    f_out.close()
cut_sentence()
