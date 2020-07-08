from sklearn.manifold import TSNE
from gensim.models import word2vec,Word2Vec
import pandas as pd
import math
import matplotlib.pyplot as plt

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

    def tsne_w2v(self,model,n_components):
        tsne = TSNE(n_components=n_components)  # 2차원 설정

        # noun_vocab : 학습된 명사 모록
        noun_vocab = [w for w in model.wv.vocab]
        W_data = model.wv[noun_vocab]
        # tsne
        W_tsne = tsne.fit_transform(W_data)

        tsneFrame = pd.DataFrame(W_tsne, index=noun_vocab, columns=['x', 'y'])
        return tsneFrame

    def  show_tsne(self,tsneFrame):
        plt.rc('font', family='Malgun Gothic')
        plt.figure()
        plt.scatter(tsneFrame['x'], tsneFrame['y'])

        plt.title(f'재료의 명사 관계도')
        for word, pos in tsneFrame.iterrows():
            plt.annotate(word, pos, fontsize=15)
        plt.show()
        ### 좌표 그리고 그 표를 파일로 저장하기
        # plt.savefig(f'uclid_data/{label}_noun_scatter.png', dpi=600, bbox_inches='tight')
        ###############################################

if __name__ == '__main__':

    embedding = Embedding('../../../data/nlp_data/norm_kwd_step.csv')
    ''''
    #### make source model ####
    w2vdata = embedding.make_word2vecData()
    model = embedding.embedding_W2V(w2vdata)
    embedding.save_model(model,"../../../data/nlp_data/source_word2vec.model")

    model = Word2Vec.load('../../../data/nlp_data/source_word2vec.model')
    tsneFrame = embedding.tsne_w2v(model,n_components=2)
    embedding.show_tsne(tsneFrame)
    '''



    '''
    ##### make recipe tsne    
    model = Word2Vec.load('../../../data/nlp_data/source_word2vec.model')
    tsneFrame = embedding.tsne_w2v(model, n_components=2)
    real_source = list(tsneFrame.index)

    sourceframe = pd.read_csv('../../../data/nlp_data/kwd_source.csv')
    cond = pd.notna(sourceframe['kwd_source'])
    sourceframe = sourceframe.loc[cond,:]
    recipe_data = list()
    #### 중심좌표 구하기
    for idx,row in sourceframe.iterrows():
        x = 0
        y = 0
        title = row.rec_title
        source_list = [ i for i in row.kwd_source.split('|') if i in real_source ]
        n = len(source_list)
        for source in source_list:
            x += tsneFrame.loc[source,'x']
            y += tsneFrame.loc[source,'y']
        mean_x = x/n
        mean_y = y/n
        recipe_data.append({'title':title,'x':mean_x,'y':mean_y})

    recipeFrame = pd.DataFrame(recipe_data)
    recipeFrame.to_csv('../../../data/nlp_data/recipe_embedding.csv')
    '''

    recipeFrame = pd.read_csv('../../../data/nlp_data/recipe_embedding_sum_vector.csv',index_col=0)
    e = 59618
    point_t = recipeFrame.iloc[e,0]
    point_x = recipeFrame.iloc[e,1]
    point_y = recipeFrame.iloc[e,2]

    distance_dict = dict()
    for idx,row in recipeFrame.iterrows():
          x = (row.x-point_x)**2
          y = (row.y-point_y)**2
          distance = math.sqrt(x+y)
          distance_dict[row.title] = distance

    sort_list = sorted(distance_dict.items(),key=lambda x : x[1])[:10]
    for i in sort_list:
        print(i)


    # ##### make recipe tsne
    # model = Word2Vec.load('../../../data/nlp_data/source_word2vec.model')
    # tsneFrame = embedding.tsne_w2v(model, n_components=2)
    # real_source = list(tsneFrame.index)
    #
    # sourceframe = pd.read_csv('../../../data/nlp_data/kwd_source.csv')
    # cond = pd.notna(sourceframe['kwd_source'])
    # sourceframe = sourceframe.loc[cond,:]
    # recipe_data = list()
    # #### 중심좌표 구하기
    # for idx,row in sourceframe.iterrows():
    #     x = 0
    #     y = 0
    #     title = row.rec_title
    #     source_list = [ i for i in row.kwd_source.split('|') if i in real_source ]
    #
    #     for source in source_list:
    #         x += tsneFrame.loc[source,'x']
    #         y += tsneFrame.loc[source,'y']
    #
    #     recipe_data.append({'title':title,'x':x,'y':y})
    #
    # recipeFrame = pd.DataFrame(recipe_data)
    # recipeFrame.to_csv('../../../data/nlp_data/recipe_embedding_sum_vector.csv')
