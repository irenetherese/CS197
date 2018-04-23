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
    '''
    Creates a file containing all the related info for a batch.
    '''
    make_dir('data/batch_data/')
    with open('./data/batch_data/batch_%s' % name, 'w+') as file:
        data = {}
        data['name'] = name
        data['collection_id'] = json.loads(requests.get('localhost:443/get_collection_id?batch_name=%s' % name).text)[
            'id']
        data['filename'] = str(uuid.uuid4())
        if date:
            data['date'] = str(date)
        else:
            data['date'] = str(datetime.datetime.now())
        data['last_tweet_id'] = ''
        data['model'] = ''
        data['model_count'] = 1
        file.write(json.dumps(data))
        print('Batch created')
        print(data)
    return data


def stop(name):
    '''
    Removes the corresponding batch file from the batch_data directory.
    This indicates that the batch is no longer being actively managed
    '''
    filename = 'batch_%s' % name
    if filename in listdir('./data/batch_data'):
        remove('./data/batch_data/batch_%s' % name)


def manage(name, isFirst=False):
    '''
    Checks current status of the batch, if the model needs updating or if there are new tweets to be located.
    '''
    try:
        # Load batch data
        batch_data = open('./data/batch_data/batch_%s' % name, 'r+')
        data = json.load(batch_data)

        isFirst = (data['model'] == '')
        try:
            d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.now()
        diff = d - d2

        # If the model is over an hour out of date or has not yet been created, it is updated
        if (((diff.total_seconds() / 60) / 60) >= 1.0 or isFirst):
            data['date'] = str(d2)
            data = update_model(data)

        # Check if there are tweets with no locations
        data = queue_tweets(data)

        batch_data.seek(0)
        batch_data.truncate()
        batch_data.write(json.dumps(data))
        batch_data.close()
    except:
        # Since it's possible a batch file could be removed while manage() is being called,
        # this except clause catches for that situation and removes the batch file.
        batch_data.close()
        stop(data['name'])
        return
    return


def update_model(data):
    '''
        Retrieves tweets to be used in as the training set and retrains the model on that
    '''
    print('Updating model for batch %s' % data['name'])
    make_dir('./data/dataset/')
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

    print('Sending request: http://localhost:443/get_geo_tweets/ph/%s/%i/%i/%i/%i' % (
        data['collection_id'], d.year, d.month, d.day, d.hour))
    # Load tweets to be used as the dataset
    tweets = json.loads(requests.get('http://localhost/get_geo_tweets/ph/%s/%i/%i/%i/%i' % (
        data['collection_id'], d.year, d.month, d.day, d.hour)).text)

    # Note: 50 is an arbitrary amount. Can be increased or decreased if needed.
    if len(tweets) > 50:
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
        # Preprocess tweets by lemmatization
        process_tweets('./data/dataset/dataset_%s.csv' % data['filename'])
        print('Tweets lemmatized')

        print('Training model')
        data = train_model(output_name=data['filename'] + ' -count' + str(data['model_count']),
                           filename='dataset_%s.csv' % data['filename'], data=data)
        data['model_count'] = int(data['model_count']) + 1
        print('Model created at %s' % data['model'])
    else:
        print('Not enough tweets for model creation')
    return data


def queue_tweets(data):
    try:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        d = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')

    # Queries for tweets after the last tweet processed
    if data['last_tweet_id'] != '':
        tweets = json.loads(requests.get(
            'http://localhost:443/get_non_geo_tweets/%s/%i/%i/%i/%i?tweet_id=%s' % (
                data['collection_id'], d.year, d.month, d.day, d.hour, data['last_tweet_id'])).text)
    else:
        tweets = json.loads(requests.get(
            'http://localhost:443/get_non_geo_tweets/%s/%i/%i/%i/%i' % (
                data['collection_id'], d.year, d.month, d.day, d.hour)).text)
    # If a non-zero amount of tweets are retrieved
    if len(tweets) >= 1:
        file = open('./data/queue/%s %i.csv' % (data['name'], data['model_count']), 'w+')
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

        # Preprocessing by lemmatization
        process_tweets('./data/queue/%s %i.csv' % (data['name'], data['model_count']))
    else:
        print('No tweets found for batch %s' % data['name'])

    return data
