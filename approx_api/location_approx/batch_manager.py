import csv
import datetime
import json
import uuid
from os import remove, listdir

import requests
from location_approx.lsa_model import train_model
from location_approx.preprocess import process_tweets
from location_approx.utils import make_dir


def start(name, date=None):
    make_dir('data/batch_data/')
    with open('./data/batch_data/batch_%s' % name, 'w+') as file:
        data = {}
        data['name'] = name
        # data['collection_id'] = json.loads(requests.get('localhost:443/get_collection_id?batch_name=%s' % name).text)[
        #     'id']
        data['collection_id'] = 1
        data['filename'] = str(uuid.uuid4())
        if date:
            data['date'] = str(date)
        else:
            data['date'] = str(datetime.datetime.now())
        data['last_tweet_id'] = ''
        data['model'] = ''
        file.write(json.dumps(data))
    manage(name, True)
    return data


def stop(name):
    if name in listdir('./data/batch_data'):
        remove('./data/batch_data/batch_%s' % name)


def manage(name, isFirst=False):
    batch_data = open('./data/batch_data/batch_%s' % name, 'r+')
    data = json.load(batch_data)
    try:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.now()
    diff = d - d2

    if (((diff.total_seconds() / 60) / 60) >= 1.0 or isFirst):
        data = update_model(data)

    data = queue_tweets(data)

    batch_data.seek(0)
    batch_data.truncate()
    batch_data.write(json.dumps(data))
    batch_data.close()

    return


def update_model(data):
    print('Updating model for batch %s' % data['name'])
    file = open('./data/dataset/dataset_%s.csv' % data['filename'], 'w+')
    try:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    writer = csv.DictWriter(file, fieldnames={
        'id': 'id',
        'lat': 'lat',
        'lng': 'lng',
        'text': 'text'
    })

    print('Sending request: http://35.202.52.52:443/get_geo_tweets/ph/%s/%i/%i/%i/%i' % (
        data['collection_id'], d.year, d.month, d.day, d.hour))
    tweets = json.loads(requests.get('http://35.202.52.52:443/get_geo_tweets/ph/%s/%i/%i/%i/%i' % (
        data['collection_id'], d.year, d.month, d.day, d.hour)).text)

    writer.writerow({
        'id': 'id',
        'lat': 'lat',
        'lng': 'lng',
        'text': 'text'
    })

    last_tweet = ''
    for item in tweets:
        last_tweet = item
        writer.writerow({
            'id': item,
            'lat': tweets[item]['lat'],
            'lng': tweets[item]['lon'],
            'text': tweets[item]['text']
        })
    data['last_tweet_id'] = last_tweet
    print('.csv file created')
    file.close()

    print('Lemmatizing tweets')
    process_tweets('./data/dataset/dataset_%s.csv' % data['filename'])
    print('Tweets lemmatized')

    print('Training model')
    data = train_model(output_name=data['filename'], filename='dataset_%s.csv' % data['filename'], data=data)
    print('Model created at %s' % data['model'])
    return data


def queue_tweets(data):
    if data['last_tweet_id'] != '':
        tweets = json.loads(requests.get(
            'http://35.202.52.52:443/get_non_geo_tweets/%s?tweet_id=%s' % (
                data['collection_id'], data['last_tweet_id'])).text)
    else:
        tweets = json.loads(requests.get(
            'http://35.202.52.52:443/get_non_geo_tweets/%s' % (data['collection_id'])).text)
    if len(tweets) > 1:
        file = open('./data/queue/%s.csv' % data['name'], 'w+')
        writer = csv.DictWriter(file, fieldnames={
            'id': 'id',
            'text': 'text'
        })

        writer.writerow({
            'id': 'id',
            'text': 'text'
        })

        for item in tweets:
            writer.writerow({
                'id': item,
                'text': tweets[item]['text']
            })
    else:
        print('No tweets found for batch %s' % data['name'])
    return data
