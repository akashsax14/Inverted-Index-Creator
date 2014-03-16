import os
import ast
#from sys import stdout
#import shutil

def merge(doc_id):
	try:
		if doc_id == 0:
			os.system('cp indexed/index_0.txt indexed/index_X0.txt')
		else:
			f0 = open('indexed/index_X' + str(doc_id-1) + '.txt', 'r+')
			lines0 = f0.readlines()
			l0 = len(lines0)
			
			f1 = open('indexed/index_'+ str(doc_id) +'.txt', 'r+')
			lines1 = f1.readlines()
			l1 = len(lines1)
			
			f = open('indexed/index_X' + str(doc_id) + '.txt', 'w+')
			#f = open('indexed/index_temp.txt', 'w+')
			
			c0 = 0	#for index_0
			c1 = 0	#for index_1
			while c0<l0 and c1<l1:
				line0 = lines0[c0].split(':-:')
				word0 = line0[0]
				list0 = ast.literal_eval(line0[1])
				
				line1 = lines1[c1].split(':-:')
				word1 = line1[0]
				list1 = ast.literal_eval(line1[1])
				
				if word0 == word1:
					f.write(word0+':-:'+str(list0 + list1)+':-:\n')
					c0 += 1
					c1 += 1
				if word0 < word1:
					f.write(word0+':-:'+str(list0)+':-:\n')
					c0 += 1
				if word1 < word0:
					f.write(word1+':-:'+str(list1)+':-:\n')
					c1 += 1
					
			#print c0, l0
			#print c1, l1	
			if c0 == l0 and c1 <> l1:
				#print "c0 finished first"
				while c1 < l1:
					line1 = lines1[c1].split(':-:')
					word1 = line1[0]
					list1 = ast.literal_eval(line1[1])
					f.write(word1+':-:'+str(list1)+':-:\n')
					c1 += 1
			elif c1 == l1 and c0 <>l0:
				#print "c1 finished first"
				while c0 < l0:
					line0 = lines0[c0].split(':-:')
					word0 = line0[0]
					list0 = ast.literal_eval(line0[1])
					f.write(word0+':-:'+str(list0)+':-:\n')
					c0 += 1
			
			#shutil.copy('indexed/index_temp.txt', 'indexed/index_final.txt')
			#os.system('cp indexed/index_temp.txt indexed/index_final.txt')
			os.system('rm indexed/index_X' + str(doc_id-1) + '.txt')
					
			f0.close()
			f1.close()
			f.close()
			
	except Exception as e:
		f0.close()
		f1.close()
		f.close()
		print "Exception in Merge : " + str(e)

#merge(0)
#merge(1)
