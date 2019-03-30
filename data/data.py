# out1 = open('./Q','w')
# out2 = open('./A','w')
out = open('./xhj_data','w')
count = 0
with open('./out.conv',encoding='UTF-8') as f:
	for line in f:
		# if count % 2 == 0:
		# 	out1.writelines(line)  
		# if count % 2 == 1:
		# 	out2.writelines(line)
		out.writelines(line)
		count += 1
		print(count)
		if count == 20000:
			break
out.close()
		
	  