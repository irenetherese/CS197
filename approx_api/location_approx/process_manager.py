import _thread as thread
import json
import time
from os import listdir, remove

import location_approx.batch_manager as batch_manager
import pandas as pd
import requests
from location_approx.convex_hull import get_convex_hull
from location_approx.matrix_similarity import get_matrix_similarity
from location_approx.utils import make_dir

NUMBER_OF_DIMENSIONS = 10


def start():
    make_dir('./data/queue/')
    thread.start_new_thread(start_thread, ())


def start_thread():
    while True:
        files = listdir('./data/queue')
        # If no tweets are queued
        if len(files) == 0:
            files = listdir('./data/batch_data')
            if len(files) != 0:
                for file in files:
                    # Update individual batches (Check for unlocated tweets or model updates)
                    batch_manager.manage(file.replace('batch_', ''))
            else:
                # Do nothing if no batches are active
                time.sleep(5)
        # else, process queued tweets
        else:
            process(files[0])


def process(file):
    filename = file.replace('.csv', '').split(' ')[0]

    print('Found file: %s.csv' % filename)
    name = 'batch_%s' % filename

    # If tweets remain queued for a batch that has ended, the tweets are discarded
    if (name not in listdir('./data/batch_data')):
        remove('./data/queue/%s' % file)
        print('Batch %s no longer exists' % filename)
        return

    # Load batch information
    batch_data = open('./data/batch_data/batch_%s' % filename, 'r+')
    data = json.load(batch_data)

    # Load tweets and associated model
    df = pd.read_csv('./data/queue/%s' % file)
    data['model'] = data['model'].replace('-count%s' % data['model_count'], file.replace('.csv', '').split(' ')[1])

    # Retrieve preprocessed tweet bodies from the csv
    lemmas_list = []
    count = 0
    for lemmas in df['lemmas']:
        if count == 30:
            break
        lemmas = str(lemmas)
        lemmas = lemmas.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        lemmas_list.append(lemmas.split())
        count += 1

    # Perform matrix similarity and convex hull generation
    data = get_matrix_similarity(lemmas_list, data)
    data = get_convex_hull(NUMBER_OF_DIMENSIONS, data)

    # Save tweet locations to the database
    for item in data:
        index = int(item['filename'].replace('similarities_', '').replace('.txt', ''))

        print('Saving to tweet id %s: %s' % (df['id'][index], item['coords']))

        coords = str(item['coords']).replace('(', '').replace(')', '').replace(' ', '').split(',')
        print(
            requests.get('http://localhost:443/update/%s/%s/%s/0' % (
                df['id'][index].replace('\'', ''), coords[0], coords[1])).text)

    batch_data.close()
    remove('./data/queue/%s' % file)
    return
