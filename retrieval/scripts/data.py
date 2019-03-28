# out1 = open('./question','w')
# out2 = open('./answer','w')
# count = 0
# with open('./out.conv',encoding='UTF-8') as f:
# 	for line in f:
# 		if count % 2 == 0:
# 			out1.writelines(line)  
# 		if count % 2 == 1:
# 			out2.writelines(line)
# 		count += 1
# 		if count == 2000:
# 			break

import jieba
inputFile = open('../data/QingYun', 'rb')
outputFile = open('../data/QingYun_fenci.txt','w', encoding='utf-8')

lines = inputFile.readlines()

# 为每一行文字分词
for i in range(len(lines)):
    line = lines[i]
    if line:
        line = line.strip()
        seg_list = jieba.cut(line)

        segments = ''
        for word in seg_list:
            segments = segments + ' ' + word
        segments += '\n'
        segments = segments.lstrip()
        # 将分词后的语句，写进文件中
        outputFile.write(segments)

inputFile.close()
outputFile.close()


#cat text.txt | tr " " "\n" | sort -u > wordlist.txt
		
	  