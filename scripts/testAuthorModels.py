# Lyndon Kennedy
# 4/2/16
# 
# testAuthorModels.py
# 
# run a test at various query lengths and noise levels to measure accuracy of predicting
# the author of a segment of text
# 
import zipfile;
import pickle;
import random;
import string;
import math;
import common;


# initialize experimental conditions
sample_lengths = [10, 100, 1000];
noise_levels = [0,.01,.1,.5];

scores = {}


# load data models
print "Loading database..."
f = open('../models/authors/tfs.pkl','rb');
tfs = pickle.load(f);
f.close();

f = open('../models/authors/dfs.pkl','rb');
dfs = pickle.load(f);
f.close();

f = open('../models/authors/norms.pkl','rb');
norms = pickle.load(f);
f.close();
print "Done."

# open output destination
fo = open('../outputs/scores_authors.txt','w');

# iterate through experimental conditions
for sample_length in sample_lengths:
	scores[sample_length] = {};
	
	for noise_level in noise_levels:


		f = open('../lists/test_files.txt');

		matched = 0.0;
		tested = 0.0;
		
		#iterate through test files
		for testitem in f:
			(id,filename,start,stop,author,title) = testitem.strip().split("\t");
			start = int(start);
			stop = int(stop);

			try:
				zf = zipfile.ZipFile('../'+filename,'r');
				for txtname in zf.namelist():
					if '.txt' in txtname:
						booktext_raw = zf.read(txtname)
	
						# get main text
						booktext_body = common.getMainText(booktext_raw,start,stop);

						# get random sample
						pieces = common.getRandomSelection(booktext_body,sample_length);	
	
	
						authorsims = {};
	
						for term in pieces:
							#clean terms
							term = term.lower();
							term = term.translate(string.maketrans("",""), string.punctuation)
							# add noise
							term = common.addNoise(term,noise_level);

		
							# lookup terms
							if term in tfs:
								for author_search,counts in tfs[term].iteritems():
									if author_search not in authorsims:
										authorsims[author_search] = 0;
									# add up similarity
									authorsims[author_search] += ((1+math.log(counts)) / (dfs[term]*norms[author_search]*1.0));
	
						# find highest scoring
						score_tups = [];
						for author_search,score in authorsims.iteritems():
							score_tups.append((score,author_search));
						score_tups.sort(reverse=True);
		
						if len(score_tups)>0:
							top_score,top_author = score_tups[0];
						else:
							top_score = 0;
							top_author = -1;
							
						# evaluate correctness
						if top_author == author:
							matched+=1;
							ishit = "CORRECT";
						else:
							ishit = "WRONG";
						tested+=1;
		
						hitrate = matched / tested;
		
						hitpos = -1;
						for depth in range(len(score_tups)):
							curr_tup = score_tups[depth];
							curr_score,curr_author = curr_tup;
							if curr_author == author:
								hitpos=depth;
		
						print ishit,sample_length,noise_level,top_score,hitrate,hitpos,top_author,author
			
			except:
				print "skipped";			
		
		# write performance scores
		scores[sample_length][noise_level] = hitrate;	
		outstr = "\t".join((str(sample_length),str(noise_level),str(hitrate)));
		fo.write(outstr+"\n");		
		
		f.close();

fo.close();