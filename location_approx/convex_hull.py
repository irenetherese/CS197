import numpy as np
import pandas as pd
import math
from scipy.spatial import ConvexHull,Delaunay
from haversine import haversine
import os

df = pd.DataFrame.from_csv('[pp_FULL] SalomePH-geo.csv')
lat_list = [] 
coords = []
main_index = 0

for lat in df['lat']:
	lat_list.append(lat)

counter = 0
for lng in df['lng']:
	temp = []
	temp.append(float(lat_list[counter]))
	temp.append(float(lng))
	coords.append(temp)
	counter += 1


with open('output_salome.txt','w+') as file:

	for filename in os.listdir('similarities/salome'):
		print(filename)
		similarities = open('similarities/salome/%s' %filename,'r')

		points = []

		isFirst = True
		counter = 10
		for line in similarities:
			if isFirst:
				isFirst = not isFirst 
				main_index = int(line.replace('(','').replace(')','').split(',')[0])
				continue
			if counter > 0:
				index = int(line.replace('(','').replace(')','').split(',')[0])
				points.append(coords[index])
				counter -= 1
			else:
				break


		points = np.array(points)

		hull = ConvexHull(points)
		de = Delaunay(points)

		import matplotlib.pyplot as plt

		plt.plot(points[:,0], points[:,1], 'o')

		cx = np.mean(hull.points[hull.vertices,0])
		cy = np.mean(hull.points[hull.vertices,1])

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

		def get_distance(id, point):
			return [id, math.sqrt(math.pow((cx-point[0]),2) + math.pow(cy-point[1], 2))]

		def in_hull(p, hull):
			from scipy.spatial import Delaunay
			if not isinstance(hull,Delaunay):
			    hull = Delaunay(hull)

			return hull.find_simplex(p)>=0

		distances = []
		for index in range(len(midpoints)):
			distances.append(get_distance(index, midpoints[index]))

		distances.sort(key=lambda x: x[1])

		index = distances[0][1]

		file.write('Case %s\n' % filename)
		file.write('\tPoint: %f,%f\n' % (cx,cy))
		file.write('\tRadius: %f' % index)
		file.write('\tinHull:' + str(in_hull(p=np.array([coords[main_index][0],coords[main_index][1]]),hull=de)) + '\n')
		file.write('\n')
