import gzip,parser, time, os
from sys import stdout
from merge import merge
from collections import defaultdict
from posting import make_inter_posting
from write_interim import write_interim
#======================================================================#
# The main method which initializes the inverted index creation. It    #
# takes in the number of files for which the index is to be prepared.  #
# Depending on user input it prepares a document-to-url mapping file   #
# along with the main inverted index. It also prepares a bunch of      #
# intermediate index files which the user may choose to save or delete.#
#======================================================================#
def indexer():
	try:	
		print separator+'='*29+"INVERTED INDEX CREATOR"+'='*29+'\n'+separator
		
		n = int(raw_input("Enter the number of files to be indexed: "))
		
		compression_choice = raw_input("\nDo you want to compress inverted index(y/n): ")
		compression_flag = False
		if compression_choice == "y" or compression_choice == "Y":
			compression_flag = True
		
		doc_id_choice = raw_input("Do you want to create Document Id Mapper(y/n): ")
		doc_id_flag = False
		if doc_id_choice == "y" or doc_id_choice == "Y":
			doc_id_flag = True
			
		delete_choice = raw_input("Do you want keep intermediate files(y/n): ")
		delete_flag = True
		if delete_choice == "y" or delete_choice == "Y":
			delete_flag = False
		
		debug_choice = raw_input("Run in debug mode(y/n): ")
		debug_flag = False
		if debug_choice == "y" or debug_choice == "Y":
			debug_flag = True
		
		print "\n"
				
		#Specify the path of folder where the data files are kept
		file_path = "nz2_merged/"
		page_id = 0
		start_time = time.time()
		
		#Specify the file details which would store doc-to-url mapping
		if doc_id_flag:
			doc_id_url = open("doc_ids.txt", "w+")
		
		if not os.path.exists("indexed"):
			os.makedirs("indexed")
			
		#Iterating over each data file
		for i in range(0,n):
			#Interim index dictionary for each data file
			interim_index = defaultdict(list)
			length = 0
			start = 0
			end = 0
			doc_counter = 0
			
			#Uncompressing and opening the index file
			gz_file_index = gzip.open(file_path + str(i) + "_index", 'rb')
			index = gz_file_index.readlines()
			gz_file_index.close()
			
			#Uncompressing and opening the data file
			gz_file_content = gzip.open(file_path + str(i) + "_data", 'rb')
			content = gz_file_content.read()
			gz_file_content.close()
			
			#Iterating over every document in a given single data file
			while end < len(content) and doc_counter < len(index):
				start = end
				page_details = index[doc_counter].split()
				
				url = page_details[0]
				length = int(page_details[3])
				status = page_details[6]
				
				doc_counter += 1
				page_id += 1
				end = end + length
				
				#If the status of current page is not "OK" move to next page
				if status <> 'ok':
					continue
				
				try:
					page = content[start:end]
					pg = page
					
					#Using the C Parser provided
					tokenized_str = parser.parser(url, page, pg, length+1, length+1)[1]
					
					#Write docId-url mapping
					if doc_id_flag:
						doc_id_url.write(str(page_id)+" : "+str(url)+"\n")
					
					#Creating intermediated posting for every document/page
					interim_index = make_inter_posting(interim_index, tokenized_str, page_id, debug_flag)
					
					current_time = time.time()
					#stdout.write("\rPages Parsed : %i | Files Read : %i | Time Elapsed : %i secs" % (page_id, (i+1), (current_time - start_time)))
					stdout.write("\rFiles Read : %i | Time Elapsed : %i secs" % ((i+1), (current_time - start_time)))
					stdout.flush()
					
				except TypeError as te:
					pass
			
			#For every data file, once interim index is created wite it to disk		
			write_interim(interim_index, i, debug_flag, compression_flag)
			
			#Merging Interim index into temporary file
			merge(i, start_time, debug_flag)
			
			#Depending on user input, delete or keep intermediate files
			if delete_flag:
				os.system('rm indexed/index_' + str(i) + '.txt')
				
		#Making the final file which will contain the final index
		os.system('mv indexed/index_X' + str(n-1) + '.txt FINAL_INDEX.txt')
		
		#Closing all open files
		if doc_id_flag == "y" or doc_id_flag == "Y":
			doc_id_url.close()
		gz_file_index.close()
		gz_file_content.close()
		if delete_flag:
			os.rmdir("indexed")
		
		print "\n" + separator +"="*36 +"SUMMARY"+"="*37
		print "Final Inverted Index : Final_Index.txt"
		print "File Size : " + str(int(os.path.getsize('FINAL_INDEX.txt'))/1.049e+6) + " Mb"
		print separator+separator
	except Exception as e:
		if debug_flag:
			print "Error in Reading Data : " + str(e)
		if doc_id_flag:
			doc_id_url.close()
		gz_file_index.close()
		gz_file_content.close()
#=======================================================================			
# GLOBAL VARIABLES
separator = '=' * 80 + '\n'
#=======================================================================
def main():
	indexer()
#=======================================================================
if __name__ == "__main__":
	main()
#=======================================================================
