# coding: utf-8
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)

db = client['chatbot']
collection = db['qingyun']

result = collection.find({'question': {'$regex':".*我爱你.*|.*你爱我.*"}})
# print(len(result))
for line in result:
    print(line['question'])
client.close()