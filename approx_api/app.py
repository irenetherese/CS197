from flask import Flask, jsonify, request
from werkzeug.routing import FloatConverter as BaseFloatConverter
import os
import handler
import sys
import optparse
import sys
import time
import approx_api
import requests
from datetime import datetime
import location_approx.batch_manager as batch_manager
import location_approx.process_manager as process_manager

app = Flask(__name__)
start = int(round(time.time()))

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

app.url_map.converters['float'] = FloatConverter
a = approx_api.ApproximationAPI("127.0.0.1", "ebayanihan_production",  "devuser0", "devuser0",  "5432")
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

@app.route("/get_geo_tweets/ph/<int:collection_id>")
def get_geo_tweets_ph(collection_id):
    return jsonify(a.get_geo_tweets_ph(collection_id))

@app.route("/get_non_geo_tweets/<int:collection_id>")
def get_non_geo_tweets(collection_id):
    return jsonify(a.get_non_geo_tweets(collection_id))

@app.route("/get_geo_tweets")
def get_all_geo_tweets():
    return jsonify(a.get_all_geo_tweets())

@app.route("/get_geo_tweets/ph")
def get_all_geo_tweets_ph():
    return jsonify(a.get_all_geo_tweets_ph())

@app.route("/get_non_geo_tweets")
def get_all_non_geo_tweets():
    return jsonify(a.get_all_non_geo_tweets())

@app.route("/get_tweet_vis_data/<int:collection_id>")
def get_tweet_vis_data(collection_id):
    return jsonify(a.get_tweet_vis_data(collection_id))

@app.route("/get_city")
def get_place(lat, lon):
    input_fields = get_all_request_values(['lat', 'lon'])
    return jsonify(a.get_location_name(input_fields['lat'], input_fields['lon']))

@app.route("/get_tweet_vis_data/ph/<int:collection_id>")
def get_tweet_vis_data_ph(collection_id):
    return jsonify(a.get_tweet_vis_data_ph(collection_id))

@app.route("/get_city/<float:lat>/<float:lon>")
def get_place(lat, lon):
    #input_fields = get_all_request_values(['lat','lon'])
    #return jsonify(a.get_location_name(input_fields['lat'], input_fields['lon']))
    return jsonify(a.get_location_name(lat,lon))

@app.route("/update/<float:tweet_id>/<float:lat>/<float:lon>/<int:radius>")
def update_location(tweet_id, lat, lng, radius):
    return a.update_location(tweet_id, lat, lng, radius)

#@app.route('/start_thread', methods=['GET'])


@app.route("/get_collections")
def get_collections():
    return jsonify(a.get_collections())

@app.route("/get_geo_tweets/<int:collection_id>/<int:year>/<int:month>/<int:day>/<int:hour>")
def get_geo_tweets_hour(collection_id, year, month, day, hour):
  try:
    date_start = datetime(year, month, day, hour, 0) 
    date_end = datetime(year, month, day, hour + 1, 0)
  except:
    return "Error: Cannot calculate date"
  
  return jsonify(a.get_geo_tweets_hour(collection_id, date_start, date_end))

@app.route("/get_geo_tweets/ph/<int:collection_id>/<int:year>/<int:month>/<int:day>/<int:hour>")
def get_geo_tweets_hour_ph(collection_id, year, month, day, hour):
  try:
    date_start = datetime(year, month, day, hour, 0) 
    date_end = datetime(year, month, day, hour + 1, 0)
  except:
    return "Error: Cannot calculate date"
  
  return jsonify(a.get_geo_tweets_hour_ph(collection_id, date_start, date_end))

@app.route("/get_non_geo_tweets/<int:collection_id>/<int:year>/<int:month>/<int:day>/<int:hour>")
def get_non_geo_tweets_hour(collection_id, year, month, day, hour):
  try:
    date_start = datetime(year, month, day, hour, 0) 
    date_end = datetime(year, month, day, hour + 1, 0)
  except:
    return "Error: Cannot calculate date"

  return jsonify(a.get_non_geo_tweets_hour(collection_id, date_start, date_end))

@app.route("/get_tweet_vis_data/<int:collection_id>/<int:start_row>")
def get_tweet_vis_data_limit(collection_id, start_row):
    return jsonify(a.get_tweet_vis_data_limit(collection_id, start_row))

@app.route("/get_tweet_vis_data/ph/<int:collection_id>/<int:start_row>")
def get_tweet_vis_data_limit_ph(collection_id, start_row):
    return jsonify(a.get_tweet_vis_data_limit_ph(collection_id, start_row))

@app.route("/create_handler/<int:thread_id>")
def create_handler(thread_id):
    return handler.create_handler(thread_id)

@app.route('/get_location',methods=['GET'])
def approx_location():
    name = request.values.get('batch_name', 'default')
    date = request.values.get('date', None)

    data = batch_manager.start_batch(name, date)

    result = {}
    result['code'] = 200
    result['message'] = 'Batch created'
    result['data'] = data
    return jsonify(result)


@app.route("/get_model_tweets/<int:model_id>")
def get_model_tweets(model_id):
    return jsonify(a.get_model_tweets(model_id))

@app.route("/get_model_tweets/ph/<int:model_id>")
def get_model_tweets_ph(model_id):
    return jsonify(a.get_model_tweets_ph(model_id))

if __name__ == '__main__':
    process_manager.begin()
   # parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
   # (args, _) = parser.parse_args()
   # if args.port == None:
   #     print("Missing required argument: -p/--port")
   #     sys.exit(1)
   app.run(host='0.0.0.0', port=3000, debug=False)
   # app.run(debug=True)
