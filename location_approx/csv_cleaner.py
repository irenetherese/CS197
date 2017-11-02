import csv

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

files = ["[pp_FULL] yolanda nov 9.csv","[pp_FULL] yolanda nov 6.csv","[pp_FULL] yolanda nov 7.csv"]

def merge_files(files):
	file = open('dataset_yolanda.csv', 'wt')
	

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

		for line in reader:
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

for filename in files:
	with open(filename, "rt") as f_obj:
		csv_reader(f_obj,filename)

merge_files(["dataset_[pp_FULL] yolanda nov 9.csv","dataset_[pp_FULL] yolanda nov 6.csv","dataset_[pp_FULL] yolanda nov 7.csv"])