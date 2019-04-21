from main import get_vectorValue
from main import readFile
from main import clean_words
import config
from app import chunks
from multiprocessing import Process

def process1(q1):
    count = 0
    out1 = open('./data/xhj/out_vec1','w',encoding='utf-8')
    for line in q1:
        strl = ''
        for e in get_vectorValue(clean_words(line)):
            strl += str(e) + ' '
        print('进程1进度：',count)
        out1.writelines(strl+'\n')
        count += 1
    out1.close()
def process2(q2):
    count = 0
    out2 = open('./data/xhj/out_vec2','w',encoding='utf-8')
    for line in q2:
        strl = ''
        for e in get_vectorValue(clean_words(line)):
            strl += str(e) + ' '
        print('进程2进度：',count)
        out2.writelines(strl+'\n')
        count += 1
    out2.close()
def process3(q3):
    count = 0
    out3 = open('./data/xhj/out_vec3','w',encoding='utf-8')
    for line in q3:
        strl = ''
        for e in get_vectorValue(clean_words(line)):
            strl += str(e) + ' '
        print('进程3进度：',count)
        out3.writelines(strl+'\n')
        count += 1
    out3.close()
def process4(q4):
    count = 0
    out4 = open('./data/xhj/out_vec4','w',encoding='utf-8')
    for line in q4:
        strl = ''
        for e in get_vectorValue(clean_words(line)):
            strl += str(e) + ' '
        print('进程4进度：',count)
        out4.writelines(strl+'\n')
        count += 1
    out4.close()
if (__name__ == "__main__"): 
    questionListPath ='./data/xhj/xhj1'
    questionList = readFile(questionListPath)

    q = chunks(questionList,4)
    
    p = Process(target=process1, args=(q[0],))
    p.start()
    p2 = Process(target=process2, args=(q[1],))
    p2.start()
    p3 = Process(target=process3, args=(q[2],))
    p3.start()
    p4 = Process(target=process4, args=(q[3],))
    p4.start() 



