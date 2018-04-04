import time
import csv
import pandas as pd
import spacy

#files = ["dataset_yolanda nov 6_6.csv", "dataset_yolanda nov 6_7.csv", "dataset_yolanda nov 6_8.csv", "dataset_yolanda nov 6_9.csv", "dataset_yolanda nov 6_10.csv", "dataset_yolanda nov 6_11.csv", "dataset_yolanda nov 6_12.csv", "dataset_yolanda nov 6_13.csv", "dataset_yolanda nov 6_14.csv", "dataset_yolanda nov 6_15.csv", "dataset_yolanda nov 6_16.csv", "dataset_yolanda nov 6_17.csv", "dataset_yolanda nov 6_18.csv", "dataset_yolanda nov 6_19.csv",  "dataset_yolanda nov 6_20.csv"]
files = ["dataset_yolanda nov 7_0.csv", "dataset_yolanda nov 7_1.csv", "dataset_yolanda nov 7_2.csv", "dataset_yolanda nov 7_3.csv", "dataset_yolanda nov 7_4.csv", "dataset_yolanda nov 7_5.csv", "dataset_yolanda nov 7_6.csv", "dataset_yolanda nov 7_7.csv", "dataset_yolanda nov 7_8.csv", "dataset_yolanda nov 7_9.csv", "dataset_yolanda nov 7_10.csv", "dataset_yolanda nov 7_11.csv", "dataset_yolanda nov 7_12.csv", "dataset_yolanda nov 7_13.csv", "dataset_yolanda nov 7_14.csv", "dataset_yolanda nov 7_15.csv", "dataset_yolanda nov 7_16.csv", "dataset_yolanda nov 7_17.csv", "dataset_yolanda nov 7_18.csv", "dataset_yolanda nov 7_19.csv",  "dataset_yolanda nov 7_20.csv", "dataset_yolanda nov 7_21.csv", "dataset_yolanda nov 7_22.csv", "dataset_yolanda nov 7_23.csv", "dataset_yolanda nov 8_0.csv", "dataset_yolanda nov 8_1.csv", "dataset_yolanda nov 8_2.csv", "dataset_yolanda nov 8_3.csv", "dataset_yolanda nov 8_4.csv", "dataset_yolanda nov 8_5.csv", "dataset_yolanda nov 8_6.csv", "dataset_yolanda nov 8_7.csv", "dataset_yolanda nov 8_8.csv", "dataset_yolanda nov 8_9.csv", "dataset_yolanda nov 8_10.csv", "dataset_yolanda nov 8_11.csv", "dataset_yolanda nov 8_12.csv", "dataset_yolanda nov 8_13.csv", "dataset_yolanda nov 8_14.csv", "dataset_yolanda nov 8_15.csv", "dataset_yolanda nov 8_16.csv", "dataset_yolanda nov 8_17.csv", "dataset_yolanda nov 8_18.csv", "dataset_yolanda nov 8_19.csv",  "dataset_yolanda nov 8_20.csv", "dataset_yolanda nov 8_21.csv", "dataset_yolanda nov 8_22.csv", "dataset_yolanda nov 8_23.csv",]
# files = ['yolanda nov 6.csv']

for filename in files:
	df = pd.read_csv(filename, delimiter=',')
	nlp = spacy.load('en')

	new_words = ["don't", "dont", "typhoon", "yolanda", "bagyo", "bagyong", "yolandaph", "supertyphoon", "super", "Yolanda", "Typhoon", "Super", "Bagyo", "YolandaPH", "YOLANDA"]
	#^ ADDED THIS FOR CLEANER TOPICS SA TOPIC DISTRIBUTION -- WE ALREADY KNOW IT'S ABOUT TYPHOON YOLANDA AND WANT TO GO THROUGH THE OTHER TOPICS 

	for word in new_words:
		lexeme = nlp.vocab[word]
		lexeme.is_stop = True

	start = time.time()
	df['Parsed'] = df['text'].apply(nlp)

	lemmas = []

	for doc in df['Parsed']:
		temp = []
		for w in doc:
			if not w.is_stop and not w.is_punct and not w.like_num and len(w.lemma_) > 2 and '@' not in w.lemma_ and 'http' not in w.lemma_:
				temp.append(str.lower(w.lemma_))
		lemmas.append(temp)

	df['lemmas'] = lemmas

	print
	print (time.time() - start)

	df.to_csv('./lda/[pp_FULL] %s' % filename)