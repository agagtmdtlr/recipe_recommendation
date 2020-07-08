from flask import Flask, render_template, redirect, request, url_for, send_file, jsonify
import flask
import cv2
import time
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from tensorflow.python.keras.preprocessing.image import load_img,img_to_array
from refrigerator_recipe.computer_vision.cv_predict import Prediction
from refrigerator_recipe.Recomend.recommend_main import *
from werkzeug.utils import secure_filename
import os
from flask import Response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Datas:
    def __init__(self):
        self.recommend_recipe_set = None
        self.sources_point_dict = None

datas = Datas()
app = Flask(__name__)
app_root = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/fileUpload', methods = ['GET', 'POST'])
# 이미지 파일 업로드 및 출력 시도
def upload_file():
    global datas
    if request.method == 'POST':

        cat1 = request.form['cate1']
        cat2 = request.form['cate2']
        cat3 = request.form['cate3']
        cat4 = request.form['cate4']
        #저장할 경로 + 파일명
        print(app_root)
        # return 'uploads 디렉토리 -> 파일 업로드 성공!'
        filenames = []
        for file in request.files.getlist('file'):
          file.save(app_root + '/static/naver/' + file.filename)
          filenames.append(file.filename)

        ############# 이미지 판별 #############
        # '../../data/computer_vision_data/resnet_extraction_224__epoch40_85.h5'
        # '../../data/computer_vision_data/label_dict.txt'
        model_path = '../../../data/computer_vision_data/resnet_extraction_224__epoch40_85.h5'
        label_path = '../../../data/computer_vision_data/label_dict.txt'
        prediction = Prediction(model_path, label_path)
        # load image and convert to array( input shape)
        sources_set = set()
        sources_predict = []
        for imagename in filenames:
            img = load_img(f'static/naver/{imagename}')
            img_array = np.array(img)
            img_array = cv2.resize(img_array, (224, 224), interpolation=cv2.INTER_AREA) / 255.0
            img_array = img_array.reshape(1, 224, 224, 3)
            predict_label = prediction.predict_label(img_array)

            sources_set.add(predict_label) # 레시피 찾는데 사용할것
            sources_predict.append(predict_label) # html에 출력하는데 사용할것

        ############# 판별 이미지로 레시피 검색 #############
        # '../../data/nlp_data/source_embedding.csv'
        # '../../data/nlp_data/recipe_embedding.csv'
        source_path = '../../../data/nlp_data/source_embedding.csv'
        recipe_path = '../../../data/nlp_data/recipe_embedding.csv'
        sourceFrame = pd.read_csv(source_path, index_col=3)
        recipeFrame = pd.read_csv(recipe_path)
        print(sourceFrame.shape, '\n', recipeFrame.shape)

        sources = list(sources_set)
        select_cat = (cat1, cat2, cat3, cat4)
        select_cat = [i for i in select_cat if i not in ('방법별','상황별','재료별','종류별')]
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

        ################################# 레시피 찾기 ########################
        start_time = time.time()
        for idx, row in recipeFrame.iterrows():
            recipe_category = set([row.cat1, row.cat2, row.cat3, row.cat4])
            # 카테고리에 해당되는지
            if len(recipe_category.intersection(select_cat_set)) == select_length:
                # 재료 포함하고 있는지
                recipe_sources = set(row.kwd_source.split('|'))
                if recipe_sources.intersection(sources_set):
                    recipe_point = (row.x, row.y, row.z)
                    # 재료별 거리 리스트 만들기 ( 거리, 아이디, 제목, 좌표 )
                    for source in sources:
                        distance = calculate_distance(sources_point_dict[source], recipe_point)
                        sources_distance_dict[source].append((distance, row.id, row.title, recipe_point))
        times = time.time() - start_time
        print(times)

        recommend_recipe_set = set()
        for distance_list in sources_distance_dict.values():
            recommend_recipe_set.update(sorted(distance_list, key=lambda x: x[0])[:10])
        [print(i) for i in recommend_recipe_set]

        datas.recommend_recipe_set = recommend_recipe_set
        datas.sources_point_dict = sources_point_dict
        return render_template('about.html',
                              label=filenames,
                              recommend_recipe_set=recommend_recipe_set,
                              predict=sources_predict,
                              lenghts = len(filenames))

@app.route('/loding')
def loding():
    return render_template('loding.html', title='loding')

@app.route('/plot.png')
def plot_png():
    global datas
    print('set',datas.recommend_recipe_set)
    print('dict',datas.sources_point_dict)
    fig = create_figure(datas.recommend_recipe_set,datas.sources_point_dict)
    output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    FigureCanvas(fig).print_figure(output,facecolor='orange')
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(recommend_recipe_set,sources_point_dict):
    ############################### DRAW GRAPH ##################################
    plt.rc('font', size=10)  # controls default text sizes
    mpl.rcParams['legend.fontsize'] = 10  # 그냥 오른쪽 위에 뜨는 글자크기 설정이다.

    mpl.rc('font', family='Malgun Gothic')
    fig = plt.figure(figsize=(10, 10))  # 이건 꼭 입력해야한다.
    ax = fig.gca(projection='3d')

    recommend_recipe_list = list(recommend_recipe_set)
    t, x, y, z, = [], [], [], []
    for i in recommend_recipe_list:
        t.append(i[2])
        x.append(i[3][0])
        y.append(i[3][1])
        z.append(i[3][2])
    # 레시피 위치
    ax.plot(x, y, z, 'o', label='recipe')  # 위에서 정의한 x,y,z 가지고 그래프그린거다.
    for t, x, y, z in zip(t, x, y, z):
        ax.text(x, y, z, t)
    # 식재료 위치
    for k, v in sources_point_dict.items():
        ax.plot([v[0]], [v[1]], [v[2]], 'o', label=k)
        ax.text(v[0], v[1], v[2], k)
    ax.legend()
    return fig
    
if __name__ == '__main__':
    #서버 실행
    app.run( host="112.186.93.164",debug = True)
