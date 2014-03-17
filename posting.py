#======================================================================#
# This module creates an intermediate posting for a single page in a   #
# given data file and saves it in a default dictonary.                 #
#======================================================================#
def make_inter_posting(interim_index, posting, page_id, debug_flag):
	try:	
		line = posting.split('\n')
		word_set = []
		for word in line:
			s_word = word.split()
			try:
				word_set.append(s_word[0])
			except:
				pass
		word_set = list(set(word_set))
		for word in word_set:
			interim_index[word].append(page_id)
		return interim_index
	except Exception as e:
		if debug_flag:
			print "Exception in Posting : "+ str(e)
		pass
#=======================================================================
