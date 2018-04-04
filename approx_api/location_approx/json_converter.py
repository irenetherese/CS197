import csv
import json

js = json.load(open('SalomePH-geo.json'))

f = csv.writer(open('SalomePH-geo.csv','w+'))

f.writerow(["id","lat","lng","text"])


for line in js:
	f.writerow([
				line,
				js[line]['lat'],
				js[line]['lon'],
				js[line]['text']
				])