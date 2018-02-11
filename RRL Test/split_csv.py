import csv
import time

#SPLITS CSV DATA INTO HOURS

def split_csv(file_obj, filename):

	mapper = [[] for i in range(0,24)] #FOR EACH HOUR OF THE DAY
	reader = csv.DictReader(file_obj, delimiter=',')
	line2 = reader.fieldnames

	for line in reader:
		#print(line)
		#print(line['created_at'])
		ttime = time.gmtime(float(line['created_at'])) # READS EPOCH TIME AND CONVERTS IT TO time_struct from time library

		if(ttime.tm_mday == 6): # THIS IS HARD CODED FOR YOLANDA NOV 6 EXAMPLE (JUST MAKING SURE IT'S THE SAME DATE)
			mapper[ttime.tm_hour].append(line) #MAPS TO LIST DEPENDING ON THE HOUR

	for i in range(0,24): #GET FROM THE MAPPER AND WRITE IT INTO NEW CSV FILES
		file = open('dataset_%s_%s.csv' % (filename, i), 'wt')
		writer = csv.DictWriter(file,delimiter=',',lineterminator='\n', fieldnames=line2)
		writer.writerow({
			'user': 'user',
			'language': 'language',
			'user location': 'user location',
			'lat': 'lat',
			'lng': 'lng',
			'user utc offset':'user utc offset',
			'text':'text',
			'user time zone': 'user time zone',
			'id': 'id',
			'created_at': 'created_at',
			})
		for line3 in mapper[i]:
			print(line3)
			writer.writerow({
				'user': line3['user'],
				'language': line3['language'],
				'user location': line3['user location'],
				'lat': line3['lat'],
				'lng': line3['lng'],
				'user utc offset': line3['user utc offset'],
				'text': line3['text'].replace(';', ''),
				'user time zone': line3['user time zone'],
				'id': line3['id'],
				'created_at': line3['created_at'],
				})

with open("yolanda nov 6.csv", "rt") as f_obj:
	split_csv(f_obj, "yolanda nov 6")
