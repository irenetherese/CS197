from gensim.models.lsimodel import LsiModel
from gensim import corpora, similarities
import gensim.models as models
import pandas as pd
import _thread
import time
import datetime

def time_counter(start_time,isRunning):
	while(isRunning):
		print("%s elapsed" % (str(datetime.timedelta(seconds=time.time() - start_time))),end='\r')


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

clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

tfidf = models.TfidfModel(clean_doc, normalize=True)

isRunning = True

start_time = time.time()

_thread.start_new_thread(time_counter,(start_time,isRunning))

# lsi = LsiModel(corpus=tfidf[clean_doc], id2word=dictionary,num_topics=200)
# lsi.save('model.txt')

lsi = LsiModel.load('model.txt')


index = similarities.MatrixSimilarity(lsi[clean_doc])

corpus = lsi[dictionary.doc2bow(lemmas_list[0])]
# print(time.time()-start_time)
with open('./outputs_clean.txt', 'w+') as file:
	for doc in sorted(enumerate(index[corpuscd ]), key=lambda item: -item[1]):
		file.write(str(doc) + '\n')

isRunning = False
time.sleep(1)

print(str(datetime.timedelta(seconds=time.time() - start_time)))