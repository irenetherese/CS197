from lsa_model import train_model
from matrix_similarity import get_matrix_similarity
from convex_hull import get_convex_hull
from random import *
import pandas as pd

df = pd.DataFrame.from_csv('dataset_yolanda.csv')
tweet = []

lemmas_list = [] 
indices = [320,3025,3320,1438,3160,4812,2990,2673,348,1171]

for lemmas in df['lemmas']:
	lemmas = str(lemmas)
	lemmas = lemmas.replace('[','')
	lemmas = lemmas.replace(']','')
	lemmas = lemmas.replace(',','')
	lemmas_list.append(lemmas.split())

for x in indices:
	print('%s : %s' % (x,lemmas_list[x]))
	tweet.append(lemmas_list[x])

data = {}

data = train_model('dataset_yolanda.csv','2')
#data = {'filename': ['similarities_0.txt', 'similarities_1.txt', 'similarities_2.txt', 'similarities_3.txt', 'similarities_4.txt', 'similarities_5.txt', 'similarities_6.txt', 'similarities_7.txt', 'similarities_8.txt', 'similarities_9.txt'], 'output_name': '1', 'directory': 'yolanda', 'model': '1_model.txt', 'dataset': 'dataset_yolanda.csv', 'dict': '1_corpus.dict'}

data['directory'] = 'yolanda'


data = get_matrix_similarity(tweet,data)
#print(data)
output = get_convex_hull(10,data)

for item in output:
	print(item)

