# coding: utf-8
from main import get_vectorValue
from main import readFile
from main import clean_words
import config
count = 0
out1 = open('./data/xhj/out_vec8','a',encoding='utf-8')
q = readFile('./data/xhj/xhj8')
for line in q:
    if count >= 24423:
        strl = ''
        for e in get_vectorValue(clean_words(line)):
            strl += str(e) + ' '
        out1.writelines(strl+'\n')
    print('进度：',count)
    count += 1
out1.close()