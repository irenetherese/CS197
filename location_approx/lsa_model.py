from gensim.models.lsimodel import LsiModel
from gensim import corpora, similarities
import gensim.models as models
import pandas as pd
import _thread
import time
import datetime

df = pd.DataFrame.from_csv('[pp_FULL] SalomePH-geo.csv')
lemmas_list = [] 

for lemmas in df['lemmas']:
	lemmas = str(lemmas)
	lemmas = lemmas.replace('[','')
	lemmas = lemmas.replace(']','')
	lemmas = lemmas.replace(',','')
	lemmas_list.append(lemmas.split())

#print(lemmas_list)

dictionary = corpora.Dictionary(lemmas_list)
dictionary.save('./salome_corpus.dict')

clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

tfidf = models.TfidfModel(clean_doc, normalize=True)

lsi = LsiModel(corpus=tfidf[clean_doc], id2word=dictionary,num_topics=200)
lsi.save('salome_model.txt')
