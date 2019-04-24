# coding: utf-8
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

db = client['chatbot']
collection = db['xhj']


questionArr = open('../data/xhj/questionList')
answerArr = open('../data/xhj/answerList')
vectorArr = qestion = open('../data/xhj/questionListVec')

count = 0
for q,a,v in zip(questionArr,answerArr,vectorArr):
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
