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
from refrigerator_recipe.computer_vision.cv_model import ResNet

class Datas:
    def __init__(self):
        self.recommend_recipe_set = None
        self.sources_point_dict = None

datas = Datas()
app = Flask(__name__)
app_root = os.path.abspath(os.path.dirname(__file__))


def load_model():
    # 미리 학습된 Keras 모델을 불러옵니다(여기서 우리는 ImageNet으로 학습되고
    # Keras에서 제공하는 모델을 사용합니다. 하지만 쉽게 하기위해
    # 당신이 설계한 신경망으로 대체할 수 있습니다.)
    global prediction
    model_path = '../data/computer_vision_data/resnet_extraction_224__epoch40_85.h5'
    label_path = '../data/computer_vision_data/label_dict.txt'
    prediction = Prediction(model_path, label_path)


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

    # def predict_label(img_array):
    #     global labeling_dict
    #     global model
    #     prediction = model.predict(img_array)
    #     # one_hot_encoding convert to integer
    #     prediction = np.argmax(prediction[0])
    #     prediction = labeling_dict[str(int(prediction))]
    #     print('predict : ', prediction)
    #     return prediction

    global datas

    if request.method == 'POST':
        start = time.time()




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

        # load image and convert to array( input shape)
        sources_set = set()
        sources_predict = []
        for imagename in filenames:
            img = load_img(f'static/naver/{imagename}')
            img_array = np.array(img)
            img_array = cv2.resize(img_array, (224, 224), interpolation=cv2.INTER_AREA) / 255.0
            img_array = img_array.reshape(1, 224, 224, 3)
            predict_label = prediction.predict_label(img_array)

            sources_set.add(predict_label)  # 레시피 찾는데 사용할것
            sources_predict.append(predict_label)  # html에 출력하는데 사용할것

        ############# 판별 이미지로 레시피 검색 #############

        sources = list(sources_set)

        ################################# 레시피 찾기 ########################
        flask_path = '../data/nlp_data/recommend_data.csv'
        FlaskFrame = pd.read_csv(flask_path, index_col=(1, 2, 3, 4))


        request_cate = [(request.form['cate1']),(request.form['cate2']),(request.form['cate3']),(request.form['cate4'])]
        cate = [slice(None),slice(None),slice(None),slice(None)]
        for idx in range(4):
            if request_cate[idx] not in ('방법별','상황별','재료별','종류별'):
                cate[idx] = request_cate[idx]

        columns = ['id','title']
        columns.extend(sources)

        print(cate)
        print(columns)

        print(FlaskFrame.loc[cate,columns])
        frame_None = FlaskFrame.loc[cate, columns]

        print(list(frame_None.columns))
        print(frame_None.sort_values(by=list(frame_None.columns)[2:]))

        final_recipe_dict = dict()

        for source in list(frame_None.columns)[2:]:
            source_frame = frame_None.loc[:, ('id', 'title', source)].dropna().sort_values(by=(source))[0:5]
            final_recipe_dict.update({d[0]: d[1] for d in zip(source_frame.id, source_frame.title)})

        print(final_recipe_dict)

        print(time.time() - start)

        return render_template('test_output.html',
                              label=filenames,
                              recommend_recipe_dict=final_recipe_dict,
                              predict=sources_predict,
                              lenghts = len(filenames))

# @app.route('/loding')
# def loding():
#     return render_template('loding.html', title='loding')

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
    # http://112.186.93.164:5000/
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_memory_growth(gpus[0], True)
        except RuntimeError as e:
            # 프로그램 시작시에 메모리 증가가 설정되어야만 합니다
            print(e)
    load_model()

    app.run(host='112.186.93.164',port='5000',debug = True)
    # http://192.168.0.3:5000/