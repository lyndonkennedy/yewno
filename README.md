#Data Modeling for Sequence Matching

##Data Preparation

I started by gathering a collection of ebooks from Project Gutenberg. I ran this wget command to get plain text copies of ebooks in English:
```
wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"
```

This ended up returning 36563 files. I then ran my `splitData.py` script to extract metadata about each book (author, title) and to detect the beginning and end points of the actual body text using simple heuristics. I counted the number of books that each author had written in the dataset and kept books by authors who had written 5 or more books. This yielded 704 unique authors (excluding "Anonymous," "Various," "Unknown," etc.) contributing 8510 total books. I held out one book for each author for a test set and used the remaining books to build a training set.


##Task 1: Document Matching

This noisy exact-match retrieval problem reminded me of audio fingerprinting and Shazam. Shazam detects audio landmark events in sound files and uses the main insight that the correct match to a query will have a lot of matches that have the same temporal offset from the query. I mapped this formulation onto the text matching problem by treating words as the "landmarks" and indexing the word positions in each document (omitting a standard stopword list, stripping punctuations, and going to lowercase). For each term in a query, we then look up its corresponding locations(s) in each document and tabulate a histogram of offsets between the document location of matching terms and their locations in the query string.

To evaluate, I used a subset of 1000 of the ebooks (to keep model loading time small for iterating and evaluating). I then queried against this database with those same 1000 ebooks. For each book, I selected a random continuous sequence of words. I chose to model the noise as character-level: given an N% noise level, each character has a N% chance of being randomly replaced with a randomly-selected lower-case alphabetic character. I find the occurrences of all matching terms in the document index and calculate the offsets between their locations and the location of the term in the query. I then find the mode of the distribution of offsets for each document-query pair and return the document that has the most query terms occurring at the mode offset as the suggested match.

I run this using queries of 10, 100, and 1000 terms and noise levels at 0%, 1%, 10%, and 50%.

Length	|	Noise	|	% Correct
------	|	-----	|	---------
10	|	0	|	0.752
10	|	0.01	|	0.741
10	|	0.1	|	0.467
10	|	0.5	|	0.007
100	|	0	|	0.876
100	|	0.01	|	0.867
100	|	0.1	|	0.86
100	|	0.5	|	0.178
1000	|	0	|	0.893


At 0% noise, the system is highly accurate with only a few query terms. As noise increases, system performance degrades, however. The trade-off is between query length and noise level. Even if 50% of characters are being switched, overall performance remains strong. (High frequency of character-level swapping leads to an even higher level of terms being corrupted). I estimate that if ~5 terms make it through the noise process, then retrieval should be fairly robust.

I further observed that in a significant portion of the errors in low-noise retrieval, the correct match was ranked 2nd. This might be due to noisy data: some segments of text are duplicated between books, such as individual short stories and collections.

```
# train
python buildMatchingModels.py

# test
python testMatchingModels.py
```

##Task 2: Author Prediction

Predicting the author of a passage of text can be achieved by using some sort of vector space representation of the terms. To approach this, I counted the frequency with which each author uses that term. I further keep track of the total number of terms used by each author and the number of documents that each term appears in. I leave out a standard stopword list.

To evaluate, I created an index using all of the available training books (this model is lighter-weight than the Document Matching model and experimentation can happen faster with this larger model). I then query the model using each of the books in the test set. I select a random continuous segment of words from the book and then apply a random character-level noise addition (as above).

```
# train
python buildAuthorModels.py

# test
python testAuthorModels.py
```

Length	|	Noise	|	% Correct
------	|	-----	|	---------
10	|	0	|	0.0553977272727
10	|	0.01	|	0.0440340909091
10	|	0.1	|	0.0284090909091
10	|	0.5	|	0.00426136363636
100	|	0	|	0.167142857143
100	|	0.01	|	0.125714285714
100	|	0.1	|	0.0542857142857
100	|	0.5	|	0.00428571428571
1000	|	0	|	0.250363901019
1000	|	0.01	|	0.213973799127
1000	|	0.1	|	0.113537117904
1000	|	0.5	|	0.00436681222707

Given queries of 1000 terms, we can achieve 25% accuracy in selecting the correct author (random chance is less than .1%). Adding noise degrades this performance rapidly. It is difficult to model authors with only 10 or 100 terms.

Given more time and/or clearer targets to achieve, I might have explored using bigram or trigrams instead of the single terms that I had used to see if these might model the peculiarities of individual authors better. Another approach that might work would be building discriminative models on top of these vector space representations and applying these models to test sequences. Recurrent neural networks (discussed below) trained individually for each author might also give language-modeling scores for each test sequence against each author.

##Task 3: Continuation Prediction

