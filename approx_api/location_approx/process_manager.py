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
        if len(files) == 0:
            files = listdir('./data/batch_data')
            if len(files) != 0:
                for file in files:
                    batch_manager.manage(file.replace('batch_', ''))
            else:
                time.sleep(5)
        else:
            process(files[0])


def process(file):
    filename = file.replace('.csv', '')

    batch_data = open('./data/batch_data/batch_%s' % filename, 'r+')
    data = json.load(batch_data)
    df = pd.read_csv('./data/queue/%s' % file)

    lemmas_list = []

    count = 0
    for lemmas in df['lemmas']:
        if count == 30:
            break
        lemmas = str(lemmas)
        lemmas = lemmas.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        lemmas_list.append(lemmas.split())
        count += 1

    data = get_matrix_similarity(lemmas_list, data)
    data = get_convex_hull(NUMBER_OF_DIMENSIONS, data)

    for item in data:
        index = int(item['filename'].replace('similarities_', '').replace('.txt', ''))

        print('Saving to tweet id %s: %s' % (df['id'][index], item['coords']))

        coords = str(item['coords']).replace('(', '').replace(')', '').split(',')
        requests.get('localhost:443/update/%s/%s/%s/0' % (df['id'][index], coords[0], [coords[1]]))

    batch_data.close()
    remove('./data/queue/%s' % file)
    return

