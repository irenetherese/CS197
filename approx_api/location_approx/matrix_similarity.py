from gensim import corpora, similarities
from gensim.models.lsimodel import LsiModel
import pandas as pd
import random
from location_approx.utils import make_dir
from datetime import datetime

def get_matrix_similarity(tweet, data):
	'''
	in:
	  tweet:
		list of lemmatized strings from tweet body. Output of preprocessing
	  data:
	    Dict containing filenames of assoc. files
	    format:
	      dataset:
		    filename of dataset csv file
		  dict:
		  	filename of dictionary file
		  model:
		    filename of lsa model
		  output_name:
		    name to be used for all output files generated
		  directory:
		  	directory name where outputs will be saved. If null, output_name is used
	'''

	start = datetime.now()
	df = pd.DataFrame.from_csv('./%s' % data['dataset'])
	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','').replace(']','').replace(',','').replace('\'','')
		lemmas_list.append(lemmas.split())


	isList = isinstance(tweet,list) and not isinstance(tweet,str) and not isinstance(tweet[0],str)

	dictionary = corpora.Dictionary.load('./dicts/%s' % data['dict'])
	clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

	lsi = LsiModel.load('./models/%s' % data['model'])

	index = similarities.MatrixSimilarity(lsi[clean_doc])
	# print(index)
	make_dir('./similarities/')
	directory = ''
	if(data['directory']):
		make_dir('./similarities/%s' % data['directory'])
		directory = data['directory']
	else:
		make_dir('./similarities/%s' % data['output_name'])
		directory = data['output_name']

	data['directory'] = directory

	init_time = (datetime.now()-start)
	print("matrix_similarity_init: %s" % (datetime.now()-start))

	if isList:
		data['filename'] = []
		data['times'] = []
		counter = 0
		for tw in tweet:
			start = datetime.now()
			corpus = lsi[dictionary.doc2bow(tw)]

			with open('./similarities/%s/similarities_%i.txt' % (directory,counter), 'w+') as file:
				for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
					file.write(str(doc) + '\n')

			data['filename'].append('similarities_%i.txt' % counter)
			data['times'].append(datetime.now()-start + init_time)
			
			counter += 1
	else:
		corpus = lsi[dictionary.doc2bow(tweet)]
		print(tweet)
		print(dictionary.doc2bow(tweet))
		with open('./similarities/%s/similarities_%s.txt' % (directory,data['output_name']), 'w+') as file:
			for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
				file.write(str(doc) + '\n')
		print('matrix_similarity_1: %s \n' % (datetime.now()-start + init_time))
		data['filename'] = 'similarities_%s.txt' % data['output_name']

	return data

def get_matrix_similarity_raw(tweet, data):
	'''
	in:
	  tweet:
		list of lemmatized strings from tweet body. Output of preprocessing
	  data:
	    Dict containing filenames of assoc. files
	    format:
	      dataset:
		    filename of dataset csv file
		  dict:
		  	filename of dictionary file
		  model:
		    filename of lsa model
		  output_name:
		    name to be used for all output files generated
		  directory:
		  	directory name where outputs will be saved. If null, output_name is used
	'''

	start = datetime.now()
	df = pd.DataFrame.from_csv('./%s' % data['dataset'])
	lemmas_list = [x.split(' ') for x in df['text'].tolist()]


	isList = isinstance(tweet,list) and not isinstance(tweet,str) and not isinstance(tweet[0],str)

	dictionary = corpora.Dictionary.load('./dicts/%s' % data['dict'])
	clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

	lsi = LsiModel.load('./models/%s' % data['model'])

	index = similarities.MatrixSimilarity(lsi[clean_doc])
	# print(index)
	make_dir('./similarities/')
	directory = ''
	if(data['directory']):
		make_dir('./similarities/%s' % data['directory'])
		directory = data['directory']
	else:
		make_dir('./similarities/%s' % data['output_name'])
		directory = data['output_name']

	data['directory'] = directory

	init_time = (datetime.now()-start)
	# print("matrix_similarity_init: %s" % (datetime.now()-start))

	if isList:
		data['filename'] = []
		data['times'] = []
		counter = 0
		for tw in tweet:
			start = datetime.now()
			corpus = lsi[dictionary.doc2bow(tw)]

			with open('./similarities/%s/similarities_%i.txt' % (directory,counter), 'w+') as file:
				for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
					file.write(str(doc) + '\n')

			data['filename'].append('similarities_%i.txt' % counter)
			data['times'].append(datetime.now()-start + init_time)
			# print('matrix_similarity_%i: %s \n for %s' % (counter,datetime.now()-start + init_time,tw))
			counter += 1
	else:
		corpus = lsi[dictionary.doc2bow(tweet)]
		print(tweet)
		print(dictionary.doc2bow(tweet))
		with open('./similarities/%s/similarities_%s.txt' % (directory,data['output_name']), 'w+') as file:
			for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
				file.write(str(doc) + '\n')

		data['filename'] = 'similarities_%s.txt' % data['output_name']

	return data
