# Lyndon Kennedy
# 4/2/2016
# 
# createRNNDataFiles.py
# 
# quick and dirty script to dump input ebooks into concatenated files for training
# recurrent neural networks

import zipfile
import string
import time
import pickle

start_time = time.time();


# count term frequencies in training set
tfs = {};
i =0;

f = open('../data/rnn/melville/train_list.txt');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	if i<100000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print "processing",i,elapsed,filename;
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)
 				

				if term not in tfs:
					tfs[term] = 0;
				tfs[term]+=1;					
f.close();	

				
tf_tups = [];
for term,count in tfs.iteritems():
	tf_tups.append((count,term));

tf_tups.sort(reverse=True);
tf_tups = tf_tups[:9999];

# keep top 9999 terms
tfs = {}
for tup in tf_tups:
	count,term = tup;
	tfs[term] = True;
	

# process training set
f = open('../data/rnn/melville/train_list.txt');
fo = open('../data/rnn/melville/ptb.train.txt','w');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	if i<100000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print "processing",i,elapsed,filename;
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)
 				

				if term not in tfs:
					term = "<unk>";
				
				fo.write(term+" ");
		
fo.close();
f.close();	

# process validation set
f = open('../data/rnn/melville/valid_list.txt');
fo = open('../data/rnn/melville/ptb.valid.txt','w');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	if i<100000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print "processing",i,elapsed,filename;
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)
 				

				if term not in tfs:
					term = "<unk>";
				
				fo.write(term+" ");
		
fo.close();
f.close();	


# process test set
f = open('../data/rnn/melville/test_list.txt');
fo = open('../data/rnn/melville/ptb.test.txt','w');
for trainitem in f:
	(id,filename,start,stop,author,title) = trainitem.strip().split("\t");
	start = int(start);
	stop = int(stop);
	
	if i<100000:
		i+=1;
		elapsed = time.time() - start_time;
		
		print "processing",i,elapsed,filename;
		
		zf = zipfile.ZipFile('../'+filename,'r');
		for txtname in zf.namelist():
			if '.txt' in txtname:
				booktext_raw = zf.read(txtname)
			
			lines = booktext_raw.split("\n");
			lines = lines[start+1:stop-1];
			booktext_body = "\n".join((lines));
			
					
			pieces = booktext_body.split();
			j = 0;
			for term in pieces:
				term = term.lower();
				term = term.translate(string.maketrans("",""), string.punctuation)
 				

				if term not in tfs:
					term = "<unk>";
				
				fo.write(term+" ");
		
fo.close();
f.close();	