Since this part was optional, I took it as an opportunity to step outside of my comfort zone and learn a bit about techniques that I had not previously had any experience in. I thought the task seemed like a good fit for recurrent neural networks and I had been recently starting to learn more about TensorFlow, so I dove in a tried to train a network. I thought author-specific prediction seemed like the most feasible task to undertake. I trained one network for Herman Melville using the books he had in my training set. My personal machine is a mid-2010 iMac (and TensorFlow doesn't support GPUs for Mac), so it took ~6 hours to train a fairly small network on Herman Melville books. 

The basis for this modeling was somewhat different than the above two tasks, since stopwords are important for natural language here. I prepare the texts by cutting them down to their most frequent 10000 terms, encoding unknown terms as `<unk>`. These functions are done in the `createRNNDataFiles.py` script.

I evaluated this qualitatively by feeding in a randomly-selected contiguous sequence from the test Melville book, "Omoo: Adventures in the South Seas," and then generating the next most likely term returned by the network. I then continuously feed the next predicted term back into the network to get the following term. I repeat this to get a predicted string of equal length to the input string. The resulting strings are amusing to look at and seem somewhat Melville-ian in that they are often about whales, ships, and the sea and have some semblance of english grammar.

We could evaluate quantitatively by measuring word error rate or perplexity against the true sequence continuation, but the model doesn't seem to be sophisticated enough yet to merit this level of evaluation. Nonetheless, I will probably proceed on my own time to experiment with more sophisticated models, better representations of sentence structure, and modeling other authors to see what's possible with RNNs.

The RNNs are adapted directly from the example code provided in the TensorFlow tutorial (I didn't even change the filenames). I added a function to iteratively feed through the output to generate longer output predictions. I also added functionality to save the learned model and to directly access the vocabulary from the numerical representations.

```
# train
python ptb_word_lm.py --data_path=../data/rnn/melville/ --train=True

# test
python ptb_word_lm.py --data_path=../data/rnn/melville/ > ../outputs/predicted_continuations.txt
```

Included below is some sample output.

```
test sequence 38
input string:
manilla hat large and portly he was also hale and fifty with a complexion like an autumnal <unk> blue <unk> teeth and a <unk> <unk> <unk> in short he was an <unk> father <unk> by name and as such pretty well known and very thoroughly <unk> throughout all the <unk> missionary settlements in polynesia in early youth he had been sent to a religious <unk> in france and taking orders there had but once or twice afterwards <unk> his native land father <unk> marched up to us briskly and the first words he uttered were to ask whether there were

predicted continuation:
one of the people of the crew that they were not very long in the morning and the next day we were engaged in the course of the vessel we had been sailing in the valley and in the same direction the islanders in the course of the island were the most remarkable of all the islands of the natives who had not been so much inclined to believe that the inhabitants of the valley were in the habit of a free tribe and the only one was the most famous of their number and with them all that was 
```

I didn't implement it, but in the case that Task 1 is able to find a matching document for the sequence, we will also know the offset at which the query string begins in the document. From there, we can deterministically continue the string until the end of the document is reached.


##Scalability Issues

As mentioned above, these experiments were conducted using an old machine on relatively small amounts of data. Some of these functions can be implemented efficiently for large-scale batch operations on a Hadoop cluster.

Consider having an entire library represented as a series of tuples `<document_id>,<term_id>,<position>`:

```
moby_dick,call,1
moby_dick,me,2
moby_dick,ishmael,3
....
```
Then having a series of queries represented in the same format, we could execute batch matching between queries and documents using a PIG script not unlike this pseudocode:

```
queries = LOAD queries USING LoaderMethod AS (q_id,q_term_id,q_offset);
docs = LOAD docs USING LoaderMethod AS (docid,doc_term_id,doc_offset);

joined = JOIN queries USING q_term_id, docs USING doc_term_id;
joined = FOREACH joined GENERATE
	docid,
	q_id,
	q_offset - doc_offset as offset;

grouped = GROUP joined BY (docid,q_id,offset);
joined_offset_counts = FOREACH grouped GENERATE
	group.$0 as docid,
	group.$1 as q_id,
	group.$2 as offset,
	COUNT(joined) as n;

grouped_offsets = GROUP offsets BY (docid,qid);
scores = FOREACH grouped_offsets GENERATE
	group.$0 as docid,
	group.$1 as qid,
	MAX(joined.n) as score;
```	

This returns a bag of tuples specifying the score similarity between any document and any query. We can then further manipulated this to return the closest match or threshold to reject.

We could apply a similar modeling approach to predicting authors for query strings but by counting term frequencies rather than locations. A more reasonable approach, however, might be to distribute the search sets by authors across many mappers. The mappers can then return the top-N closest authors and scores within their sets and a reducer can aggregate these with a guarantee of finding the true top-N closest authors.

It would probably be premature to consider parallelizing the continuation prediction framework, but models like this can be applied to any input directly on the mappers.


##Feature Selection

The way that I have set up these models, there is less opportunity for feature selection. 

For the matching task we have tried to omit stopwords since they might add more noise in the offset counting than signal. We could analytically generate such a list by finding the terms that have high entropy in their locations and therefore don't provide much signal.

Similarly, if we were to revisit the author prediction task as a more traditional supervised/discriminative task, we might be able to see which terms are most predictive through standard methods.


##Performance Assessment

I have broken out the evaluations, both actually-done and speculatively-conceived-of, of each task directly in the corresponding notes above.

