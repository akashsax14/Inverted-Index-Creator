import os
from collections import defaultdict
import zlib
import base64

def write_interim(interim_index, doc_id):
	try:	
		index_rw = open('indexed/index_'+ str(doc_id) +'.txt', 'wb+')
		#index_rwc = open('indexed/index_'+ str(doc_id) +'c.txt', 'wb+')
		
		sorted_interim_index = sorted(interim_index)
		
		#open("temp.txt", 'w+').write(str(sorted_interim_index)+'\n')
		for k in sorted_interim_index:
			index_rw.write(k+':-:'+str(interim_index[k])+':-:\n')
			#index_rw.write(k+' '+str(v)+'\n')
		index_rw.seek(0)
		file_content = index_rw.read()
		compressed_content = base64.b64encode(zlib.compress(file_content))		
		index_rw.close()
		with open('indexed/index_'+ str(doc_id) +'.txt', 'wb+') as fp:
			fp.write(compressed_content)
		#os.system('sort -f -o indexed/index_'+str(doc_id)+'.txt indexed/index_'+str(doc_id)+'.txt')
	except Exception as e:
		index_rw.close()
		#index_rwc.close()
		print "Exception in Write_Interim : " + str(e)
		pass
		
