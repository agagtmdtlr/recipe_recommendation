import numpy as np
import pandas as pd
import cx_Oracle
import re
from multiprocessing import Pool

class RecipePreProcess:
    def __init__(self):
        pass
    def concat_data(self,x,y):
        return pd.concat([x,y],axis=0,ignore_index=True)
    def merge_data(self,x,y,on):
        return pd.merge(x,y,how='inner',on=on)

    # 파일명과 데이터 프레임을 넣어 준다.
    def save_data(self,filename,df):
        if isinstance(df,pd.DataFrame):
            # 파일명, 데이터의 범위를 표시해준다.
            df.to_csv('../../data/pre_process_data/{}.csv'.format(filename),encoding='utf-8',index=False)
        else:
            print('argument type not dataframe')

    def str_drop_na(self,recipe_raw):
        print('drop before',recipe_raw.shape)
        for x in recipe_raw.columns[1:]:
            recipe_raw.loc[recipe_raw[x] == '-',x] = np.nan
        print(recipe_raw)
        drop_na = recipe_raw.dropna(axis=0) #(125964, 10)
        for x in range(1,9):
            print(f'column {x} :',sum(drop_na.iloc[:,x] == '-'))
        print('drop after',drop_na.shape)
        return drop_na

    # 해당 데이터프레임을 oracle table에 insert한다.
    '''
    (recipe_id                                                      6930519
    cat1                                                         볶음
    cat2                                                         일상
    cat3                                                       돼지고기
    cat4                                                       메인반찬
    rec_title                                               [돼지불고기]
    rec_sub                                         3인분 30분 이내 아무나 
    rec_source    돼지고기 앞다리살 760g|양파 1/2개|쪽파 1줌|다진마늘 1T|고추장 3T|설탕...
    rec_step      재료와 양념은 사진상으로 참고하시면 좋을 것 같아서 올려봅니다 ^^|돼지고기 앞다리...
    '''
    def df_to_oracle(self,df): # insert data to oracle table
        conn = None
        cur = None
        try:
            loginfo = 'recommend/oracle@localhost:1521/xe'
            conn = cx_Oracle.connect(loginfo, encoding = 'utf-8')
            cur = conn.cursor()
            if isinstance(df,pd.DataFrame):
                print(max([ len(i) for i in df['rec_step']]))
                for idx,row in df.iterrows():
                    sql = f" insert into recipe_infos " \
                          f"(id, cat1, cat2, cat3, cat4) " \
                          f" values('{row.id}','{row.cat1}','{row.cat2}','{row.cat3}'," \
                          f" '{row.cat4}')"
                    cur.execute(sql)
                    sql = " update recipe_infos set "
                    sql += self.execute_to_clob('rec_title',row.rec_title)+" , "
                    sql += self.execute_to_clob('rec_sub',row.rec_sub)+" , "
                    sql += self.execute_to_clob('rec_source',row.rec_source)+" , "
                    sql += self.execute_to_clob('rec_step',row.rec_step)
                    sql += f" where id = '{row.id}'"
                    cur.execute(sql)
                    print(idx)
                    pd.re
                conn.commit()
            else:
                print('argument type not dataframe')
        except Exception as err:
            print(err)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    def sql_to_clob(self,col,text):
        sql = f" {col} = "
        lens = len(text)
        text = text.replace("'",'"')
        to_clob_list = []
        for x in range(0,lens,1000):
            if lens - x < 1000:
                to_clob_list.append(f" to_clob(' {text[x:]} ')")
            else:
                to_clob_list.append(f" to_clob(' {text[x:1000+x]} ')")
        sql = sql + " || ".join(to_clob_list)

        # print(sql)
        return sql

    def select_all_db(self,path):
        conn = None
        cur = None
        try:
            loginfo = 'recommend/oracle@localhost:1521/xe'
            conn = cx_Oracle.connect(loginfo, encoding='utf-8')
            cur = conn.cursor()
            # recipe_table ( 최종 필터링된 테이블 ) 존재하는 상태에서 불러올수있다.
            sql = ' select * from recipe_finals '
            db_df = pd.read_sql(sql=sql, con=conn)
            db_df.columns = [column.lower() for column in db_df]
            print(db_df.shape)
            db_df.to_csv(path, index=False)
        except Exception as err:
            print(err)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()


if __name__ == '__main__':
    recipepp = RecipePreProcess()

    ################# multi process ######################
    # loginfo = 'recommend/oracle@localhost:1521/xe'
    # pool = cx_Oracle.SessionPool(loginfo,min=2,max=5,increment = 1,threaded=True,encoding='utf-8')
    # conn = pool.acquire()
    #
    # recipepp.conn.commit()
    # recipepp.conn.close()
    ##########################################

    ####################### step1 ########################
    # category = pd.read_csv('../../data/crawl_data/category.csv',index_col=0)
    # detail = pd.read_csv('../../data/crawl_data/Crawl_recipe_detail_0_135345.csv',index_col=0)
    # recipe = recipepp.merge_data(category,detail,'recipe_id')
    # print(recipe.shape,len(recipe))
    # recipepp.save_data('recipe_raw',recipe)
    ########################################################

    ######################## step2 ###########################
    # recipe = pd.read_csv('../../data/pre_process_data/recipe_raw.csv')
    # print(recipe.shape, len(recipe))
    # print(recipe)
    # drop_na = recipepp.str_drop_na(recipe.iloc[:,:9])
    # drop_na.to_csv('../../data/pre_process_data/recipe_dropna.csv',index=False)

    ###################### step [ 3 or 4 ] ###################

    ######################## step5 #####################

    ###################### step6 ###########################
    recipepp.select_all_db('../../data/pre_process_data/recipe_nlp.csv')

    ####################################################################
    recipepp.select_all_db('../../data/nlp_data/recipe_nlp.csv')

    '''
    Index(['recipe_id', 'cat1', 'cat2', 'cat3', 'cat4', 'rec_title',
       'rec_sub', 'rec_source', 'rec_step', 'rec_tag'],
      dtype='object')
    '''
    '''
    D:\Phycharm_pss\global_interpreter\venv\lib\site-packages\pandas\core\ops\array_ops.py:253:
    FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
    res_values = method(rvalues)
    '''