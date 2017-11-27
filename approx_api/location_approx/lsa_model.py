from gensim.models.lsimodel import LsiModel
from gensim import corpora, similarities
import gensim.models as models
import pandas as pd
import _thread
import time
from datetime import datetime
from location_approx.utils import make_dir


def train_model(filename, output_name):
	output = {}

	start = datetime.now()
	output['dataset'] = filename
	output['output_name'] = output_name

	df = pd.DataFrame.from_csv(filename)
	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','')
		lemmas = lemmas.replace(']','')
		lemmas = lemmas.replace(',','')
		lemmas_list.append(lemmas.split())

	#print(lemmas_list)
	dictionary = corpora.Dictionary(lemmas_list)
	make_dir('./dicts/')
	dictionary.save('./dicts/%s_corpus.dict' % output_name)

	output['dict'] = '%s_corpus.dict' % output_name

	clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

	tfidf = models.TfidfModel(clean_doc, normalize=True)

	lsi = LsiModel(corpus=tfidf[clean_doc], id2word=dictionary,num_topics=200)
	make_dir('./models')
	lsi.save('./models/%s_model.txt' % output_name)
	output['model'] = '%s_model.txt'%output_name

	print('lsa_model: %s' % (datetime.now()-start))
	return output
