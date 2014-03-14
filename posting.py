def make_inter_posting(interim_index, posting, page_id):
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
