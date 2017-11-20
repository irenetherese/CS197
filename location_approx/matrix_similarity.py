from gensim import corpora, similarities
from gensim.models.lsimodel import LsiModel
import pandas as pd
import random
from utils import make_dir

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

	df = pd.DataFrame.from_csv(data['dataset'])
	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','')
		lemmas = lemmas.replace(']','')
		lemmas = lemmas.replace(',','')
		lemmas_list.append(lemmas.split())


	dictionary = corpora.Dictionary.load('./dicts/%s' % data['dict'])

	clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

	lsi = LsiModel.load('./models/%s' % data['model'])

	index = similarities.MatrixSimilarity(lsi[clean_doc])

	corpus = lsi[dictionary.doc2bow(tweet)]

	make_dir('./similarities/')
	directory = ''
	if(data['directory']):
		make_dir('./similarities/%s' % data['directory'])
		directory = data['directory']
	else:
		make_dir('./similarities/%s' % data['output_name'])
		directory = data['output_name']

	data['directory'] = directory

	with open('./similarities/%s/similarities_%s.txt' % (directory,data['output_name']), 'w+') as file:
		for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
			file.write(str(doc) + '\n')

	data['filename'] = 'similarities_%s.txt' % data['output_name']

	return data
