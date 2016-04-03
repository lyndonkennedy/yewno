# Lyndon Kennedy
# 4/2/16
# 
# testMatchingModels.py
# 
# run a test at various query lengths and noise levels to measure accuracy of predicting
# the source of a segment of text
# 
import zipfile;
import pickle;
import random;
import string;
import math;
from collections import Counter
import common;


# set experimental conditions
sample_lengths = [10, 100, 1000];
noise_levels = [0,.01,.1,.5];

# initialize scores array
scores = {}


# load the location model
print "Loading database..."
f = open('../models/matching/locations_1000.pkl','rb');
locations = pickle.load(f);
f.close();
print "Done."

# open output file
fo = open('../outputs/scores_matching.txt','w');

# iterate through experimental conditions
for sample_length in sample_lengths:
	scores[sample_length] = {};
	
	for noise_level in noise_levels:

		# read test files
		f = open('../lists/train_files.txt');

		matched = 0.0;
		tested = 0.0;

		i = 0;
		
		# iterate through test files
		for testitem in f:
			(id,filename,start,stop,author,title) = testitem.strip().split("\t");
			start = int(start);
			stop = int(stop);

			# for speed, only consider the first 1000 files
			if i < 1000:
				i+=1;
				try:
					zf = zipfile.ZipFile('../'+filename,'r');
					for txtname in zf.namelist():
						if '.txt' in txtname:
							booktext_raw = zf.read(txtname)
	
						# get body text
						booktext_body = common.getMainText(booktext_raw,start,stop);

						# get a random segment
						pieces = common.getRandomSelection(booktext_body,sample_length);
	
						docoffsets = {};
	
						j = 0;
						for term in pieces:
							# clean terms
							term = term.lower();
							term = term.translate(string.maketrans("",""), string.punctuation)
		
							# add noise
							term = common.addNoise(term,noise_level);
		
							#look up terms
							if term in locations:
								for id_search,locs in locations[term].iteritems():
					
									if id_search not in docoffsets:
										docoffsets[id_search] = [];
					
									for loc in locs:
										docoffsets[id_search].append(loc-j);

							j+=1;			
	
						score_tups = [];
						
						# get offset statistics
						for id_search,offsets in docoffsets.iteritems():
							data = Counter(offsets);
							score = data.most_common(1)[0][1];
			
							score_tups.append((score,id_search));

						score_tups.sort(reverse=True);
		
						# get top match
						if len(score_tups)>0:
							top_score,top_id = score_tups[0];
						else:
							top_score = 0;
							top_id = -1;
		
						# evaluate for correctness
						if top_id == id:
							matched+=1;
							ishit = "CORRECT";
						else:
							ishit = "WRONG";
						tested+=1;
		
						hitrate = matched / tested;
		
						hitpos = -1;
						for depth in range(len(score_tups)):
							curr_tup = score_tups[depth];
							curr_score,curr_id = curr_tup;
							if curr_id == id:
								hitpos=depth;
		
						print ishit,sample_length,noise_level,top_score,hitrate,hitpos,top_id,id
				except:
					print "skipped";		
		
		# write results
		scores[sample_length][noise_level] = hitrate;	
		outstr = "\t".join((str(sample_length),str(noise_level),str(hitrate)));
		fo.write(outstr+"\n");

		f.close();
		


fo.close();
