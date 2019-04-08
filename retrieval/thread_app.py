import asyncio
import time
from main import readFile
from main import top5results_emb
import math
import sys
import datetime
import threading
questionListPath = './data/questionList'
answerListPath = './data/answerList'
questionListVecPath = './data/questionListVec'
questionList = readFile(questionListPath)
answerList = readFile(answerListPath)
vectorValueList = []
with open(questionListVecPath) as f:
    for line in f.readlines():
        tmpLst = line.rstrip(' \n').split(" ")
        vectorValueList.append([float(x) for x in tmpLst])
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]
result = []
q = chunks(questionList,4)
a = chunks(answerList,4)
v = chunks(vectorValueList,4)
questionList = []
answerList = []
vectorValueList = []
async def get_response(req,questionList,answerList,vectorValueList):
    await asyncio.sleep(0)
    print(top5results_emb(req,questionList,answerList,vectorValueList))

async def run(req):
    task1 = asyncio.create_task(get_response(req,q[0],a[0],v[0]))
    task2 = asyncio.create_task(get_response(req,q[1],a[1],v[1]))
    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2
def test(req):
    print(top5results_emb(req,q[0],a[0],v[0]))
def test1(req):
    print(top5results_emb(req,q[1],a[1],v[1]))
def test2(req):
    print(top5results_emb(req,q[2],a[2],v[2]))
def test3(req):
    print(top5results_emb(req,q[3],a[3],v[3]))
def thread_test(req):
    threading.Thread(target= test,args = (req,)).start()
    threading.Thread(target= test1,args = (req,)).start()
if __name__ == '__main__':
    while True:
        sys.stdout.write("> ")
        sys.stdout.flush()
        req = sys.stdin.readline()
        start2 = datetime.datetime.now()
        thread1 = threading.Thread(target= test,args = (req,))
        thread2 = threading.Thread(target= test1,args = (req,))
        thread3 = threading.Thread(target= test2,args = (req,))
        thread4 = threading.Thread(target= test3,args = (req,))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        threads = []
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        # 等待所有线程完成
        for t in threads:
            t.join()
        end2 = datetime.datetime.now()
        print ('回答用时:',end2-start2)
