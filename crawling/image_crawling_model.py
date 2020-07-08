from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from gensim.models import Word2Vec
import re,time,urllib,os
#from webdriver_manager.chrome import ChromeDriverManager

# for item in keydf_wd:
#     if isinstance(item,str):
#         item  = item.split('|')
#     # print(item)


# print(type(keydf_wd))
# print(keydf_wd)

class ImgSch:
    def __init__(self):
        print('eee')
        pass

    def img_search(self):
        model = Word2Vec.load('../../data/nlp_data/source_word2vec.model')
        vocab = model.wv.vocab
        wdlist = list(vocab.keys())

        # for i in range(0, 4):#len(wdlist)):
        #         #     print(wdlist[i])
        #         #     word = (wdlist[i])
        return wdlist

    def Mk_folder(self, dirlist):
        base_dir = 'C:\\Users\\TJ\\Desktop\\dyffo\\Python\\project_03\\data\\crl_image\\new_crl_image\\'
        os.chdir(base_dir)
        for idx in dirlist:
            path = os.path.join(base_dir, str(idx))
            print(path)
            print(os.getcwd())
            try:
                os.mkdir(path)
            except Exception :
                pass


    def img_crl(self, arg):
        word = arg[0]
        idx = arg[1]
        search = str(word)

        url = f'https://www.google.com/search?q={quote_plus(search)}&source=lnms&tbm=isch&sa=X&ved=' \
              f'2ahUKEwjtkrie6fvpAhWCMN4KHXxsArQQ_AUoAXoECBYQAw&biw=1920&bih=920'


        path = 'D:\chromedriver.exe'
        driver = webdriver.Chrome(path)
        driver.get(url)
        driver.implicitly_wait(3)
        while(True):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(0.5)
            try:
                element = driver.find_element_by_xpath('//input[@class="mye4qd"]')
                if(element is not None):
                    element.click()
                    break
            except Exception:
                continue

        errTime = 0
        successTime = 0

        while(errTime < 20 and successTime <10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.05)
            try:
                element = driver.find_element_by_xpath('//div[@class="mye4qd"]')
                if(element is not None):
                    element.click()
                    successTime += 1
                    errTime = 0
            except Exception:
                errTime += 1


        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        img = soup.select('.rg_i.Q4LuWd')
        n = 1
        imgurl = []

        for i in img:
            try:
                imgurl.append(i.attrs["src"])

            except KeyError:
                imgurl.append(i.attrs["data-src"])


        for i in imgurl:
            urlretrieve(i, "C:\\Users\\TJ\\Desktop\\dyffo\\Python\\project_03\\data\\crl_image\\new_crl_image/{}/" .format(idx) + idx + str(n) +  ".jpg")
            n += 1
            #print(imgurl)
            if (n > 1200 or n == None):
                break

        driver.close()


from multiprocessing import Pool
if __name__=='__main__':
    print('이미지크롤링 시작')
    start_time = time.time()
    # wdlist = ImgSch().img_search()
    # print(wdlist)
    # print(len(wdlist))

    wordlist = ['Sanddab fish', 'Potato', 'raisindry fruits', 'an egg', 'a sweetpotato', 'a oyster', 'a meat',
                'a crab-food', 'a beer', 'an corn']
    dirlist = ['가자미','감자','건포도','달걀','고구마','굴','고기','게','맥주','옥수수']
    # 각식재료별 이미지 별도 폴더 생성
    ImgSch().Mk_folder(dirlist)

    crl_list = list(zip(wordlist,dirlist))
    pool = Pool(processes=2)
    #pool.map(ImgSch().img_crl, wdlist[0:])
    pool.map(ImgSch().img_crl, crl_list)


    print("--- %s seconds ---" % (time.time() - start_time))
