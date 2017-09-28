import approx_api
a = approx_api.ApproximationAPI("localhost", "ebayanihan",  "ebayanihan",  "ebayanihan")
a.test()
#a.setup()
a.connect()
a.import_tweets("data.csv")
