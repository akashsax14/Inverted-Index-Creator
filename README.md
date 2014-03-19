=====================================================================================================
Inverse Index Creator:
=====================================================================================================
=====================================================================================================
Pre-requisites : 
1) Compile the c parser files using the below two commands

gcc -c -fpic -I/usr/Python/include/python2.7 parsermodule.c parser.c

gcc -shared parser.o parsermodule.o -o parsermodule.so

2) The program assumes that the data files are present in a folder named "nz/". File naming is 
assumed to be as n_data and n_index where n is an integer. 

=====================================================================================================
Execution : 

1) To Execute, run indexer.py

2) Intermediate files are stored in folder named indexed(gets deleted depending upon user input)

3) The final index is stored in the same directory in a file named FINAL_INDEX.txt

=====================================================================================================
Known Issues :

1) Merging takes fairly more time as more and more files are read. This can be imporved in the next 
homework.

2) Final Index is not currently stored in binary format and words are present in string format as 
of now. Can be converted to binary form with a single iteration over the final index file.

=====================================================================================================
