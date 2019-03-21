



# ### 6 基于词向量的文本表示
def top5results_emb(inputQuestion):
    def get_vectorValue(keywordList):
        filePath = "./data/glove.6B/glove.6B.100d.txt"
        vectorValueList = []
        with open(filePath, 'r', encoding='UTF-8') as r:
            for line in r.readlines():
                tmpLst = line.rstrip('\n').split(" ")
                word = tmpLst[0]
                if word in keywordList:
                    vectorValueList.append([float(x) for x in tmpLst[1:]])
        # 按关键词的平均，算句子的向量
        vectorSum = np.sum(vectorValueList, axis=0)
        return vectorSum / len(vectorValueList)
    
    inputQuestionKW = clean_words(inputQuestion)
    # input Question中的keywords
    input_question_vector = get_vectorValue(inputQuestionKW)
    simiVDict = {}
    filteredQuestionDict = filter_questionByInvertTab(inputQuestionKW, questionList, invertTable)
    for idx, question in filteredQuestionDict.items():
        # 取得当前问题的Vector值
        filtered_question_vector = get_vectorValue(clean_words(question))
        # 计算与输入问句的cos similarity
        simiVDict[idx] = 1 - distance.cosine(input_question_vector, filtered_question_vector)

    d = sorted(simiVDict, key=simiVDict.get, reverse=True)
    print(d)
    # Top5最相似问题对应的答案
    print("计算Top5相似-基于词向量及倒排表")
    for idx in d[:5]:
        print("问题：" + questionList[idx])
        print("答案：" + answerList[idx])  
print (top5results_emb("At what age did Frédéric move to Paris?"))