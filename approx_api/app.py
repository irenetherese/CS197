from flask import Flask
import sys
import optparse
import time
import approx_api

app = Flask(__name__)
start = int(round(time.time()))

a = approx_api.ApproximationAPI("localhost", "ebayanihan",  "it",  "5432")
a.test()

@app.route("/")
def hello_world():
    return "Hello World Flask Test!"


@app.route("/get_tweets")
def get_tweets():
	a.connect()
	return a.get_tweet_data(10)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python3 app.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)
