
f_out = open('../data/questionVecList','a',encoding='utf-8')

with open('./questionListVec',encoding='utf-8') as f:
    count = 0
    for line in f:
        f_out.writelines(line)
        print(count)
        count += 1
f_out.close()