import numpy as np
import pandas as pd
import math
from scipy.spatial import ConvexHull,Delaunay
from haversine import haversine
import os
from datetime import datetime

def get_distance(id, point, cx, cy):
	return [id, math.sqrt(math.pow((cx-point[0]),2) + math.pow(cy-point[1], 2))]

def in_hull(p, hull):
	# if not isinstance(hull,Delaunay):
	#     hull = Delaunay(hull)

	return hull.find_simplex(p)>=0

def get_convex_hull(n,data):
	start = datetime.now()
	df = pd.DataFrame.from_csv('./%s' % data['dataset'])
	lat_list = [] 
	coords = []
	main_index = 0
	directory = ''
	if (data['directory']):
		directory = data['directory']
	else:
		directory = data['output_name']

	output = {}
	isList = isinstance(data['filename'],list) and not isinstance(data['filename'],str)

	init_time = (datetime.now()-start)
	# print("convex_hull_init: %s" % (datetime.now()-start))
	if isList:
		output_list = []
		out_counter = 0
		for filename in os.listdir('./similarities/%s' % directory):
			start = datetime.now()
			if filename in data['filename']:
				similarities = open('./similarities/%s/%s' %(directory,filename),'r')

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
						points.append([df['lat'][index],df['lng'][index]])
						counter -= 1
					else:
						break
				points = np.array(points)

				hull = ConvexHull(points)
				de = Delaunay(points)

				cx = np.mean(hull.points[hull.vertices,0])
				cy = np.mean(hull.points[hull.vertices,1])

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

				index = haversine((cx,cy),(midpoints[distances[0][0]][0],midpoints[distances[0][0]][1]))


				sample_dict = {}

				sample_dict['coords'] =	(cx,cy)
				sample_dict['radius'] = index
				sample_dict['filename'] = filename
				sample_dict['inHull'] = in_hull(p=np.array([df['lat'][main_index],df['lng'][main_index]]),hull=de)	
				sample_dict['time'] = str(datetime.now()-start+init_time+data['times'][out_counter])
				output_list.append(sample_dict)

				# print("convex_hull_init_%i: %s" % (main_index, datetime.now()-start+init_time))
				
				out_counter += 1
		return output_list
	else:
		start = datetime.now()
		similarities = open('./location_approx/similarities/%s/%s' %(directory,data['filename']),'r')

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
				points.append([df['lat'][index],df['lng'][index]])
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

		print("convex_hull_init_1: %s" % (datetime.now()-start+init_time))
		return output	
