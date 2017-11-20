import numpy as np
import pandas as pd
import math
from scipy.spatial import ConvexHull,Delaunay
from haversine import haversine
import os


def get_distance(id, point, cx, cy):
	return [id, math.sqrt(math.pow((cx-point[0]),2) + math.pow(cy-point[1], 2))]

def in_hull(p, hull):
	from scipy.spatial import Delaunay
	if not isinstance(hull,Delaunay):
	    hull = Delaunay(hull)

	return hull.find_simplex(p)>=0

def get_convex_hull(n,data):
	df = pd.DataFrame.from_csv(data['dataset'])
	lat_list = [] 
	coords = []
	main_index = 0
	directory = ''
	if (data['directory']):
		directory = data['directory']
	else:
		directory = data['output_name']

	for lat in df['lat']:
		lat_list.append(lat)

	output = {}
	counter = 0
	for lng in df['lng']:
		temp = []
		temp.append(float(lat_list[counter]))
		temp.append(float(lng))
		coords.append(temp)
		counter += 1

	isList = isinstance(data['filename'],list) and not isinstance(data['filename'],str)

	if isList:
		output_list = []
		for filename in os.listdir('similarities/%s' % directory):
			if filename in data['filename']:
				similarities = open('similarities/%s/%s' %(directory,filename),'r')

				points = []

				isFirst = True
				counter = n
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

				distances = []
				for index in range(len(midpoints)):
					distances.append(get_distance(index, midpoints[index],cx,cy))

				distances.sort(key=lambda x: x[1])

				index = distances[0][1]

				sample_dict = {}

				sample_dict['coords'] =	(cx,cy)
				sample_dict['radius'] = index
				sample_dict['filename'] = filename	

				output_list.append(sample_dict)
		return output_list
	else:
		similarities = open('similarities/%s/%s' %(directory,data['filename']),'r')

		points = []

		isFirst = True
		counter = n
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

		distances = []
		for index in range(len(midpoints)):
			distances.append(get_distance(index, midpoints[index],cx,cy))

		distances.sort(key=lambda x: x[1])

		index = distances[0][1]

		output['coords'] = (cx,cy)
		output['radius'] = index

		return output	
