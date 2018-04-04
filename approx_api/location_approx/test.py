from lsa_model import train_model
from matrix_similarity import get_matrix_similarity
from convex_hull import get_convex_hull

tweet = ['alright', 'confirm', 'class', 'level', 'rizal', 'province', 'suspend', 'tom', 'supertyphoon']



data = {'output_name': '1', 
		'directory': 'yolanda', 
		'model': '1_model.txt', 
		'dataset': 'dataset_yolanda.csv', 
		'dict': '1_corpus.dict'}

data = train_model('dataset_yolanda.csv','1')
data['directory'] = 'stress'
print(data)
data = get_matrix_similarity(tweet,data)
print(data['filename'])
print(get_convex_hull(10,data))