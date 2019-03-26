## 训练

### seq2seq
python demo.py train

### 基于检索


进入retrieval目录，对话数据为main.py中的filePath，单行为问题 双行为答案
训练:`python3 main.py Train`

预测:`python3 main.py predict`

训练的过程其实是基于已有的中文单词向量表(main.py中的zh_vectorPath)把每一个问题转换成向量存储起来，在进行预测的时候将输入的问题转换成向量与已有的问题向量计算余弦相似度，最后输出相似度最高的问题的索引，最终根据索引在answerList中寻找答案


