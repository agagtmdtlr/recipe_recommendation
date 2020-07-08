from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from gensim.models import word2vec,Word2Vec

import random
import numpy as np
import pandas as pd
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Embedding:
    def __init__(self,path):
        self.df = pd.read_csv(path,index_col=0)
        self.df.columns = ['id','rec_step']

    def make_word2vecData(self):
        cond = pd.notna(self.df['rec_step'])
        word2vec_data = [row.split('|') for row in self.df.loc[cond, 'rec_step']]
        return word2vec_data

    def embedding_W2V(self,word2vec_data):
        model = word2vec.Word2Vec(word2vec_data, size=200, window=5, hs=1, min_count=1, sg=1,iter=6)
        return model

    def save_model(self,model,path):
        model.save(path)

    def pca_w2v(self,model,n_components):

        pca = PCA(n_components=n_components)

        # noun_vocab : 학습된 명사 모록
        noun_vocab = [w for w in model.wv.vocab]
        W_data = model.wv[noun_vocab]
        # pca
        W_pca = pca.fit_transform(W_data)

        col = ['d' + str(i) for i in range(1, n_components + 1)]
        tsneFrame = pd.DataFrame(W_pca, index=noun_vocab, columns=col)
        return tsneFrame

    def tsne_w2v(self,W_data,noun_vocab,n_components):
        tsne = TSNE(n_components=n_components)  # 2차원 설정
        # tsne
        W_tsne = tsne.fit_transform(W_data)

        col = ['d'+str(i) for i in range(1,n_components+1)]
        tsneFrame = pd.DataFrame(W_tsne, index=noun_vocab, columns=col)
        return tsneFrame

    #only 2d
    def  show_tsne(self,tsneFrame):
        plt.rc('font', family='Malgun Gothic')
        plt.rc('font', size=20)
        plt.figure(figsize=(15,15))
        plt.scatter(tsneFrame['d1'], tsneFrame['d2'])

        plt.title(f'재료의 명사 관계도')
        for word, pos in tsneFrame.iterrows():
            plt.annotate(word, pos, fontsize=10)
        plt.savefig('../../../data/nlp_data/imsi.png', dpi=600, bbox_inches='tight')
        plt.show()
        ### 좌표 그리고 그 표를 파일로 저장하기
        ###############################################

