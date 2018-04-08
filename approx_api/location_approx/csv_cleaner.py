import csv
import pandas as pd
import requests
import json
from location_approx.utils import make_dir

def csv_reader(file_obj,filename):
	reader = csv.DictReader(file_obj, delimiter=',')
	print(reader.fieldnames)

	file = open('dataset_%s' % filename, 'wt')
	writer = csv.DictWriter(file,delimiter=',',lineterminator='\n', fieldnames=reader.fieldnames)

	line2 = reader.fieldnames

	writer.writerow({
					'user': line2[3],
					'language': line2[5],
					'user location': line2[8],
					'lat': line2[6],
					'lng': line2[7],
					'user utc offset': line2[9],
					'text': line2[4],
					'user time zone': line2[10],
					'id': line2[1],
					'created_at': line2[2],
					'lemmas': line2[12]
					})

	for line in reader:
		if line['lat'] and line['lng'] and len(line['language']) == 2:
				writer.writerow({
					'user': line['user'],
					'language': line['language'],
					'user location': line['user location'],
					'lat': line['lat'],
					'lng': line['lng'],
					'user utc offset': line['user utc offset'],
					'text': line['text'].replace(';', ''),
					'user time zone': line['user time zone'],
					'id': line['id'],
					'created_at': line['created_at'],
					'lemmas': line['lemmas']
					})

# files = ["[pp_FULL] yolanda nov 9.csv","[pp_FULL] yolanda nov 6.csv","[pp_FULL] yolanda nov 7.csv"]


def merge_files(files):
	file = open('dataset_stress.csv', 'wt')
	

	isFirst = True

	for filename in files:
		reader = csv.DictReader(open(filename,"rt"), delimiter=',')
		print(reader.fieldnames)
		writer = csv.DictWriter(file,delimiter=',',lineterminator='\n',fieldnames=reader.fieldnames)

		if isFirst:
			line2 = reader.fieldnames
			writer.writerow({
					'user': line2[3],
					'language': line2[5],
					'user location': line2[8],
					'lat': line2[6],
					'lng': line2[7],
					'user utc offset': line2[9],
					'text': line2[4],
					'user time zone': line2[10],
					'id': line2[1],
					'created_at': line2[2],
					'lemmas': line2[12]
					})
			isFirst = not isFirst
		count = 1
		for line in reader:
			try:
				# print('line %i' % count )
				# print(requests.get('http://35.226.51.248:443/get_city/%s/%s' % (line['lat'],line['lng'])))
				# if json.loads(requests.get('http://35.226.51.248:443/get_city/%s/%s' % (line['lat'],line['lng'])).text)['name'] != 'N/A':
				writer.writerow({
				'user': line['user'],
				'language': line['language'],
				'user location': line['user location'],
				'lat': line['lat'],
				'lng': line['lng'],
				'user utc offset': line['user utc offset'],
				'text': line['text'],
				'user time zone': line['user time zone'],
				'id': line['id'],
				'created_at': line['created_at'],
				'lemmas': line['lemmas']
				})
				count += 1
			except Exception:
				print(line['lat'] + " " + line['lng'])

# for filename in files:
# 	with open(filename, "rt") as f_obj:
# 		csv_reader(f_obj,filename)

def split_into_folds(num_of_folds, filename):
	file = open(filename, 'rt')

	count = 0
	reader = csv.DictReader(file, delimiter=',')
	writers = []
	for i in range(0, num_of_folds):
		writers.append(csv.DictWriter(open("./folds/fold-%i.csv" % i, 'wt'),delimiter=',',lineterminator='\n',fieldnames=reader.fieldnames))

	isFirst = [True,True,True,True,True,True,True,True,True,True]
	for line in reader:
		if (isFirst[count]):
			line2 = reader.fieldnames
			writers[count].writerow({
					'user': line2[3],
					'language': line2[5],
					'user location': line2[8],
					'lat': line2[6],
					'lng': line2[7],
					'user utc offset': line2[9],
					'text': line2[4],
					'user time zone': line2[10],
					'id': line2[1],
					'created_at': line2[2],
					'lemmas': line2[12]
					})
			isFirst[count] = not isFirst[count]
		
		writers[count].writerow({
			'user': line['user'],
			'language': line['language'],
			'user location': line['user location'],
			'lat': line['lat'],
			'lng': line['lng'],
			'user utc offset': line['user utc offset'],
			'text': line['text'],
			'user time zone': line['user time zone'],
			'id': line['id'],
			'created_at': line['created_at'],
			'lemmas': line['lemmas']
			})
		if count == 9:
			count = 0
		else:
			count += 1
	for i in range(0,10):
		files = []
		isTheFirst = True
		for t in range(0,10):
			make_dir("./folds/case_%i" % t)
			files.append(csv.DictReader(open('./folds/fold-%i.csv' %t,"rt"), delimiter=','))
		wr = csv.DictWriter(open("./folds/case_%i/training.csv" % i, 'wt'),delimiter=',',lineterminator='\n',fieldnames=reader.fieldnames)
		for count in range(0,10):
			if(count != i):
				for line in files[count]:
					if isTheFirst:
						line2 = reader.fieldnames
						wr.writerow({
								'user': line2[3],
								'language': line2[5],
								'user location': line2[8],
								'lat': line2[6],
								'lng': line2[7],
								'user utc offset': line2[9],
								'text': line2[4],
								'user time zone': line2[10],
								'id': line2[1],
								'created_at': line2[2],
								'lemmas': line2[12]
								})
						isTheFirst = not isTheFirst
					else:
						wr.writerow({
						'user': line['user'],
						'language': line['language'],
						'user location': line['user location'],
						'lat': line['lat'],
						'lng': line['lng'],
						'user utc offset': line['user utc offset'],
						'text': line['text'],
						'user time zone': line['user time zone'],
						'id': line['id'],
						'created_at': line['created_at'],
						'lemmas': line['lemmas']
						})
			if count == i:
				isReallyTheFirst = True
				wt = csv.DictWriter(open('./folds/case_%i/testing.csv' % i,'wt'),delimiter=',',lineterminator='\n',fieldnames=reader.fieldnames)
				for line in files[count]:
					print(line)
					print('----------%i---------------------' % i)
					if isReallyTheFirst:
						line2 = reader.fieldnames
						wt.writerow({
								'user': line2[3],
								'language': line2[5],
								'user location': line2[8],
								'lat': line2[6],
								'lng': line2[7],
								'user utc offset': line2[9],
								'text': line2[4],
								'user time zone': line2[10],
								'id': line2[1],
								'created_at': line2[2],
								'lemmas': line2[12]
								})
						isReallyTheFirst = not isReallyTheFirst
					else:
						wt.writerow({
						'user': line['user'],
						'language': line['language'],
						'user location': line['user location'],
						'lat': line['lat'],
						'lng': line['lng'],
						'user utc offset': line['user utc offset'],
						'text': line['text'],
						'user time zone': line['user time zone'],
						'id': line['id'],
						'created_at': line['created_at'],
						'lemmas': line['lemmas']
						})



merge_files(['batch1.csv','batch2.csv','batch3.csv','batch4.csv'])
# split_into_folds(10,'dataset_yolanda.csv')
