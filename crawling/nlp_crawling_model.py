import re,time,urllib
import urllib.request
import urllib.error
import pandas as pd
from itertools import count
from bs4 import BeautifulSoup
from bs4 import element
from multiprocessing import Pool

class Crawl:
    # 초기 url 여기에 cat id를 합친다
    get_category_id_url = 'https://www.10000recipe.com/recipe/list.html'
    get_recipe_id_base_url = 'https://www.10000recipe.com/recipe/list.html?cat1={}&cat2={}&cat3={}'
    category4_url = 'https://www.10000recipe.com/recipe/list.html?cat4={}'
    def __init__(self):
        # 대분류별(category1~4) 중분류 정보를 담고 있는 변수 key : id_text / value : id
        self.category1,self.category2,self.category3,self.category4 = {},{},{},{}
        

    def Crawl_category_id(self): # 대분류별 중분류 정보 수집
        '''
        crawling category id(number) from recipe main page
        and setting instances values -> category1~4
        why crawl category id??
            we request url combine category id by get method
        :return: None
        '''
        req = urllib.request.Request(self.get_category_id_url)
        sourcecode = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(sourcecode, "html.parser")


        super_category_list = soup.find("div", id="id_search_category").find_all("div", class_="cate_list")
        pattern = re.compile('[0-9]+') # subset only category id
        super_category_result = []
        # super 순서 ㅊ
        for super_category in super_category_list:
            sub_category_list = super_category.find_all('a')
            sub_category_dict = {}
            # sub_category_list[0]은 '전체' not use
            for a in sub_category_list[1:]:
                #print(a['href'])
                re_str = a['href'].split(',')[1]
                cat_id = pattern.search(re_str).group()
                cat_text = a.text
                sub_category_dict[cat_id] = cat_text

            super_category_result.append(sub_category_dict)
        self.category4, self.category2, self.category3, self.category1 =  super_category_result

    def Crawl_recipe_id(self,c1): # 중분류별 레시피 id 수집
        '''
        catergory1 & category2 & category3 을 동시에 만족하는 recipe들을 찾아 id와 그에 맞는 검색 기준을 attribute취급하여 같이 저장한다.

        count를 이용하여 board page를 넘기기 검색결과가 없으면 해당 category 수집 중단

        :param c1: 방법 분류 id
        :return: recipe_list ( 1 recipe :: 1 dict ) recipe id 가 어떤 중분류(방법, 상황, 재료) 정보를 담고 있는지 같이 저장된다.
        '''
        recipe_id_result = []
        for c2 in self.category2.keys():
            for c3 in self.category3.keys():
                for page_idx in count(1):
                    pageurl = self.get_recipe_id_base_url.format(c1,c2,c3) + '&page=' + str(page_idx) # 방법, 상황, 재료
                    print(pageurl)
                    sourcecode = urllib.request.urlopen(pageurl).read()
                    soup = BeautifulSoup(sourcecode, "html.parser")
                    # print(pageurl)
                    col_xs_list = soup.select("div.col-xs-3")  # 해당 상위 속성 범위 좁히기

                    if len(col_xs_list)>1 : # 검색 결과가 있습니다.
                        for col_xs in col_xs_list:
                            print('-'*60)

                            a = col_xs.select_one('a.thumbnail') # 광고/레시피 중 레시피 요소만 추출
                            if a:
                                recipe_id = a['href'].split('/')[2] # /recipe/id 중 id만 추출
                                print(recipe_id)
                                recipe_id_result.append({'recipe_id':recipe_id,\
                                                    'category1':self.category1[c1],\
                                                    'category2':self.category2[c2],\
                                                    'category3':self.category3[c3]})
                    else: # 검색결과가 없습니다 작업 중단
                        break
        # end for
        return recipe_id_result # 1페이지당 레시피의 결과물

    def Crawl_recipe_id_by_category4(self,c4):
        '''
        category4를 이용하여 각 조건에 해당하는 레시피의 id를 추출한다.

        :param c4: 종류 분류 id
        :return: recipe_list ( 1 recipe :: 1 dict ) recipe id 가 어떤 중분류(종류) 정보를 담고 있는지 같이 저장된다.
        '''
        recipe_list = []

        for page_idx in count(1):
            pageurl = self.category4_url.format(c4) + '&page=' + str(page_idx) # 종류
            print(pageurl)
            sourcecode = urllib.request.urlopen(pageurl).read()
            soup = BeautifulSoup(sourcecode, "html.parser")
            # print(pageurl)
            col_xs_list = soup.select("div.col-xs-3")  # 해당 상위 속성 범위 좁히기

            if len(col_xs_list)>1 : # 검색 결과가 있습니다.
                for col_xs in col_xs_list:
                    print('-'*60)
                    a = col_xs.select_one('a.thumbnail')
                    if a:
                        recipe_id = a['href'].split('/')[2]
                        print(recipe_id)
                        recipe_list.append({'recipe_id':recipe_id,\
                                            'category4':self.category4[c4]
                                            })
            else: # 검색결과가 없습니다
                break
        # end for
        return recipe_list # 1페이지당 레시피의 결과물

    def Crawl_recipe_detail(self,recipe_id):
        rec_dict = {}
        url = 'https://www.10000recipe.com/recipe/'+ str(recipe_id)
        try:
            sourcecode = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(sourcecode, "html.parser")
        except urllib.error.URLError as err:
            print(err)
            return rec_dict


        rec_source = {}  # 레시피 재료
        rec_step = []  # 레시피 순서
        ######## 레시피 id ############
        rec_dict['id'] = str(recipe_id)
        ######### 레시피 제목 #############
        try:
            h3 = soup.find('h3')
            rec_title = h3.get_text()
            rec_dict['rec_title']= rec_title

        except(AttributeError):
            rec_dict['rec_title']='-'
        ######### 레시피 부연 설명 ###########
        try:
            view2_summary_info = soup.find('div', 'view2_summary_info')
            rec_sub = view2_summary_info.get_text().replace('\n', '')
            rec_dict['rec_sub']= rec_sub
        except(AttributeError) as err:
            print(err)
            rec_dict['rec_sub']='-'
        ########## 레시피 재료 ###########
        try:
            rg = re.compile('[\s]{2,}')
            res = soup.find('div', 'ready_ingre3')
            source_category = []
            for n in res.find_all('ul'):
                source_element_list = []
                title = n.find('b').get_text()
                rec_source[title] = ''
                for tmp in n.find_all('li'):
                    text = tmp.get_text().replace('\n', '')
                    text = rg.sub(' ',text)
                    source_element_list.append(text)
                source_category.append('|'.join(source_element_list))
            rec_dict['rec_source']='&'.join(source_category)
        except (AttributeError):
            rec_dict['rec_source']='-'

        ###########  레시피 조리 순서 ############
        res = soup.find('div', 'view_step')
        i = 0
        if (res):
            for n in res.find_all('div', 'view_step_cont'):
                i = i + 1
                rec_step.append(n.get_text().replace('\n', ' '))
                #  나중 순서를 구별 하기 위해 #을 넣는다
            if rec_step:
                rec_dict['rec_step']='|'.join(rec_step)
            else:
                rec_dict['rec_step']='-'

            tag = res.find('div', 'view_tag')
            if tag:
                rec_dict['rec_tag'] = tag.get_text()
                # del recipe_tag[0]
            else:
                rec_dict['rec_tag'] = '-'
        else:
            rec_dict['rec_step'] = '-'
            rec_dict['rec_tag'] = '-'
        # 해시 태그가 글 내에 있는 판단하고 출력 해주는  for문
        print(rec_dict)
        return rec_dict

