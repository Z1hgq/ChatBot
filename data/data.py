out1 = open('./question','w')
out2 = open('./answer','w')
count = 0
with open('./out.conv',encoding='UTF-8') as f:
	for line in f:
		if count % 2 == 0:
			out1.writelines(line)  
		if count % 2 == 1:
			out2.writelines(line)
		count += 1
		if count == 2000:
			break
		
	  