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
            print(files)
            if len(files) != 0:
                for file in files:
                    batch_manager.manage(file.replace('batch_', ''))
            else:
                time.sleep(5)
        else:
            process(files[0])


def process(file):
    filename = file.replace('.csv', '').split(' ')[0]

    print('Found file: %s.csv' % filename)
    batch_data = open('./data/batch_data/batch_%s' % filename, 'r+')
    data = json.load(batch_data)
    df = pd.read_csv('./data/queue/%s' % file)
    print(data['model'])
    data['model'] = data['model'].replace('-count%s' % data['model_count'], file.replace('.csv', '').split(' ')[1])
    print(data['model'])
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

        coords = str(item['coords']).replace('(', '').replace(')', '').replace(' ', '').split(',')
        print(
            requests.get('http://35.202.52.52:443/update/%s/%s/%s/0' % (
            df['id'][index].replace('\'', ''), coords[0], coords[1])).text)

    batch_data.close()
    remove('./data/queue/%s' % file)
    return
