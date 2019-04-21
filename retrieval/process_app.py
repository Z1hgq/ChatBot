import multiprocessing
from multiprocessing import Pipe, Process
import time
from main import readFile
from main import top5results_emb
import math
import sys
import datetime
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
q = chunks(questionList,2)
a = chunks(answerList,2)
v = chunks(vectorValueList,2)
questionList = []
answerList = []
vectorValueList = []
q1 = q[0]
a1 = a[0]
v1 = v[0]
q2 = q[1]
a2 = a[1]
v2 = v[1]
q = []
a = []
v = []
result = []
def son_process(out_pipe, in_pipe):
    _out_pipe, _in_pipe = out_pipe, in_pipe
    # 关闭fork过来的输入端
    _in_pipe.close()
    while True:
        try:
            req = _out_pipe.recv()
            result.append(top5results_emb(req,q2,a2,v2))
        except EOFError:
            # 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程
            break
def son_process2(out_pipe, in_pipe):
    _out_pipe, _in_pipe = out_pipe, in_pipe

    # 关闭fork过来的输入端
    _in_pipe.close()
    while True:
        try:
            req = _out_pipe.recv()
            result.append(top5results_emb(req,q1,a1,v1))
        except EOFError:
            # 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程
            break
if __name__ == '__main__':
    out_pipe, in_pipe = Pipe(True)
    out_pipe2, in_pipe2 = Pipe(True)
    son_p = Process(target=son_process, args=(out_pipe, in_pipe))
    son_p2 = Process(target=son_process2, args=(out_pipe2, in_pipe2))
    son_p.start()
    son_p2.start()
    # 等pipe被fork 后，关闭主进程的输出端
    # 这样，创建的Pipe一端连接着主进程的输入，一端连接着子进程的输出口
    out_pipe.close()
    out_pipe2.close()     
    while True:
        result = []
        sys.stdout.write("> ")
        sys.stdout.flush()
        req = sys.stdin.readline()
        in_pipe.send(req)
        in_pipe2.send(req)
        print(result)
    in_pipe.close()
    in_pipe2.close()
    son_p.join()
    son_p2.join()
