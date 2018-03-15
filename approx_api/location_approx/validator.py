import pandas as pd
import json
import requests
from utils import make_dir
from haversine import haversine



def measure_accuracy(cou2n2t, point1, point2):
	print(cou2n2t)
	print(json.loads(requests.get('http://35.193.17.215:443/get_city/%s/%s' % (point1[0],point1[1])).text)['name'])
	print(json.loads(requests.get('http://35.193.17.215:443/get_city/%s/%s' % (point2[0],point2[1])).text)['name'])
	print()
	if json.loads(requests.get('http://35.193.17.215:443/get_city/%s/%s' % (point1[0],point1[1])).text)['name'] != json.loads(requests.get('http://35.193.17.215:443/get_city/%s/%s' % (point2[0],point2[1])).text)['name']:
		return 0
	else:
		return 1


files = []
for i in range(0,10):
	files.append(pd.DataFrame.from_csv('./folds/case_%i/testing.csv' % i))

def validate(batch,value):
	sum3 = 0
	sum4 = 0
	for i in range(0,10):	
		with open('./logs/%s_%i.txt' % (batch,i), 'rt') as rd:
			make_dir('./validation')
			cou2n2t = 1
			sum1 = 0;
			sum2 = 0;
			count1 = 0;
			count2 = 0;
			for l in rd:
				line = l.split(' & ')
				line[1] = line[1].replace('(','').replace(')','')
				temp = line[1].split(',')
				pt = (float(files[i]['lat'][int(line[0])-1]),float(files[i]['lng'][int(line[0])-1]))
				cpt =(float(temp[0]),float(temp[1]))
				if(line[3] == 'True'):
					sum1 += measure_accuracy(cou2n2t,pt,cpt)
					count1 += 1
				sum2 += measure_accuracy(cou2n2t,pt,cpt)
				count2 += 1
				cou2n2t += 1
			sum3 += sum1/count1
			sum4 += sum2/count2	
			print('-----%s | %f-----' % (batch,value))
			print(sum3)
			print(sum4)
			print('\n')
	print('-----%s | %f-----' % (batch,value))
	print(sum3/10)
	print(sum4/10)
	print('\n')

batches = ['tfidf-weighted']

for batch in batches:
	validate(batch,10.0)


def validate_hull(batch):
	sum3 = 0
	sum4 = 0
	for i in range(0,10):	
		with open('./logs/%s_%i.txt' % (batch,i), 'rt') as rd:
			make_dir('./validation')
			sum1 = 0;
			sum2 = 0;
			count1 = 0;
			count2 = 0;
			for l in rd:
				line = l.split(' & ')
				line[1] = line[1].replace('(','').replace(')','')
				temp = line[1].split(',')
				pt = (float(files[i]['lat'][int(line[0])-1]),float(files[i]['lng'][int(line[0])-1]))
				cpt =(float(temp[0]),float(temp[1]))
				if(line[3] == 'True'):
					sum1 += 1
				count1 += 1
			sum3 += sum1/count1	
	print('-----%s-----' % (batch))
	print((sum3/10.0)*100)
	print('\n')

print('\n')
print('\n')
print('\n')
print('\n')

batches = ['tfidf-weighted']

for batch in batches:
	validate_hull(batch)

