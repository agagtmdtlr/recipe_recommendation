import os
import math
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Conv2D,Flatten,Dropout # 레이어 추가
from tensorflow.python.keras.preprocessing.image import load_img,img_to_array,array_to_img,save_img

class ImgGenerator:
    def get_path(self,folder):
        img_list = [ (i[0],i[2]) for i in list(os.walk(f'../../data/crl_image/{folder}'))[1:]]
        # print(len(img_list))
        # for i in img_list:
        #     print(i)
        return img_list  # [ str , ... ]

    def generator(self,fp,imgs,path):
        # 이미지 증식
        idg = ImageDataGenerator(
            # rescale=1/255, # 스케일 변경
            rotation_range=40.0, # 회전 각도
            width_shift_range=0.2, # 수평 방향 이동 비율
            height_shift_range=0.2, # 수직 방향 이동 비율
            shear_range=0.2, # 반시계 방향의 전단 강도(radian)
            zoom_range=0.2, # 랜덤하게 확대할 사진의 범위 지정
            horizontal_flip=True, # 수평 방향으로 입력 반전
            fill_mode = 'nearest'
            # vertical_flip=True # 수직 방향으로 입력 반전
        )
        class_name = fp.split('\\')[-1]
        for img_fp in imgs:
            img = load_img(fp+'\\'+img_fp)
            ary = img_to_array(img)
            ary = ary.reshape((1,)+ary.shape)

            i = 0
            for batch in idg.flow(ary, batch_size=1,
                                  save_to_dir=f'../../data/crl_image/{path}/{class_name}',
                                  save_prefix=class_name,save_format='jpeg'):
                i += 1
                if i > 20: break
        print(fp,imgs)



if __name__ == '__main__':
    IG = ImgGenerator()
    img_list = IG.get_path('crl_image_extraction')
    # print(img_list[0])
    for fp,imgs in img_list:
        IG.generator(fp,imgs)