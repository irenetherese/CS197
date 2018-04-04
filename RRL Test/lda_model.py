from gensim.models.ldamodel import LdaModel
from gensim import corpora, similarities
import gensim
import gensim.models as models
import pandas as pd
import _thread
import time
import datetime
from utils import make_dir
from operator import itemgetter
import csv


def lda_train_model(filename, output_name):
	output = {}
	output['dataset'] = filename
	output['output_name'] = output_name

	#LEMMATIZATION
	df = pd.DataFrame.from_csv(filename)
	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','')
		lemmas = lemmas.replace(']','')
		lemmas = lemmas.replace(',','')
		lemmas_list.append(lemmas.split())

	#print(lemmas_list)

	#CLEAN DOCUMENT
	dictionary = corpora.Dictionary(lemmas_list)
	make_dir('./lda/dicts/')
	dictionary.save('./lda/dicts/%s_corpus.dict' % output_name)
	output['dict'] = '%s_corpus.dict' % output_name
	clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]
	tfidf = models.TfidfModel(clean_doc, normalize=True)


	try:
	#CREATE MODEL
		lda = LdaModel(corpus=tfidf[clean_doc], id2word=dictionary, num_topics = 5)
	except ValueError:
		print("Error: Cannot compute LDA over an empty collection (no terms)")
		return output

	make_dir('./lda/models')
	lda.save('./lda/models/yolanda nov 8_%s_model.txt' % output_name)
	output['model'] = '%s_model.txt'%output_name


	#GET TOPICS AND TOPIC DISTRIBUTION TO BE SAVED TO FILE
	topics = lda.show_topics()
	topic_dist = lda[clean_doc]
	make_dir('./lda/topics')
	text_file = open("./lda/topics/yolanda nov 8_%s_topics.txt" %output_name, "w")

	iterr = 0
	text_file.write("TOPICS: \n ----- \n \n")
	for topic in topics:
		text_file.write("TOPIC " + str(iterr)+": "+ str(topic) + "\n")
		iterr += 1

	final_topics = []
	iterr = 0
	text_file.write("-----\n \nTOPIC DISTRIBUTION: \n-----\n \n")
	for topic_dis in topic_dist:
		text_file.write(str(iterr) + ": " + str(topic_dis) + "\n" + "--- " + str(max(topic_dis,key=itemgetter(1))[0]) + "\n")
		iterr += 1
		final_topics.append(max(topic_dis,key=itemgetter(1))[0])
	text_file.close()


	#CREATE DATASET WITH CORRESPONDING TOPIC NUMBER TO BE PLOTTED
	with open('./lda/dataset_yolanda nov 8_%s.csv' %output_name,'r') as csvinput:
	#with open('yolanda nov 8.csv','r') as csvinput:
		with open('./lda/dataset_yolanda nov 8_%s_topics.csv' %output_name, 'w') as csvoutput:
			writer = csv.writer(csvoutput, lineterminator='\n')
			reader = csv.reader(csvinput)

			al = []
			row = next(reader)
			row.append('TOPIC')
			al.append(row)

			i = 0
			for row in reader:
				if row[5] != '':
					row.append(final_topics[i])
					al.append(row)
				i += 1

			writer.writerows(al)

	print(output)
	return output
