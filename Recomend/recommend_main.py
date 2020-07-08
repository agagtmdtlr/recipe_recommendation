import os
import tensorflow as tf
import pickle
import cv2
import time
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


from tensorflow.python.keras.preprocessing.image import load_img,img_to_array
from refrigerator_recipe.computer_vision.cv_predict import Prediction

def calculate_distance(x,y):
    lens = len(x)
    distance = 0
    for i in range(lens):
        distance += (x[i] - y[i])**2
    return math.sqrt(distance)

def calculate_consine(x,y):
    lens = len(x)
    x_scale = 0
    y_scale = 0
    xy_dot = 0
    for i in range(lens):
        x_scale += x[i]**2
        y_scale += y[i]**2
        xy_dot += x[i]*y[i]

    return xy_dot/(math.sqrt(x_scale)*math.sqrt(y_scale))

def find_point(SOURCES):
    SOURCE_LEN = len(SOURCES)

    find_point_x = 0
    find_point_y = 0
    find_point_z = 0

    for source in SOURCES:
        find_point_x += sourceFrame.loc[source,'x']
        find_point_y += sourceFrame.loc[source,'y']
        find_point_z += sourceFrame.loc[source,'z']

    # find_point_x = find_point_x/SOURCE_LEN
    # find_point_y = find_point_y/SOURCE_LEN
    # find_point_z = find_point_z/SOURCE_LEN
    return find_point_x,find_point_y,find_point_z

if __name__ == '__main__':

    # ############# 이미지 판별 #############
    # model_path = '../../data/computer_vision_data/resnet_extraction_224__epoch40_85.h5'
    # label_path = '../../data/computer_vision_data/label_dict.txt'
    # prediction = Prediction(model_path,label_path)
    #
    # # load image and convert to array( input shape)
    # img = load_img('C:/Users/TJ/Desktop/연어.jpg')
    # img_array = np.array(img)
    # img_array = cv2.resize(img_array, (224, 224), interpolation=cv2.INTER_AREA) /255.0
    # img_array = img_array.reshape(1,224,224,3)
    # prediction.predict_label(img_array)


    ############# 판별 이미지로 레시피 검색 #############
    source_path = '../../data/nlp_data/source_embedding.csv'
    recipe_path = '../../data/nlp_data/recipe_embedding.csv'
    flask_path = '../../data/nlp_data/recommend_data.csv'
    sourceFrame = pd.read_csv(source_path,index_col=3)
    recipeFrame = pd.read_csv(recipe_path)
    print(sourceFrame.shape,'\n',recipeFrame.shape)

    sources = ['참치','고추']
    select_cat = ('볶음','일상',None,None)
    select_cat = [i for i in select_cat if i is not None]
    my_point = find_point(sources)
    # 각 재료별 좌표를 저장하는 객체
    sources_point_dict = {source: (sourceFrame.loc[source, 'x'],
                                   sourceFrame.loc[source, 'y'],
                                   sourceFrame.loc[source, 'z']) for source in sources}
    print(sources_point_dict.keys())
    # 레시피와 각 재료별 거리를 저장하는 객체
    sources_distance_dict = {source: [] for source in sources}

    select_cat_set = set(select_cat)
    sources_set = set(sources)
    select_length = len(select_cat_set)

    start_time = time.time()
    for idx,row in recipeFrame.iterrows():
        recipe_category = set([row.cat1,row.cat2,row.cat3,row.cat4])
        # 카테고리에 해당되는지
        if len(recipe_category.intersection(select_cat_set)) == select_length:
            # 재료 포함하고 있는지
            recipe_sources = set(row.kwd_source.split('|'))
            if recipe_sources.intersection(sources_set) :
                recipe_point = (row.x, row.y, row.z)
                # 재료별 거리 리스트 만들기 ( 거리, 아이디, 제목, 좌표 )
                for source in sources:
                    distance = calculate_distance(sources_point_dict[source],recipe_point )
                    sources_distance_dict[source].append((distance, row.id, row.title, recipe_point))
    times = time.time() - start_time
    print(times)

    recommend_recipe_set = set()
    for distance_list in sources_distance_dict.values():
        recommend_recipe_set.update(sorted(distance_list,key=lambda x : x[0])[:10])
    [print(i) for i in recommend_recipe_set]

    ############################### DRAW GRAPH ##################################
    plt.rc('font', size=10)  # controls default text sizes
    mpl.rcParams['legend.fontsize'] = 10  # 그냥 오른쪽 위에 뜨는 글자크기 설정이다.

    mpl.rc('font', family='Malgun Gothic')
    fig = plt.figure(figsize=(20,20))  # 이건 꼭 입력해야한다.
    ax = fig.gca(projection='3d')

    recommend_recipe_list = list(recommend_recipe_set)
    t,x,y,z, = [],[],[],[]
    for i in recommend_recipe_list:
        t.append(i[2])
        x.append(i[3][0])
        y.append(i[3][1])
        z.append(i[3][2])
    # 레시피 위치
    ax.plot(x, y, z,'o', label='recipe')  # 위에서 정의한 x,y,z 가지고 그래프그린거다.
    for t,x,y,z in zip(t,x,y,z):
        ax.text(x,y,z,t)
    # 식재료 위치
    for k,v in sources_point_dict.items():
        ax.plot([v[0]],[v[1]],[v[2]],'o',label=k)
        ax.text(v[0],v[1],v[2],k)
    ax.legend()
    plt.show()