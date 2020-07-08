from konlpy.tag import Okt,Mecab
from konlpy.corpus import kobill
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import re,time

okt = Okt()
#mec = Mecab()


# filename1 = '../../../data/crawl_data/recipe_dropna.csv'
# data1 = pd.read_csv(filename1, encoding='UTF-8', index_col=0)
# #mycol = ['recipe_id','cat1','cat2','cat3','cat4']
# data1 = pd.DataFrame(data1)
# data_source = data1.loc[:,['rec_source','rec_step']]
# recss = ['rec_source', 'rec_step']
# start = time.time()
# # 불용어 확보를 위한 테스트
# set_source = set()

# ######### make stopword dict ##################3
# stopword_dict = dict()
# with open('../../../data/nlp_data/source_stopword.txt','r',encoding='utf-8') as f:
#     for kwd in f.readlines():
#         key,values = kwd.split(':')
#         stopword_dict[key] = [i.strip('\n') for i in values.split(',')]
# print(stopword_dict)
#
# # dataframe only rec_source column
#
# norm_source_total = []
#
# for item1 in data_source.iloc[:,0]:
#     #print(item)
#     # catl = 재료 카테고리 주재료,부재료...
#     catl = item1.split('&')
#     norm_sourcel = set()
#     for cat in catl :
#         raw_sourcel = cat.split('|')
#         for source in raw_sourcel:
#             for key,vals in stopword_dict.items():
#                 for v in vals:
#                     if re.match(f'{v}',source):
#                         norm_sourcel.add(key)
#     if len(list(norm_sourcel))>2:
#         norm_source_total.append(norm_sourcel)
#
# print(len(norm_source_total))
#
# print(len(set_source))
# print(sorted(list(set_source)))
# print(list(set_source).sort())
# # pd.DataFrame(sorted(list(set_source))).to_csv('../../../data/nlp_data/split_space_source_keyword02.csv')
# print(time.time() - start)


#print(type(data_source))
#print(data_source.iloc[:,0])

############# multi process #############
class Source:
    def __init__(self):
        ######### make stopword dict ##################3
        self.stopword_dict = dict()
        with open('../../../data/nlp_data/source_stopword.txt', 'r', encoding='utf-8') as f:
            for kwd in f.readlines():
                key, values = kwd.split(':')
                self.stopword_dict[key] = [i.strip('\n') for i in values.split(',')]
        print(self.stopword_dict)

    def subset_kwd(self,row):
        catl = row.split('&')
        norm_sourcel = set()
        for cat in catl:
            raw_sourcel = cat.split('|')
            for source in raw_sourcel:
                for key, vals in self.stopword_dict.items():
                    for v in vals:
                        find = False
                        if re.match(f'.*{v}.*', source):
                            # print(source,vals)
                            norm_sourcel.add(key)
                            find = True
                            break
                        if find : break
        if len(list(norm_sourcel)) > 2:
            return norm_sourcel
        else: return None



from multiprocessing import Pool
if __name__ == '__main__':

    filename1 = '../../../data/pre_process_data/recipe_dropna.csv'
    data1 = pd.read_csv(filename1, encoding='UTF-8', index_col=0)
    # mycol = ['recipe_id','cat1','cat2','cat3','cat4']
    data1 = pd.DataFrame(data1)
    data_source = data1.loc[:, ['rec_source', 'rec_step']]
    recss = ['rec_source', 'rec_step']
    start = time.time()

    source = Source()

    pool = Pool(processes=8)
    norm_source_total = pool.map(source.subset_kwd,data_source.iloc[:,0])
    # norm_source_total = [ i for i in norm_source_total if i is not None ]
    norm_str_list = []
    for norm in norm_source_total:
        if norm:
            norm_str_list.append('|'.join(norm))
        else:
            norm_str_list.append(None)

    df = pd.DataFrame({'rec_title':data1.loc[:,'rec_title'],'kwd_source':norm_str_list})
    cond = pd.notna(df['kwd_source'])
    df = df.loc[cond, :]
    df.to_csv('../../../data/nlp_data/kwd_source.csv',encoding='utf-8')
    norm_source_total = [ i for i in norm_source_total if i is not None ]
    print(len(norm_source_total))
    # 110715
    print(time.time() - start)
    # 65.7620894908905...s