from konlpy.tag import Okt,Mecab
from konlpy.corpus import kobill
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import re,time

okt = Okt()
#mec = Mecab()



filename1 = '../../../data/crawl_data/recipe_dropna.csv'
data1 = pd.read_csv(filename1, encoding='UTF-8', index_col=0)

#mycol = ['recipe_id','cat1','cat2','cat3','cat4']
data1 = pd.DataFrame(data1)
data_source = data1.loc[:,['rec_source','rec_step']]
recss = ['rec_source', 'rec_step']

# 불용어 확보를 위한 테스트

set_source = set()
for item1 in data_source.iloc[:,0]:
    #print(item)
    catl = item1.split('&')
    for cat in catl :
        sourcel = cat.split('|')
        for source in sourcel:
            source = source.split(' ')
            set_source.update(source)
print(len(set_source))
print(sorted(list(set_source)))
print(list(set_source).sort())
# pd.DataFrame(sorted(list(set_source))).to_csv('../../../data/nlp_data/split_space_source_keyword.csv')


#print(type(data_source))
#print(data_source.iloc[:,0])


