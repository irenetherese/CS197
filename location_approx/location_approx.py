from lsa_model import train_model
from matrix_similarity import get_matrix_similarity
from convex_hull import get_convex_hull


data = {}

print(data)
data = train_model('dataset_yolanda.csv','1')
print(data)
data['directory'] = 'yolanda'

tweet = ['pagasa', 'typhoon', 'yolanda', 'expect', 'enter', 'area', 'responsibility', 'midnight', 'yolandaph']

data = get_matrix_similarity(tweet,data)
print(data)
output = get_convex_hull(10,data)

print(output)

