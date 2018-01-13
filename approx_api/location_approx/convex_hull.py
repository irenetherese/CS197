import numpy as np
import pandas as pd
import math
from scipy.spatial import ConvexHull,Delaunay
from haversine import haversine
import os
from datetime import datetime
import location_approx.utils as utils

def get_distance(id, point, cx, cy):
	return [id, math.sqrt(math.pow((cx-point[0]),2) + math.pow(cy-point[1], 2))]

def in_hull(p, hull):
	# if not isinstance(hull,Delaunay):
	#     hull = Delaunay(hull)

	return hull.find_simplex(p)>=0

def get_convex_hull(n,data):
	start = datetime.now()
	df = pd.DataFrame.from_csv('./location_approx/%s' % data['dataset'])
	lat_list = [] 
	coords = []
	main_index = 0
	directory = ''
	if (data['directory']):
		directory = data['directory']
	else:
		directory = data['output_name']

	output = {}
	weights = {}
	isList = isinstance(data['filename'],list) and not isinstance(data['filename'],str)

	init_time = (datetime.now()-start)
	print("convex_hull_init: %s" % (datetime.now()-start))
	if isList:
		output_list = []
		out_counter = 0
		for filename in os.listdir('./location_approx/similarities/%s' % directory):
			start = datetime.now()
			if filename in data['filename']:
				similarities = open('./location_approx/similarities/%s/%s' %(directory,filename),'r')

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
						print(df['lat'][index])
						weights[df['lat'][index]] = int(line.replace('(','').replace(')','').split(',')[1])
						counter -= 1
					else:
						break
				points = np.array(points)

				hull = ConvexHull(points)
				de = Delaunay(points)

				import matplotlib.pyplot as plt

				plt.plot(points[:,0], points[:,1], 'o')

				sumx,sumy,sumz = 0,0,0
				for pt in hull.points[hull.vertices]:
					print(pt)
					# p = utils.lon_lat_to_cartesian()
		
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
				sample_dict['inHull'] = in_hull(p=np.array([df['lat'][main_index],df['lng'][main_index]]),hull=de)	

				output_list.append(sample_dict)

				print("convex_hull_init_%i: %s" % (main_index, datetime.now()-start+init_time))
				
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
				weights[df['lat'][index]] = float(line.replace('(','').replace(')','').replace('\n','').split(',')[1])
				counter -= 1
			else:
				break

		points = np.array(points)

		hull = ConvexHull(points)
		de = Delaunay(points)

		sumx,sumy,sumz,sumw = 0,0,0,0
		for pt in hull.points[hull.vertices]: 
			p = utils.lon_lat_to_cartesian(pt[0],pt[1])
			sumx = weights[pt[0]] * p[0].astype(np.int64)
			sumy = weights[pt[0]] * p[1].astype(np.int64)
			sumz = weights[pt[0]] * p[2].astype(np.int64)
			sumw = weights[pt[0]]

		m = utils.cartesian_to_lon_lat((sumx/sumw,sumy/sumw,sumz/sumw))
		cx = m[0]
		cy = m[1]

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
