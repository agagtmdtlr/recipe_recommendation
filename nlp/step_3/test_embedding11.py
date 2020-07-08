from sklearn.manifold import TSNE
from gensim.models import word2vec,Word2Vec
import pandas as pd
import math
import matplotlib.pyplot as plt

train_data = pd.read_csv('../../../data/nlp_data/recipe_embedding.csv', index_col=0)
print(train_data)

model = Word2Vec