# coding: utf-8
import scipy.spatial.distance as distance
count = 0
vectorValueList = []
with open('./data/questionListVec') as f:
    for line in f.readlines():
        tmpLst = line.rstrip(' \n').split(" ")
        print(tmpLst)
        vectorValueList.append([float(x) for x in tmpLst])
        print(vectorValueList)
        if count == 10:
            break
        count += 1
cosdis=1 - distance.cosine(vectorValueList[0], vectorValueList[1])
print(cosdis)
