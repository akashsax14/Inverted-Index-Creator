import os
from collections import defaultdict
def write_interim(interim_index, doc_id):
	try:	
		index_rw = open('indexed/index_'+ str(doc_id) +'.txt', 'w+')
		
		sorted_interim_index = sorted(interim_index)
		
		for k in sorted_interim_index:
			index_rw.write(k+':-:'+str(interim_index[k])+':-:\n')
			#index_rw.write(k+' '+str(v)+'\n')
		index_rw.close()
		#os.system('sort -f -o indexed/index_'+str(doc_id)+'.txt indexed/index_'+str(doc_id)+'.txt')
	except Exception as e:
		index_rw.close()
		pass
		#print "Exception in Write_Interim : " + str(e)
