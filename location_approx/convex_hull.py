import numpy as np
import pandas as pd
import math
from scipy.spatial import ConvexHull
from haversine import haversine

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
counter = 10
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

print(points)
print(points[0][0])

hull = ConvexHull(points)

import matplotlib.pyplot as plt

plt.plot(points[:,0], points[:,1], 'o')

cx = np.mean(hull.points[hull.vertices,0])
cy = np.mean(hull.points[hull.vertices,1])

print(hull.points[hull.vertices])

plt.plot(cx, cy, 'o')

for simplex in hull.simplices:
	plt.plot(points[simplex, 0], points[simplex, 1], 'k-')



counter = 1
midpoints = []
for point in hull.points[hull.vertices]:

	if counter == len(points):
		counter = 0
	px = (point[0] + points[counter][0])/2
	py = (point[1] + points[counter][1])/2
	midpoints.append([px,py])
	counter += 1

print(len(midpoints))

def get_distance(id, point):
	return [id, math.sqrt(math.pow((cx-point[0]),2) + math.pow(cy-point[1], 2))]

distances = []
for index in range(len(midpoints)):
	distances.append(get_distance(index, midpoints[index]))

distances.sort(key=lambda x: x[1])

index = distances[0][0]
print(haversine((cx,cy),(midpoints[index][0],midpoints[index][1])))

plt.show()