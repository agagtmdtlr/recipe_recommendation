from konlpy.tag import Okt,Mecab
from konlpy.corpus import kobill
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import re,time

okt = Okt()
#mec = Mecab()


filename1 = '../../../data/crawl_data/recipe_dropna.csv'
data1 = pd.read_csv(filename1, encoding='UTF-8', index_col=0).head(10)
#mycol = ['recipe_id','cat1','cat2','cat3','cat4']
data1 = pd.DataFrame(data1)
data_source = data1.loc[:,['rec_source','rec_step']]
recss = ['rec_source', 'rec_step']

class konlpy:

    def __init__(self):
        pass

    # def RERE(self,data):
    #     for item in data['rec_source']:
    #         #ang = item
    #         ang = re.split('[0-9][^0-9]',item)
    #
    #     return ang


    def df_token(self, recss):
        rec_souce = []
        rec_step = []
        rec_step_adj = []

        for item in recss:
            for line in data_source[str(item)]:
                if item == 'rec_source':
                    token_1 = okt.nouns(line)
                    rec_souce.append(token_1)
                elif item == 'rec_step':
                    # print(line)
                    token_2 = okt.nouns(line)
                    rec_step.append(token_2)

                    token_3 = okt.pos(line)
                    a = []
                    for token in token_3:
                        if token[1] == 'Adjective':
                            b = token[0]
                            a.append(b)
                    rec_step_adj.append(a)

        data_source.loc[:, 'rec_source'] = rec_souce
        data_source.loc[:, 'rec_step'] = rec_step
        data_source['rec_step_pos'] = rec_step_adj
        list1 = rec_souce
        list2 = rec_step
        return list1, list2, data_source


    def Check_token(self,list1, list2):
        ########################################
        # 재료 토큰, 순서 토큰 내부 비교
        n = 0
        tot = []
        for i in range(0, len(list1)):
            not_subset_token = []
            for x in list1[i]:
                if x not in list2[i]:
                    # print(x)
                    not_subset_token.append(x)
            if not_subset_token: n+=1
            tot.append(not_subset_token)
        # for l in tot:
        #     print(l)
        # print(n)
        return tot, n
        #########################################

if __name__ == '__main__':
    start_time = time.time()
    kon = konlpy()

    #data_source.to_csv('test_token.csv')
    l1,l2,data_s = kon.df_token(recss)
    #print(l1)
    #print(l2)
    tot, n = kon.Check_token(l1,l2)
    #[print(l) for l in tot]
    #print(n)
    newlist = []
    allkey = []
    i = 0
    print(l1)
    for idx10 in l1:
        for idx9 in idx10:
            newlist.append(idx9)

    set_newlist = set(newlist)
    print(set_newlist)
    print('-' * 40)
    count = 0
    for item in set_newlist:
        count = count + 1
        print('count_({}) >>>>> {}'.format(count, item))



    data_s.to_csv('../../../data/process_data/test_token1.csv')
    #ang = kon.RERE(data_source)
    #print(ang)
    # print(data_source)
    # print(kon)
    print("--- %s seconds ---" % (time.time() - start_time))









# # stopfile = 'stopword.txt'
# # stopword = open(stopfile, encoding='UTF-8').read()
#
# start_time = time.time()
#
# filename1 = '../../../data/crawl_data/recipe_dropna.csv'
#
# data1 = pd.read_csv(filename1, encoding='UTF-8', index_col=0).head(10)
#
# #mycol = ['recipe_id','cat1','cat2','cat3','cat4']
#
# data1 = pd.DataFrame(data1)
#
# data_source = data1.loc[:,['rec_source','rec_step']]
#
# #print(data_source.loc[data_source[1],'rec_source'])
# recss = ['rec_source', 'rec_step']
# #print(data_source[['rec_source', 'rec_step']])
#
# #print(data_source)
#
# rec_souce = []
# rec_step = []
# rec_step_adj = []
#
# for idx in recss:
#     for line in data_source[str(idx)]:
#         if idx == 'rec_source':
#             token_1 = okt.nouns(line)
#             rec_souce.append(token_1)
#         elif idx == 'rec_step':
#             #print(line)
#             token_2 = okt.nouns(line)
#             rec_step.append(token_2)
#
#             token_3 = okt.pos(line)
#             a = []
#             for token in token_3:
#                 if token[1] == 'Adjective':
#                     b = token[0]
#                     a.append(b)
#             rec_step_adj.append(a)
#             #news_word = okt.nouns(line)
#             #print(news_word)
#
# #print(rec_souce)
# #print(rec_step)
# #print(rec_step_adj)
#
# data_source.loc[:,'rec_source'] = rec_souce
# data_source.loc[:,'rec_step'] = rec_step
# data_source['rec_step_pos'] = rec_step_adj
#
# #print(data_source)
# #[[0 for j in range(2)] for i in range(3)]
#
# list1 = rec_souce
# list2 = rec_step
#
# # 3개 컬럼다 타입은 여기까지 list 로 반환
#
# #print(set(list1) == set(list2))
# ########################################
# # 재료 토큰, 순서 토큰 내부 비교
# n = 0
# tot = []
# for i in range(0,len(list1)):
#     not_subset_token = []
#     for x in list1[i]:
#         if x not in list2[i]:
#             # print(x)
#             not_subset_token.append(x)
#     tot.append(not_subset_token)
# for l in tot:
#     print(l)
# print(n)
#
# #########################################
#
#
# data_source.to_csv('test_token.csv')
#
#
#
# print("--- %s seconds ---" % (time.time() - start_time))



