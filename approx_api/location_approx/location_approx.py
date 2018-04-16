from lsa_model import train_model,train_model_tfidf,train_model_tfidf_raw,train_model_raw
from matrix_similarity import get_matrix_similarity,get_matrix_similarity_raw
from convex_hull import get_convex_hull
from convex_hull_unweighted import get_convex_hull as get_ch
from random import *
import location_approx.utils 
import pandas as pd

for i in range(0,10):
	filename = 'tfidf-weighted_%i' % i
	print(filename)
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)

	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','').replace(']','').replace(',','').replace('\'','')
		lemmas_list.append(lemmas.split())

	data = {}

	data = train_model_tfidf('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation_tfidf-weighted'

	data = get_matrix_similarity(lemmas_list,data)
	print(data)
	output = get_convex_hull(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'notfidf-weighted_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','').replace(']','').replace(',','').replace('\'','')
		lemmas_list.append(lemmas.split())

	data = {}

	data = train_model('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-notfidf-weighted'

	data = get_matrix_similarity(lemmas_list,data)
	print(data)
	output = get_convex_hull(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'tfidf-unweighted_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','').replace(']','').replace(',','').replace('\'','')
		lemmas_list.append(lemmas.split())

	data = {}

	data = train_model_tfidf('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-tfidf-unweighted'

	data = get_matrix_similarity(lemmas_list,data)
	print(data)
	output = get_ch(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'notfidf-unweighted_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [] 

	for lemmas in df['lemmas']:
		lemmas = str(lemmas)
		lemmas = lemmas.replace('[','').replace(']','').replace(',','').replace('\'','')
		lemmas_list.append(lemmas.split())

	data = {}

	data = train_model('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-notfidf-unweighted'

	data = get_matrix_similarity(lemmas_list,data)
	print(data)
	output = get_ch(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))

			count+=1

for i in range(0,10):
	filename = 'tfidf-weighted_raw_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)

	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [x.split(' ') for x in df['text'].tolist()]

	data = {}

	data = train_model_tfidf_raw('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation_tfidf-weighted_raw'

	data = get_matrix_similarity_raw(lemmas_list,data)
	print(data)
	output = get_convex_hull(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'notfidf-weighted_raw_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [x.split(' ') for x in df['text'].tolist()]

	data = {}

	data = train_model_raw('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-notfidf-weighted_raw'

	data = get_matrix_similarity_raw(lemmas_list,data)
	print(data)
	output = get_convex_hull(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'tfidf-unweighted_raw_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [x.split(' ') for x in df['text'].tolist()]

	data = {}

	data = train_model_tfidf_raw('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-tfidf-unweighted_raw'

	data = get_matrix_similarity_raw(lemmas_list,data)
	print(data)
	output = get_ch(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))
			count+=1

for i in range(0,10):
	filename = 'notfidf-unweighted_raw_%i' % i
	df = pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i)
	print(filename)
	print('------------------------%i-------------------------------------------------------' % i)

	lemmas_list = [x.split(' ') for x in df['text'].tolist()]

	data = {}

	data = train_model_raw('./folds/case_%i/training.csv' % i,'case_%i' % i)

	data['directory'] = 'validation-notfidf-unweighted_raw'

	data = get_matrix_similarity_raw(lemmas_list,data)
	print(data)
	output = get_ch(10,data)

	utils.make_dir('./logs')
	with open('./logs/%s.txt' % filename, 'w+') as file:
		count = 1
		for item in output:
			print (item)
			file.write('%i & (%.4f,%.4f) & %.4f & %s & %s\n' % (count,item['coords'][0],item['coords'][1],item['radius'],item['inHull'],item['time']))

			count+=1
