import time
import csv
import pandas as pd
import spacy


df = pd.read_csv('yolanda nov 7.csv', delimiter=',')
nlp = spacy.load('en')

new_words = ["don't", "dont"]

for word in new_words:
	lexeme = nlp.vocab[word]
	lexeme.is_stop = True

start = time.time()
df['Parsed'] = df['text'].apply(nlp)

lemmas = []

for doc in df['Parsed']:
	temp = []
	for w in doc:
		if not w.is_stop and not w.is_punct and not w.like_num:
			temp.append(w)
	lemmas.append(temp)
df['lemmas'] = lemmas

print (time.time() - start)

df.to_csv('./[pp_FULL] yolanda nov 7.csv')