if __name__=='__main__':
    print('크롤링 시작')
    start_time = time.time()
    #################### step1 ####################
    crawl = Crawl()
    # crawl.Crawl_category_id()
    # print(crawl.category4, crawl.category2, crawl.category3, crawl.category1, sep='\n')

    pool = Pool(processes=16)
    ################### step2 #####################
    step2_result = pool.map(crawl.Crawl_recipe_id,iter(crawl.category1.keys()))
    # df_data = []
    # [df_data.extend(i) for i in step2_result]
    # step2_df = pd.DataFrame(df_data)
    # step2_df.to_csv('../../data/crawl_data/Crawl_recipe_id.csv', encoding='UTF-8', header=True)

    ################### step3 #####################
    # result_list = pool.map(crawl.Crawl_recipe_id_by_category4,iter(crawl.category4.keys()))
    # end = []
    # [end.extend(i) for i in result_list]
    # df = pd.DataFrame(end)
    # df.to_csv('../../data/crawl_data/Crawl_recipe_id_by_category4.csv', encoding='UTF-8', header=True)

    ################## step4 ##############################
    # category_1_3 = pd.read_csv('../../data/crawl_data/Crawl_recipe_id.csv',index_col=0)
    # category_4 = pd.read_csv('../../data/crawl_data/Crawl_recipe_id_by_category4.csv',index_col=0)
    # category = pd.merge(category_1_3,category_4,on='recipe_id')
    # category.to_csv('category.csv',encoding='utf-8', index=False)

    ################ step5 ####################################
    # category = pd.read_csv('../../data/crawl_data/category.csv')
    # pool = Pool(processes=16) # 4개의 프로세스를 사용합니다
    # detail_data = pool.map(crawl.Crawl_recipe_detail, iter(category.iloc[:,0]))
    # detail = pd.DataFrame(detail_data)
    # '''
    # # 중복되는 파일명으로 내용이 덮어쓰기가 될수 있으므로
    # # file_serial_name으로 구별 시킨다.
    # '''
    # file_serial_name = 'serial_n'
    # detail.to_csv('../pre_processing/crawl_data/Crawl_recipe_detail_{}.csv'.format(file_serial_name))

    print("--- %s seconds ---" % (time.time() - start_time))