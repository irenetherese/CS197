import approx_api
a = approx_api.ApproximationAPI("0.0.0.0", "ebayanihan_development",  "postgres",  "8080")
#a.test()
#a.setup()
a.connect()
#a.import_tweets("data/yolanda nov 7.csv")
#print(a.get_location_name(11.580717100000001, 122.75519059999999))
#a.update_location( 398297782605197313,11.580717100000001, 122.75519059999999, 3)
print(a.get_tweet_data(10))
a.close_connect()
#"location": self.get_location_name(arr[i][4], arr[i][5])