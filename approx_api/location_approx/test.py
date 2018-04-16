#
# df = pd.read_csv('./data/dataset/dataset_yolanda.csv')
# lemmas_list = []
#
# count = 0
# for lemmas in df['lemmas']:
#     if count == 30:
#         break
#     lemmas = str(lemmas)
#     lemmas = lemmas.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
#     lemmas_list.append(lemmas.split())
#     count += 1
#
# data = train_model('dataset_yolanda.csv',uuid.uuid4())
# data = get_matrix_similarity(lemmas_list,data)
# data = get_convex_hull(10,data)
#
# print(data)

def hello():
    print('hello')