if __name__ == '__main__':

    embedding = Embedding('../../../data/nlp_data/norm_kwd_step.csv')

    #### make source model ####
    # w2vdata = embedding.make_word2vecData()
    # model = embedding.embedding_W2V(w2vdata)
    # embedding.save_model(model,"../../../data/nlp_data/source_word2vec.model")

    model = Word2Vec.load('../../../data/nlp_data/source_word2vec.model')
    pcaFrame = embedding.pca_w2v(model, n_components=50)
    noun_vocab = [w for w in model.wv.vocab]
    tsneFrame = embedding.tsne_w2v(pcaFrame,noun_vocab,n_components=2)
    embedding.show_tsne(tsneFrame)



    # model = Word2Vec.load('../../../data/nlp_data/source_word2vec.model')
    # pcaFrame = embedding.pca_w2v(model, n_components=50)
    # print(pcaFrame)
    # #
    # # ###### noun_vocab : 학습된 명사 모록
    # noun_vocab = [w for w in model.wv.vocab]
    # tsneFrame = embedding.tsne_w2v(pcaFrame, noun_vocab,n_components=3)
    # print(tsneFrame)
    # tsneFrame.columns = ['x','y','z']
    # tsneFrame = tsneFrame + 1000
    # tsneFrame['source'] = noun_vocab
    # tsneFrame.to_csv('../../../data/nlp_data/source_embedding.csv',index=False)
    # real_source = list(tsneFrame.index)
    #
    # sourceframe = pd.read_csv('../../../data/nlp_data/recipe_nlp.csv') # 레시피별 위치를 구하기 위해서 가져온다. ( 레시피가 가지고 있는 식재료 데이터 : 중복제거)
    # print(sourceframe.shape)
    #
    # cond = pd.notna(sourceframe['kwd_source'])
    # sourceframe = sourceframe.loc[cond,:]
    # sourceframe.to_csv('../../../data/nlp_data/recipe_nlp.csv',index=False)
    #
    # print(sourceframe.shape)
    # recipe_data = list()
    # #### 중심좌표 구하기
    # for idx,row in sourceframe.iterrows():
    #     x = 0
    #     y = 0
    #     z = 0
    #
    #     title = row.rec_title
    #     id = row.recipe_id
    #     cat1,cat2,cat3,cat4 = row.cat1,row.cat2,row.cat3,row.cat4
    #     kwd_source = row.kwd_source
    #     print(row.kwd_source)
    #     source_list = [ i for i in row.kwd_source.split('|') if i in real_source ]
    #     if len(source_list):
    #         n = len(source_list)
    #         for source in source_list:
    #             x += tsneFrame.loc[source,'x']
    #             y += tsneFrame.loc[source,'y']
    #             z += tsneFrame.loc[source,'z']
    #
    #         mean_x = x/n
    #         mean_y = y/n
    #         mean_z = z/n
    #
    #         recipe_data.append({'id':id,'cat1':cat1,'cat2':cat2,'cat3':cat3,'cat4':cat4,'title':title,'kwd_source':kwd_source,'x':mean_x,'y':mean_y,'z':mean_z})
    #         # recipe_data.append({'id': id, 'title': title,'kwd_source':kwd_source, 'x': x, 'y': y, 'z': z})
    # # #
    # recipeFrame = pd.DataFrame(recipe_data)
    # print(recipeFrame.shape)
    # recipeFrame.to_csv('../../../data/nlp_data/recipe_embedding.csv',index=False)

    ###########

    # ran = np.random.randint(1,10000,50)
    # print(ran)
    # recipeFrame = pd.read_csv('../../../data/nlp_data/recipe_embedding.csv',index_col=0).iloc[ran,:]
    # recipeFrame.set_index(keys='title',inplace=True)
    # print(recipeFrame)
    # # embedding.show_tsne(recipeFrame.iloc[:1000])
    # e = 2
    # point_x = recipeFrame.iloc[e,0]
    # point_y = recipeFrame.iloc[e,1]
    # point_z = recipeFrame.iloc[e,2]
    #
    # distance_dict = dict()
    # for idx,row in recipeFrame.iterrows():
    #       x = (row.x-point_x)**2
    #       y = (row.y-point_y)**2
    #       z = (row.z-point_z)**2
    #       distance = math.sqrt(x+y+z)
    #       distance_dict[idx] = distance
    #
    # sort_list = sorted(distance_dict.items(),key=lambda x : x[1])[:30]
    # for i in sort_list:
    #     print(i)

    ############################### DRAW GRAPH ##################################
    # mpl.rcParams['legend.fontsize'] = 10  # 그냥 오른쪽 위에 뜨는 글자크기 설정이다.
    # mpl.rc('font', family='Malgun Gothic')
    # fig = plt.figure(figsize=(20,20))  # 이건 꼭 입력해야한다.
    # ax = fig.gca(projection='3d')
    # theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)  # 각도의 범위는 -4파이 에서 +4파이
    # z = recipeFrame['z']  # z는 -2부터 2까지 올라간다.
    # x = recipeFrame['x']  # 나선구조를 만들기 위해 x는 sin함수
    # y = recipeFrame['y']  # 나선구조를 만들기 위해 y는 cos함수
    # ax.plot(x, y, z,'o', label='parametric curve')  # 위에서 정의한 x,y,z 가지고 그래프그린거다.
    # ax.legend()  # 오른쪽 위에 나오는 글자 코드다. 이거 없애면 글자 사라진다. 없애도 좋다.
    # for t,x,y,z in zip(recipeFrame['title'],x,y,z):
    #     ax.text(x,y,z,t)
    # plt.show()




