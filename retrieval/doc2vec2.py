# coding: utf-8
from main import get_vectorValue
from main import readFile
from main import clean_words
import config
count = 0
out1 = open('./data/xhj/out_vec5','w',encoding='utf-8')
q = readFile('./data/xhj/xhj5')
for line in q:
    strl = ''
    for e in get_vectorValue(clean_words(line)):
        strl += str(e) + ' '
    print('进度：',count)
    out1.writelines(strl+'\n')
    count += 1
out1.close()