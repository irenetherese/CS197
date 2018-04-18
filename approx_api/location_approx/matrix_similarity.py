import pandas as pd
from gensim import corpora, similarities
from gensim.models.lsimodel import LsiModel
from location_approx.utils import make_dir


def get_matrix_similarity(tweet, data):
    '''
    in:
      tweet:
        list of lemmatized strings from tweet body. Output of preprocessing
      data:
        Dict containing filenames of assoc. files
        format:
          dataset:
            filename of dataset csv file
          dict:
            filename of dictionary file
          model:
            filename of lsa model
          output_name:
            name to be used for all output files generated
          directory:
              directory name where outputs will be saved. If null, output_name is used
    '''

    df = pd.read_csv('./data/dataset/%s' % data['dataset'])
    lemmas_list = []

    for lemmas in df['lemmas']:
        lemmas = str(lemmas)
        lemmas = lemmas.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        lemmas_list.append(lemmas.split())

    dictionary = corpora.Dictionary.load('./data/dicts/%s' % data['dict'])
    clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

    lsi = LsiModel.load('./data/models/%s' % data['model'])

    index = similarities.MatrixSimilarity(lsi[clean_doc])

    make_dir('./data/similarities/')
    directory = ''
    if ('directory' in data.keys()):
        make_dir('./data/similarities/%s' % data['directory'])
        directory = data['directory']
    else:
        make_dir('./data/similarities/%s' % data['output_name'])
        directory = data['output_name']

    data['directory'] = directory

    data['filename'] = []
    counter = 0
    for tw in tweet:
        corpus = lsi[dictionary.doc2bow(tw)]

        with open('./data/similarities/%s/similarities_%i.txt' % (directory, counter), 'w+') as file:
            for doc in sorted(enumerate(index[corpus]), key=lambda item: -item[1]):
                file.write(str(doc) + '\n')

        data['filename'].append('similarities_%i.txt' % counter)

        counter += 1

    return data
