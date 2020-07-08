import os
import random
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.python.keras.preprocessing.image import load_img,img_to_array,save_img

class SeparateData:
    def __init__(self):
        pass

    def get_path(self,folder):
        img_list = [(i[0], i[2]) for i in list(os.walk(f'../../data/crl_image/{folder}'))[1:]]
        print(len(img_list))
        # for i in img_list:
        #     print(i[0],i[1],sep='\n')
        return img_list  # [ ( str, list ) , ... ]

    def seperate_file(self,img_path):
        train = []
        test = []

        for path, file_list in img_path:
            lens = len(file_list)
            random.seed(1000)
            random.shuffle(file_list)
            point = int(0.7 * lens)
            train.append((path, file_list[:point]))
            test.append((path, file_list[point:]))
        return train, test

    def move_image(self,group_dir,fp,imgs):
        base_path = '../../data/crl_image/'
        group_path = base_path+group_dir
        move_path = group_path+'/'+fp.split('\\')[-1]
        print(move_path)
        # print(fp,img)
        if os.path.exists(group_path):
            print('true')
        else:
            os.mkdir(group_path)
        if os.path.exists(move_path):
            print('true')
        else:
            os.mkdir(move_path)
        for img in imgs:
            image_obj = load_img(fp+'\\'+img)
            save_img(move_path+'\\'+img,image_obj)

if __name__ == '__main__':
    separate = SeparateData()
    image_list = separate.get_path('crl_image_resize_extraction_end')
    train, test = separate.seperate_file(image_list)
    for fp,imgs in train:
        separate.move_image('train',fp,imgs)
    for fp,imgs in test:
        separate.move_image('test',fp,imgs)

