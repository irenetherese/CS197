from flask import Flask
from flask import jsonify
from werkzeug.routing import FloatConverter as BaseFloatConverter

import sys
import optparse
import time
import approx_api
import requests
from datetime import datetime


class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

app = Flask(__name__)
start = int(round(time.time()))

a = approx_api.ApproximationAPI("127.0.0.1", "ebayanihan_production",  "devuser0", "devuser0",  "5432")
a.test()
a.connect()

app.url_map.converters['float'] = FloatConverter

@app.route("/")
def hello_world():
    return "Hello World Flask Test!"

@app.route("/get_geo_tweets/<int:collection_id>")
def get_geo_tweets(collection_id):
    return jsonify(a.get_geo_tweets(collection_id))

@app.route("/get_non_geo_tweets/<int:collection_id>")
def get_non_geo_tweets(collection_id):
    return jsonify(a.get_non_geo_tweets(collection_id))

@app.route("/get_geo_tweets")
def get_all_geo_tweets():
    return jsonify(a.get_all_geo_tweets())

@app.route("/get_non_geo_tweets")
def get_all_non_geo_tweets():
    return jsonify(a.get_all_non_geo_tweets())

@app.route("/get_tweet_vis_data/<int:collection_id>")
def get_tweet_vis_data(collection_id):
    return jsonify(a.get_tweet_vis_data(collection_id))

@app.route("/get_city/<float:lat>/<float:lon>")
def get_place(lat, lon):
    return jsonify(a.get_location_name(lat, lon))

@app.route("/update/<float:tweet_id>/<float:lat>/<float:lon>/<int:radius>")
def update_location(tweet_id, lat, lng, radius):
    return a.update_location(tweet_id, lat, lng, radius)

@app.route("/get_collections")
def get_collections():
    return jsonify(a.get_collections())

@app.route("/get_geo_tweets/<int:collection_id>/<int:year>/<int:month>/<int:day>/<int:hour>")
def get_geo_tweets(collection_id, year, month, day, hour):
  try:
    date_start = datetime(year, month, day, hour, 0) 
    date_end = datetime(year, month, day, hour + 1, 0)
  except:
    return "Error: Cannot calculate date"
  
    return jsonify(a.get_geo_tweets(collection_id, date_start, date_end))

@app.route("/get_non_geo_tweets/<int:collection_id>")
def get_non_geo_tweets(collection_id, year, month, day, hour):
  try:
    date_start = datetime(year, month, day, hour, 0) 
    date_end = datetime(year, month, day, hour + 1, 0)
  except:
    return "Error: Cannot calculate date"

    return jsonify(a.get_non_geo_tweets(collection_id, date_start, date_end))

@app.route("/get_tweet_vis_data/<int:collection_id>/<int:start_row>/<int:num_rows>")
def get_tweet_vis_data(collection_id, start_row, num_rows):
    return jsonify(a.get_tweet_vis_data(collection_id, start_row, num_rows))

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

if __name__ == '__main__':
   # parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
   # (args, _) = parser.parse_args()
   # if args.port == None:
   #     print("Missing required argument: -p/--port")
   #     sys.exit(1)
     app.run(host='0.0.0.0', port=3000, debug=False)
   # app.run(debug=True)

