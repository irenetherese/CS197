import time

import pandas as pd
import spacy


# files = ['yolanda nov 6.csv', 'yolanda nov 7.csv', 'yolanda nov 9.csv']
# files = ["./lda/dataset_yolanda nov 6_6.csv", "./lda/dataset_yolanda nov 6_7.csv", "./lda/dataset_yolanda nov 6_8.csv", "./lda/dataset_yolanda nov 6_9.csv", "./lda/dataset_yolanda nov 6_10.csv", "./lda/dataset_yolanda nov 6_11.csv", "./lda/dataset_yolanda nov 6_12.csv", "./lda/dataset_yolanda nov 6_13.csv", "./lda/dataset_yolanda nov 6_14.csv", "./lda/dataset_yolanda nov 6_15.csv", "./lda/dataset_yolanda nov 6_16.csv", "./lda/dataset_yolanda nov 6_17.csv", "./lda/dataset_yolanda nov 6_18.csv", "./lda/dataset_yolanda nov 6_19.csv",  "./lda/dataset_yolanda nov 6_20.csv"]
# files = ['yolanda nov 6.csv']
# files = ['SalomePH-geo.csv']
def process_tweet(filename):

    df = pd.read_csv(filename, delimiter=',')
    nlp = spacy.load('en')
    new_words = ["don't", "dont"]

    for word in new_words:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True

    start = time.time()
    df['Parsed'] = df['text'].apply(nlp)

    lemmas = []

    for doc in df['Parsed']:
        temp = []
        for w in doc:
            if not w.is_stop and not w.is_punct and not w.like_num and len(
                    w.lemma_) > 2 and '@' not in w.lemma_ and 'http' not in w.lemma_:
                temp.append(str.lower(w.lemma_))
        lemmas.append(temp)
    df['lemmas'] = lemmas

    df.to_csv(filename)
