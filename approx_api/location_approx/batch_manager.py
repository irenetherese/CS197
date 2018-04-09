from utils import make_dir
import json
import uuid
import datetime

def start_batch(name, date=None):
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
        file.write(json.dumps(data))


start_batch('test')


