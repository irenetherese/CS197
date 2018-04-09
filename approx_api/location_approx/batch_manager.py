import datetime
import json
import uuid
from os import remove, listdir

from utils import make_dir


def start(name, date=None):
    make_dir('data/batch_data/')
    with open('./data/batch_data/batch_%s' % name, 'w+') as file:
        data = {}
        data['name'] = name
        data['filename'] = str(uuid.uuid4())
        data['model']
        if date:
            data['date'] = date
        else:
            data['date'] = str(datetime.datetime.now())
        data['last_tweet_id'] = ''
        file.write(json.dumps(data))
    manage(name)
    return data


def stop(name):
    if name in listdir('./data/batch_data'):
        remove('./data/batch_data/batch_%s' % name)


def manage(name):
    # TODO: retrieve new tweets from db and update model dataset

    return
