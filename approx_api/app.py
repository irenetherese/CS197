from flask import Flask
import sys
import optparse
import time
import approx_api

app = Flask(__name__)
start = int(round(time.time()))

a = approx_api.ApproximationAPI("localhost", "ebayanihan_development",  "postgres",  "8080")
a.test()
a.connect()

@app.route("/")
def hello_world():
    return "Hello World Flask Test!"

@app.route("/get_tweets")
def get_tweets():
	return a.get_tweet_data(10)

@app.route("/get_city/<float:lat>/<float:lon>")
def get_place(lat, lon):
    return a.get_location_name(lat, lon)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python3 app.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)
