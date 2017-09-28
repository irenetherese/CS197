import psycopg2
import sys
import csv
import json


class ApproximationAPI:

    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.con = None

    def connect(self):
        self.con = psycopg2.connect("host='" + self.host + "' dbname='" + self.dbname + "' user='" + self.user + "' password='" + self.password + "'")   
        return self.con

    def close_connect(self):
        self.con.close()
        self.con = None

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

    #def update_db(self, filename):
        #self.connect();
        #cur = self.con.cursor
        #cur.copy_from(fi[plename, temp_unicommerce_status, sep=',')


    def setup(self):
        if self.con:
            cur = self.con.cursor()
            cur.execute(open("tables.sql","r").read())
            print("Created tables.")
            cur.execute(open("phl_adm0s.sql","r").read())
            print("Imported gis data to countries table")
            cur.execute(open("phl_adm1s.sql","r").read())
            print("Imported gis data to provinces table")
            cur.execute(open("phl_adm2s.sql","r").read())
            print("Imported gis data to city_municipalities table")
            cur.execute(open("phl_adm3s.sql","r").read())
            print("Imported gis data to barangays table")
            self.con.commit()
            cur.close()
        else:
            self.connect()
            self.setup()

    def test(self):
        print("Testing connection to database: " + self.dbname)
        print("Host: " + self.host)
        print("User: " + self.user)
       
        self.con = self.connect()
        print("Successfully connected to database")

        if self.con:
            self.close_connect()
            print("Successfully closed connection from database")


