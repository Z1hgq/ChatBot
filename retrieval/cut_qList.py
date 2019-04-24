from main import cut_sentence

fout = open('./data/xhj/xhjCut','w',encoding='utf-8')
count = 0
with open ('./data/xhj/questionList',encoding='utf-8') as f:
    for line in f:
        fout.writelines(cut_sentence(line))
        print(count)
        count += 1
