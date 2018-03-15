from lsa_model import train_model
from matrix_similarity import get_matrix_similarity
from convex_hull import get_convex_hull

tweet = ['storm', 'make', 'hard', 'sleep', 'yolanda', 'unta', 'muabot', 'sudden', 'deep', 'slumber']

data = {'output_name': '1', 
		'directory': 'yolanda', 
		'model': '1_model.txt', 
		'dataset': 'dataset_yolanda.csv', 
		'dict': '1_corpus.dict'}
data = get_matrix_similarity(tweet,data)
print(data['filename'])
get_convex_hull(10,data)