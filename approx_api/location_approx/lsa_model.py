from gensim.models.lsimodel import LsiModel
from gensim import corpora, similarities
import gensim.models as models
import pandas as pd
from datetime import datetime
from utils import make_dir


def train_model(filename, output_name):
    output = {}

    output['dataset'] = filename
    output['output_name'] = output_name

    df = pd.read_csv('./data/dataset/%s' % filename)
    lemmas_list = []

    for lemmas in df['lemmas']:
        lemmas = str(lemmas)
        lemmas = lemmas.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        lemmas_list.append(lemmas.split())

    dictionary = corpora.Dictionary(lemmas_list)
    make_dir('./data/dicts/')
    dictionary.save('./data/dicts/%s_corpus.dict' % output_name)

    output['dict'] = '%s_corpus.dict' % output_name

    clean_doc = [dictionary.doc2bow(text) for text in lemmas_list]

    tfidf = models.TfidfModel(clean_doc, normalize=True)

    lsi = LsiModel(corpus=tfidf[clean_doc], id2word=dictionary, num_topics=200)
    make_dir('./data/models')
    lsi.save('./data/models/%s_model.txt' % output_name)
    output['model'] = '%s_model.txt' % output_name

    return output
