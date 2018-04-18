import datetime
import json
import uuid
from os import remove, listdir

from location_approx.lsa_model import train_model
from location_approx.utils import make_dir


def start(name, date=None):
    make_dir('data/batch_data/')
    with open('./data/batch_data/batch_%s' % name, 'w+') as file:
        data = {}
        data['name'] = name
        data['filename'] = str(uuid.uuid4())
        if date:
            data['date'] = date
        else:
            data['date'] = str(datetime.datetime.now())
        data['last_tweet_id'] = ''
        data['model'] = ''
        file.write(json.dumps(data))
    manage(name)
    return data


def stop(name):
    if name in listdir('./data/batch_data'):
        remove('./data/batch_data/batch_%s' % name)


def manage(name):
    # TODO: retrieve new tweets from db and update model dataset

    batch_data = open('./data/batch_data/batch_%s' % name, 'r+')
    data = json.load(batch_data)
    print(data)
    data = train_model(output_name=data['filename'], filename='dataset_yolanda.csv')

    d = datetime.datetime.strftime(data['date'], '%Y-%m-%d %H:%M:%S.%f')
    d2 = datetime.datetime.now()
    diff = d - d2
    if (((diff.total_seconds() / 60) / 60) >= 1.0):
        update_model(data)

    queue_tweets(data)

    batch_data.seek(0)
    batch_data.truncate()
    batch_data.write(json.dumps(data))
    batch_data.close()

    return


def update_model(data):
    # TODO: update model

    return


def queue_tweets(data):
    #
    # TODO: query non_geo_tweets then save to .csv

    return
