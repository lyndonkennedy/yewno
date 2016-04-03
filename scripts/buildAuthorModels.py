# Lyndon Kennedy
# 4/2/2016
# 
# buildAuthorModels.py
# 
# traverse over a collection of ebooks gathered from Project Gutenberg and build author
# models based on term frequency usage
#
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

doctrack = {};

tfs = {};
dfs ={};
norms = {};
# locations = {};

# iterate over training files
f = open('../lists/train_files.txt');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	# set stopping threshold
	if i<100000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print "processing",i,elapsed,filename;
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			# get book data
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				# process and normalize terms
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)
 				

				# add term counts to data structure
				if term not in stopwords:
					if term not in tfs:
						tfs[term] = {};
					if author not in tfs[term]:
						tfs[term][author] = 0;
					if author not in norms:
						norms[author] = 0;
						
					if term not in doctrack:
						doctrack[term] = {};
						dfs[term] = 0;
					if id not in doctrack[term]:
						doctrack[term][id] = True;
						dfs[term]+=1;

					tfs[term][author]+=1;
					norms[author]+=1;
					

f.close();


# write data files

fo = open('tfs.pkl','wb');
pickle.dump(tfs,fo);
fo.close();


fo = open('dfs.pkl','wb');
pickle.dump(dfs,fo);
fo.close();

fo = open('norms.pkl','wb');
pickle.dump(norms,fo);
fo.close();

