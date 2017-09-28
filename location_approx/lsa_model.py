from gensim.models.lsimodel import LsiModel
from gensim import corpora
import gensim.models as models
import pandas as pd

df = pd.DataFrame.from_csv('[pp_FULL] yolanda nov 7.csv')
lemmas_list = [] 

for lemmas in df['lemmas']:
	lemmas = str(lemmas)
	lemmas = lemmas.replace('[','')
	lemmas = lemmas.replace(']','')
	lemmas = lemmas.replace(',','')
	lemmas_list.append(lemmas.split())

#print(lemmas_list)

dictionary = corpora.Dictionary(lemmas_list)
dictionary.save('./nov7_corpus.dict')

clean_doc = dictionary.doc2bow(lemmas_list)
tfidf = models.TfidfModel(lemmas_list)

lsi = LsiModel(corpus=tfidf,num_topics=200)

#print(lsi[corpus[text]])