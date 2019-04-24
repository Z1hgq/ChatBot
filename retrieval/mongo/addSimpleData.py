# coding: utf-8
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

db = client['chatbot']
collection = db['xhj_simple']

keywordArr = open('../data/xhj/xhjCut')
questionArr = open('../data/xhj/questionList')
answerArr = open('../data/xhj/answerList')
vectorArr = qestion = open('../data/xhj/questionListVec')

count = 0
for k,q,a,v in zip(keywordArr,questionArr,answerArr,vectorArr):
    if k.rstrip(' \n') == '' or k.rstrip(' \n') == ' ':
        obj = {
        "question":q.rstrip(' \n'),
        "answer":a.rstrip(' \n'),
        "vector":v.rstrip(' \n')
        }
        collection.insert_one(obj)
    print(count)
    count += 1
    # if count == 10:
    #     break
questionArr.close()
answerArr.close()
vectorArr.close()

client.close()
