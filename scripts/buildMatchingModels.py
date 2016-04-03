# Lyndon Kennedy
# 4/2/2016
# 
# buildMatchingModels.py
# 
# ingest a set of books from Project Gutenberg and index term locations

import zipfile
import string
import time
import pickle

# load stopwords
stopwords = {};
f = open('../data/stopwords/stopwords.txt');
for line in f:
	term = line.strip();
	stopwords[term] = True;
f.close();


start_time = time.time()


i = 0;

locations = {};

# iterate over items
f = open('../lists/train_files.txt');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	if i<1000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print("processing",i,elapsed,filename);
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			# process book text
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				# normalize words
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)

 				
				# index words in data structure
				if term not in stopwords:
				
					if term not in locations:
						locations[term] = {};
					if id not in locations[term]:
						locations[term][id] = [];

					locations[term][id].append(j);

				j+=1;					

f.close();


# write models
fo = open('../models/matching/locations_1000.pkl','wb');
pickle.dump(locations,fo);
fo.close();


