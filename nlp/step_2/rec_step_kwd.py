from konlpy.tag import Okt
from multiprocessing import Pool

import pandas as pd
import re,time

class Step:
    def __init__(self):
        self.okt = None
        ######### make stopword dict ##################3
        self.stopword_dict = dict()
        with open('../../../data/nlp_data/step_stopword.txt', 'r', encoding='utf-8') as f:
            for kwd in f.readlines():
                key, values = kwd.split(':')
                self.stopword_dict[key] = [i.strip('\n') for i in values.split(',')]
        print(self.stopword_dict)

    def init_okt(self):
        self.okt = Okt()

    def rec_step_tokenize(self, iterrow):
        token_set = set()
        sentence_list = iterrow[1].rec_step.split('|')
        for sentence in sentence_list:
            token_list = self.okt.nouns(sentence)
            token_set.update(token_list)
        return token_set

    def Check_token(self,list1, list2):
        n = 0
        tot = []
        for i in range(0, len(list1)):
            not_subset_token = []
            for x in list1[i]:
                if x not in list2[i]:
                    not_subset_token.append(x)
            if not_subset_token: n+=1
            tot.append(not_subset_token)
        return tot, n

    def subset_kwd(self, row):
        norm_stepl = []
        id = row[1].id
        raw_stepl = row[1].rec_step.split('|')
        for step_kwd in raw_stepl:
            for key, vals in self.stopword_dict.items():
                for v in vals:
                    self.find = False
                    if re.match(f'.*{v}.*', step_kwd):
                        norm_stepl.append(key)
                        self.find = True
                        break
                    if self.find: break
        return id,'|'.join(norm_stepl)
# class Step
okt = None

def multiprocessing_initializer():
    global okt
    okt = Okt()

def rec_step_tokenize(iterrow):
    token_row = ''
    id = iterrow[1].id
    sentence_list = iterrow[1].rec_step.split('|')
    for sentence in sentence_list:
        token_list = okt.nouns(sentence)
        # print(token_list,type(token_list))
        # token_list = [i[0] for i in token_list if i[1] in ('Noun','Verb')]
        token_row += '|'.join(token_list)
    return id,token_row


if __name__ == '__main__':
    start_time = time.time()

    filename1 = '../../../data/crawl_data/recipe_dropna.csv'
    data1 = pd.read_csv(filename1, encoding='UTF-8')
    data_source = data1.loc[:, ('id','rec_step')]
    # print(data_source)



    '''
    step = Step()
    all_token_set = set()
    if isinstance(data_source,pd.DataFrame):
        for row in data_source.iterrows():
            print(row)
            all_token_set.update(step.rec_step_tokenize(row))
        df_data = sorted(list(all_token_set))
        print(df_data)
        pd.DataFrame(df_data).to_csv('../../../data/nlp_data/kwd_step.csv')
    print("--- %.4f seconds ---" % (time.time() - start_time))
    '''
    '''
    all_token_set = set()
    pool = Pool(processes=8,initializer=multiprocessing_initializer)
    tokens_l = pool.map(rec_step_tokenize,data_source.iterrows())
    id = [i[0] for i in tokens_l]
    step = [i[1] for i in tokens_l]
    pd.DataFrame({'id':id,'rec_step':step}).to_csv('../../../data/nlp_data/kwd_step_noun_okt.csv')
    # _pickle.PicklingError: Can
    # 't pickle <java class '
    # kr.lucypark.okt.OktInterface
    #'>: attribute lookup kr.lucypark.okt.OktInterface on jpype._jclass failed
    '''
    filename = '../../../data/nlp_data/kwd_step_noun_okt.csv'
    data_source = pd.read_csv(filename, encoding='utf-8',index_col=0)
    step = Step()
    # print(sum(pd.notna(data_source['rec_step'])))
    data_source = data_source.loc[pd.notna(data_source['rec_step']),:]
    pool = Pool(processes=8)
    norm_step_l = pool.map(step.subset_kwd,data_source.iterrows())
    pd.DataFrame(norm_step_l).to_csv('../../../data/nlp_data/norm_kwd_step.csv',encoding='utf-8')
    print("--- %.4f seconds ---" % (time.time() - start_time))


