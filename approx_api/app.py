from flask import Flask,jsonify,request

import sys
import optparse
import time
import approx_api
import requests

from location_approx.lsa_model import train_model
from location_approx.matrix_similarity import get_matrix_similarity
from location_approx.convex_hull import get_convex_hull

app = Flask(__name__)
start = int(round(time.time()))

a = approx_api.ApproximationAPI("192.168.1.120", "ebayanihan_development",  "postgres",  "8080")
a.test()
a.connect()

def get_all_request_values(request_field_list):
    """Appends requested value to input_fields if value is not None"""
    input_fields = {}
    for field in request_field_list:
        input_fields[field] = request.values.get(field, None)
        if input_fields[field] is not None:
            if input_fields[field] == "":
                input_fields[field] = None
            else:
                input_fields[field] = input_fields[field].strip()
    return input_fields


@app.route("/")
def hello_world():
    return "Hello World Flask Test!"

@app.route("/get_geo_tweets/<int:collection_id>")
def get_geo_tweets(collection_id):
    return jsonify(a.get_geo_tweets(collection_id))

@app.route("/get_non_geo_tweets/<int:collection_id>")
def get_non_geo_tweets(collection_id):
    return jsonify(a.get_non_geo_tweets(collection_id))

@app.route("/get_tweet_vis_data/<int:collection_id>")
def get_tweet_vis_data(collection_id):
    return jsonify(a.get_tweet_vis_data(collection_id))

@app.route("/get_city")
def get_place(lat, lon):
    input_fields = get_all_request_values(['lat','lon'])
    return jsonify(a.get_location_name(input_fields['lat'], input_fields['lon']))

@app.route("/update/<float:tweet_id>/<float:lat>/<float:lon>/<int:radius>")
def update_location(tweet_id, lat, lng, radius):
    return a.update_location(tweet_id, lat, lng, radius)

@app.route('/get_location',methods=['GET'])
def approx_location():
	tweet = request.values.get('tweet',None).replace('\'','').replace(' ','').split(',')
	print(type(tweet[0]))

	data = {'output_name': '1', 
			'directory': 'yolanda', 
			'model': '1_model.txt', 
			'dataset': 'dataset_yolanda.csv', 
			'dict': '1_corpus.dict'}
	data = get_matrix_similarity(tweet,data)
	print(data['filename'])
	return jsonify(get_convex_hull(10,data))


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python3 app.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='127.0.0.1', port=int(args.port), debug=False)
