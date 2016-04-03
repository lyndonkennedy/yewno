# Lyndon Kennedy
# 4/2/2016
# 
# common.py
# 
# common functions for processing ebooks and adding noise or selecting segments

import random

str = "abcdefghijklmnopqrstuvwxyz";
letters = list(str)

# add character level noise to noiseProb percent of characters
def addNoise(instr,noiseProb):
	inlist = list(instr);
	
	for i in range(len(inlist)):
		if random.random() < noiseProb:
			j = random.randint(0,len(letters)-1);
			inlist[i] = letters[j];
				
	return "".join(inlist);

# strip out the headers and footers from Project Gutenberg ebook and return body
def getMainText(booktext_raw,start,stop):
	lines = booktext_raw.split("\n");
	lines = lines[start+1:stop-1];
	booktext_body = "\n".join((lines));
	return booktext_body;


# get a random segment of sample_length words from booktext_body string
def getRandomSelection(booktext_body,sample_length):
	pieces = booktext_body.split();
	randstart = random.randint(0,len(pieces)-sample_length-1);
	randstop = randstart + sample_length;
	pieces = pieces[randstart:randstop];		
	return pieces;
	

