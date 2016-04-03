# Lyndon Kennedy
# 4/2/2016
# 
# splitData.py
# 
# quick and dirty script to extract metadata and main text segments from a collection of
# Project Gutenberg ebooks
# 
# creates train set for authors with >4 books
# 
# holds out one book for test set
# 
import zipfile

i = 0;

books = {};
authors = {}

f = open('../lists/all_zip_files.txt');
for filename in f:
	filename = filename.strip();
	if filename[-6:] != "-0.zip" and filename[-6:] != "-8.zip":
		path_pieces = filename.split("/");
		id = path_pieces[len(path_pieces)-2];
		i+=1;
		print "processing:",str(i),id," - ",filename;

	

		try:
		
			zf = zipfile.ZipFile('../'+filename,'r');
			for txtname in zf.namelist():
				if '.txt' in txtname:
					x = zf.read(txtname)
			
			
				lines = x.split("\n");
				start = 0;
				stop = len(lines)-1;
		
				author = "";
				title = "";
				for l in range(len(lines)):
			
					line = lines[l];
								
					if start==0:
						if line.find("Author:")==0:
							author = line[7:].strip();
						if line.find("Title:")==0:
							title = line[7:].strip();
				
					if "*** START OF THIS PROJECT GUTENBERG EBOOK" in line or "*** START OF THE PROJECT GUTENBERG EBOOK" in line or "***START OF THIS PROJECT GUTENBERG EBOOK" in line or "***START OF THE PROJECT GUTENBERG EBOOK" in line:
						start = l;
					if "*** END OF THIS PROJECT GUTENBERG EBOOK" in line or "*** END OF THE PROJECT GUTENBERG EBOOK" in line  or "***END OF THIS PROJECT GUTENBERG EBOOK" in line  or "***END OF THE PROJECT GUTENBERG EBOOK" in line:
						stop = l;
		
			if author not in authors:
				authors[author] = [];
			authors[author].append(id);

			books[id] = {};
			books[id]['filename'] = filename;
			books[id]['author'] = author;
			books[id]['title'] = title;
			books[id]['start'] = str(start);
			books[id]['stop'] = str(stop);
		
		except:
			print "DROPPED",filename;
			
		
f.close();


# Various,Anonymous,Unknown,""

testids = [];
trainids = [];

for author,bookids in authors.iteritems():
	if author not in ['Various','Anonymous','Unknown',''] and len(bookids)>4:
		print author,bookids;
	
		testid = bookids.pop();
		testids.append(testid);
	
		for trainid in bookids:
			trainids.append(trainid);
		

fo = open('../lists/train_files.txt','w');
for id in trainids:
	filename = books[id]['filename'];
	author = books[id]['author'];
	title = books[id]['title'];
	start = books[id]['start'];
	stop = books[id]['stop'];
	
	outstr = "\t".join((id,filename,start,stop,author,title));
	fo.write(outstr+"\n");
	print outstr;
fo.close();


fo = open('../lists/test_files.txt','w');
for id in testids:
	filename = books[id]['filename'];
	author = books[id]['author'];
	title = books[id]['title'];
	start = books[id]['start'];
	stop = books[id]['stop'];
	
	outstr = "\t".join((id,filename,start,stop,author,title));
	fo.write(outstr+"\n");
	print outstr;
fo.close();

