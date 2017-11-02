import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

df = pd.DataFrame.from_csv('dataset_yolanda.csv')
lat_list = [] 
coords = []


for lat in df['lat']:
	lat_list.append(lat)

counter = 0
for lng in df['lng']:
	temp = []
	temp.append(float(lat_list[counter]))
	temp.append(float(lng))
	coords.append(temp)
	counter += 1


similarities = open('similarities.txt','r')

points = []

isFirst = True
counter = 5
for line in similarities:
	if isFirst:
		isFirst = not isFirst 
		continue
	if counter > 0:
		index = int(line.replace('(','').replace(')','').split(',')[0])
		points.append(coords[index])
		counter -= 1
	else:
		break


points = np.array(points)


hull = ConvexHull(points)

import matplotlib.pyplot as plt

plt.plot(points[:,0], points[:,1], 'o')

for simplex in hull.simplices:
	plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

plt.show()