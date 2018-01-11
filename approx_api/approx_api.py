import psycopg2
import sys
import csv
import simplejson as json
import decimal

class ApproximationAPI:
    def __init__(self, host, dbname, user, pw, port):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.port = port
        self.pw = pw
        self.con = None

###############
# CONNECTIONS #
###############
    def connect(self):
        self.con = psycopg2.connect("host='" + self.host + "' dbname='" + self.dbname + "' user='" + self.user + "' password='" + self.pw + "' port='" + self.port + "'")   
        return self.con

    def close_connect(self):
        self.con.close()
        self.con = None

    #test connection
    def test(self):
        print("Testing connection to database: " + self.dbname)
        print("Host: " + self.host)
        print("User: " + self.user)
       
        self.con = self.connect()
        print("Successfully connected to database")

        if self.con:
            self.close_connect()
            print("Successfully closed connection from database")


#################
# FUNCTIONALITY #
#################
    def get_location_name(self, lat, lon):
        statement = ''' 
            SELECT tweet_collector_barangays.name_3, city_municipalities.name_2, provinces.name_1
            FROM city_municipalities 
            INNER JOIN tweet_collector_barangays ON city_municipalities.id_2 = tweet_collector_barangays.id_2
            INNER JOIN provinces ON provinces.id_1 = city_municipalities.id_1
            WHERE ST_INTERSECTS(ST_PointFromText('POINT( ''' + str(lon) + " " + str(lat) + ''')', 4326), tweet_collector_barangays.geom);
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        fetch = cur.fetchone()
        cur.close()
        if(fetch != None):
            out = {"name": {"barangay":fetch[0], "city": fetch[1], "province": fetch[2]}, "geo": {"lat": str(lat), "lon": str(lon)}}
        else:
            out = {"name": "N/A", "geo": {"lat": lat, "lon": lon}}
        return out

    #all tweets
    def get_tweets(self, collection_id):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json
            FROM tweet_collector_tweets
            WHERE collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": arr[i][2], "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": {"lat": str(arr[i][4]), "lon": str(arr[i][5])}, "radius": arr[i][7]}
        cur.close()
        return dic

    #for model training
    def get_geo_tweets(self, collection_id):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]),"lon": str(arr[i][3])}
        cur.close()
        return dic

    #for tweets to be geolocated using model
    def get_non_geo_tweets(self, collection_id):
        statement = ''' 
            SELECT tweet_id, tweet_text
            FROM tweet_collector_tweets
            WHERE tweet_lat ISNULL AND tweet_lon ISNULL AND collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1])}
        cur.close()
        return dic

    #for visualization of tweets
    def get_tweet_vis_data(self, collection_id):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            location = self.get_location_name(arr[i][4], arr[i][5])
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": json.loads(arr[i][8])['user']['name'],  "username": arr[i][2], "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": location, "radius": arr[i][7]}
        cur.close()
        return dic

    def update_location(self, tweet_id, lat, lon, radius):
        statement = ''' 
            UPDATE tweet_collector_tweets
            SET tweet_lat = ''' + str(lat) + ''', tweet_lon = ''' + str(lon) + ''', radius = ''' + str(radius) + '''
            WHERE tweet_id =''' + str(tweet_id) + ''';
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        self.con.commit()
        cur.close()
        return "Success!"

    def get_tweet_json(self, collection_id):
        statement = ''' 
            SELECT tweet_json
            FROM tweet_collector_tweets
            WHERE collection_id = ''' + str(collection_id) + '''
            LIMIT 1
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        return cur.fetchone()
        

###########################
# FOR LOCAL DATABASE TEST #
###########################
    def setup(self):
        if self.con:
            cur = self.con.cursor()
            cur.execute(open("migrations/tables.sql","r").read())
            print("Created tables.")
            cur.execute(open("migrations/phl_adm0s.sql","r").read())
            print("Imported gis data to countries table")
            cur.execute(open("migrations/phl_adm1s.sql","r").read())
            print("Imported gis data to provinces table")
            cur.execute(open("migrations/phl_adm2s.sql","r").read())
            print("Imported gis data to city_municipalities table")
            cur.execute(open("migrations/phl_adm3s.sql","r").read())
            print("Imported gis data to tweet_collector_barangays table")
            self.con.commit()
            cur.close()
        else:
            self.connect()
            self.setup()

    def import_tweets(self, filename):
        statement = ''' 
            COPY %s FROM STDIN WITH 
                CSV 
                HEADER
                DELIMITER AS ',' 
            '''
        my_file = open(filename)
        cur = self.con.cursor()
        cur.copy_expert(sql=statement % 'tweets',file = my_file)
        self.con.commit()
        cur.close()
        print("Successfully imported tweets")
