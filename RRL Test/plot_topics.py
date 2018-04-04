from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import csv
 
# map.drawcoastlines()
# map.drawcountries()
# map.shadedrelief();
# map.bluemarble()

# lon = -135.3318
# lat = 57.0799
# x,y = map(lon, lat)
# map.plot(x, y, 'bo', markersize=24)

colors = ['bo', 'go', 'ro', 'co', 'mo']

for i in range(0, 24):
	#hour = 'main'
	map = Basemap(projection='lcc', width=1200000,height=1800000, lat_0 = 13, lon_0 = 122, resolution = 'f')
	map.fillcontinents(color = 'tab:olive')
	map.drawmapboundary()

	try:
		with open('./lda/dataset_yolanda nov 8_%s_topics.csv' %i,'r') as csvinput:
			reader = csv.reader(csvinput)
			row = next(reader)

			for row in reader:
				lat = row[5] 
				lon = row[6]
				x,y = map(lon, lat)
				map.plot(x, y, colors[int(row[10])], markersize=1)

		figprops = dict(figsize=(5,4), dpi=100, facecolor='white')
		# generate the first figure.
		fig1 = plt.figure(1,**figprops)
		ax1 = fig1.add_subplot(111)

		fig1.canvas.draw()
		fig1.savefig("./lda/figs/dataset_yolanda nov 8_%s.png" %i, dpi=1000)
		fig1.clf()
		# plt.show()
	except:
		print("Error occured")