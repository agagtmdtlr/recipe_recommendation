import os,time,cv2
import numpy as np
from PIL import Image
from gensim.models import Word2Vec

class Resize:
    def __init__(self):
        pass

    def img_search(self):
        model = Word2Vec.load('../../data/nlp_data/source_word2vec.model')
        vocab = model.wv.vocab
        wdlist = list(vocab.keys())

        return wdlist

    def Mk_folder(self,dirlist):
        base_dir = 'C:/Users/TJ/Desktop/dyffo/Python/project_03/data/crl_image/new_crl_image_resize/'
        os.chdir(base_dir)
        for idx in dirlist:
            path = os.path.join(base_dir, str(idx))
            print(path)
            #print(os.getcwd())
            try:
                os.mkdir(path)
            except Exception :
                pass

    def Resize_img(self, word):
        original_path = 'C:/Users/TJ/Desktop/dyffo/Python/project_03/data/crl_image/new_crl_image/{}/'.format(word)
        resized_path = 'C:/Users/TJ/Desktop/dyffo/Python/project_03/data/crl_image/new_crl_image_resize/{}/'.format(word)

        file_list = os.listdir(original_path)
        img_list = []

        for item in file_list :
            if item.find('.jpg') is not -1 :
                img_list.append(item)
        print(img_list)
        total_image = len(img_list)
        index = 0

        for name in img_list :

            img = Image.open('%s%s'%(original_path, name))
            print(img)
            img_array = np.array(img)
            img_resize = cv2.resize(img_array, (224,224), interpolation = cv2.INTER_AREA)
            img = Image.fromarray(img_resize)
            print(resized_path,name)
            img.save(resized_path + name)

            print(name + '   ' + str(index) + '/' + str(total_image))
            index = index + 1

from multiprocessing import Pool
if __name__=='__main__':
    print('이미지크롤링 시작')
    start_time = time.time()
    # wdlist = Resize().img_search()
    # print(wdlist)
    # print(len(wdlist))
    dirlist = ['가자미', '감자', '건포도', '달걀', '고구마', '굴', '고기', '게', '맥주', '옥수수']
    # 각식재료별 이미지 별도 폴더 생성
    Resize().Mk_folder(dirlist)

    pool = Pool(processes=8)
    #pool.map(ImgSch().img_crl, wdlist[0:])
    pool.map(Resize().Resize_img, dirlist, time.sleep(5))


    print("--- %s seconds ---" % (time.time() - start_time))