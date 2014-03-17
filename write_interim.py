#======================================================================#
# Writes the data of an intermediate index for a single data file into #
# a file. Called for every data file.                                  #
# Inverted index is created by deleimiting word and list of doc ids    #
# by :-: character for future parsing and merging of index files       #
#======================================================================#
def write_interim(interim_index, doc_id, debug_flag, compression_flag):
	try:	
		index_rw = open('indexed/index_'+ str(doc_id) +'.txt', 'w+')
		
		#Compressing intermediate index by representing list of doc_ids as difference in doc_ids
		if compression_flag:
			for k, v in interim_index.iteritems():
				l = len(v)
				c = l-1
				while c >= 1:
					v[c] = v[c] - v[c-1]
					c -= 1
		
		#Sorting inverted index based on word(dictionary key)
		sorted_interim_index = sorted(interim_index)
		
		#Writing the intermediate inverted index for a single data file
		for k in sorted_interim_index:
			if compression_flag:
				#Adding a "|" character for delimiting a section of compression for each data file
				index_rw.write(k+':-:'+str(interim_index[k]+['|'])+':-:\n')
			else:
				index_rw.write(k+':-:'+str(interim_index[k])+':-:\n')
			
		index_rw.close()
	except Exception as e:
		index_rw.close()
		if debug_flag:
			print "Exception in Write_Interim : " + str(e)
		pass
#=======================================================================
