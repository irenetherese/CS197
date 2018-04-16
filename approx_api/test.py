import approx_api
import simplejson as json

a = approx_api.ApproximationAPI("0.0.0.0", "ebayanihan_development",  "postgres",  "8080")
#a.test()
#a.setup()
a.connect()
#a.import_tweets("data/yolanda nov 7.csv")
#print(a.get_location_name(11.580717100000001, 122.75519059999999))
#a.update_location( 398297782605197313,11.580717100000001, 122.75519059999999, 3)
data = a.get_tweet_json(2)
with open('sample_tweet.json', 'w') as outfile:
    json.loads(data, outfile)

#data = a.get_geo_tweets(2)
#with open('SalomePH-geo.json', 'w') as outfile:
#    json.dump(data, outfile, sort_keys=True, indent=4)

#data = a.get_non_geo_tweets(2)
#with open('SalomePH-non-geo.json', 'w') as outfile:
#    json.dump(data, outfile, sort_keys=True, indent=4)


a.close_connect()
#"location": self.get_location_name(arr[i][4], arr[i][5])