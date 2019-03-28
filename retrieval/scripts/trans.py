
def QingYun():
    fout = open('../data/QingYun','w')
    with open('../data/QingYun.yml',encoding='utf-8') as f:
        count = 0
        for line in f:
            if count%2==0:
                fout.writelines(line.lstrip('- - '))
            if count%2==1:
                fout.writelines(line.lstrip('  - '))
        count += 1
    fout.close()

def xiaohuangji():
    fout = open('../data/xiaohuangji','w')
    with open('../data/xiaohuangji.yml',encoding='utf-8') as f:
        count = 0
        for line in f:
            if count%2==0:
                fout.writelines(line.lstrip('- - '))
            if count%2==1:
                fout.writelines(line.lstrip('  - '))
        count += 1
    fout.close()
xiaohuangji()
