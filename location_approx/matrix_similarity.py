from gensim import corpora, similarities
from gensim.models.lsimodel import LsiModel
import pandas as pd
import random

counter = 0


df = pd.DataFrame.from_csv('dataset_yolanda.csv')
lemmas_list = [] 

for lemmas in df['lemmas']:
	lemmas = str(lemmas)
	lemmas = lemmas.replace('[','')
	lemmas = lemmas.replace(']','')
	lemmas = lemmas.replace(',','')
	lemmas_list.append(lemmas.split())


dictionary = corpora.Dictionary.load('yolanda_corpus.dict')

clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

lsi = LsiModel.load('yolanda_model.txt')

while counter < 10:

	index = similarities.MatrixSimilarity(lsi[clean_doc])


	corpus = lsi[dictionary.doc2bow(lemmas_list[random.randint(0,len(lemmas_list)-1)])]
	# print(time.time()-start_time)
	with open('./similarities/similarities_yolanda_%s.txt' % counter, 'w+') as file:
		for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
			file.write(str(doc) + '\n')
	counter += 1