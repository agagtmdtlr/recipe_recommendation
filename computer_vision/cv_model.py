from tensorflow.keras import models, layers
from tensorflow.python.keras import losses
from tensorflow.keras import Input
from tensorflow.keras.models import Model, load_model
# from keras.preprocessing.image import ImageDataGenerator
# from keras import optimizers, initializers, regularizers, metrics
# from keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.layers import BatchNormalization, Conv2D, Activation, Dense, GlobalAveragePooling2D, MaxPooling2D, \
    ZeroPadding2D, Add
from tensorflow.python.keras import losses
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Activation # 레이어 추가
from tensorflow.keras import activations,optimizers,metrics #케라스 자체로만 하면 최신 버전 사용 가능
from tensorflow.python.keras.layers import Conv3D,MaxPooling3D,Conv2D,MaxPooling2D,Flatten,Dropout

import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import math



def conv1_layer(x):
    x = ZeroPadding2D(padding=(3, 3))(x)
    x = Conv2D(64, (7, 7), strides=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = ZeroPadding2D(padding=(1, 1))(x)

    return x


def conv2_layer(x):
    x = MaxPooling2D((3, 3), 2)(x)

    shortcut = x

    for i in range(3):
        if (i == 0):
            x = Conv2D(64, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(64, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(256, (1, 1), strides=(1, 1), padding='valid')(x)
            shortcut = Conv2D(256, (1, 1), strides=(1, 1), padding='valid')(shortcut)
            x = BatchNormalization()(x)
            shortcut = BatchNormalization()(shortcut)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

        else:
            x = Conv2D(64, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(64, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(256, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

    return x


def conv3_layer(x):
    shortcut = x

    for i in range(4):
        if (i == 0):
            x = Conv2D(128, (1, 1), strides=(2, 2), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(128, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(512, (1, 1), strides=(1, 1), padding='valid')(x)
            shortcut = Conv2D(512, (1, 1), strides=(2, 2), padding='valid')(shortcut)
            x = BatchNormalization()(x)
            shortcut = BatchNormalization()(shortcut)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

        else:
            x = Conv2D(128, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(128, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(512, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

    return x


def conv4_layer(x):
    shortcut = x

    for i in range(6):
        if (i == 0):
            x = Conv2D(256, (1, 1), strides=(2, 2), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(256, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(1024, (1, 1), strides=(1, 1), padding='valid')(x)
            shortcut = Conv2D(1024, (1, 1), strides=(2, 2), padding='valid')(shortcut)
            x = BatchNormalization()(x)
            shortcut = BatchNormalization()(shortcut)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

        else:
            x = Conv2D(256, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(256, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(1024, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

    return x


def conv5_layer(x):
    shortcut = x

    for i in range(3):
        if (i == 0):
            x = Conv2D(512, (1, 1), strides=(2, 2), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(512, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(2048, (1, 1), strides=(1, 1), padding='valid')(x)
            shortcut = Conv2D(2048, (1, 1), strides=(2, 2), padding='valid')(shortcut)
            x = BatchNormalization()(x)
            shortcut = BatchNormalization()(shortcut)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

        else:
            x = Conv2D(512, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(512, (3, 3), strides=(1, 1), padding='same')(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

            x = Conv2D(2048, (1, 1), strides=(1, 1), padding='valid')(x)
            x = BatchNormalization()(x)

            x = Add()([x, shortcut])
            x = Activation('relu')(x)

            shortcut = x

    return x

def ResNet(inputs,outputs):
    x,y,z = inputs

    input_tensor = Input(shape=(x, y, z), dtype='float32', name='input')

    x = conv1_layer(input_tensor)
    x = Dropout(0.2)(x)
    x = conv2_layer(x)
    x = Dropout(0.2)(x)
    x = conv3_layer(x)
    x = Dropout(0.2)(x)
    x = conv4_layer(x)
    x = Dropout(0.2)(x)
    x = conv5_layer(x)

    x = GlobalAveragePooling2D()(x)


    x = Dense(1024,kernel_regularizer=tf.keras.regularizers.l2(0.001), activation='relu')(x)
    # x = Dropout(0.5)(x)
    x = Dense(512,kernel_regularizer=tf.keras.regularizers.l2(0.001), activation='relu')(x)
    # x = Dropout(0.5)(x)

    outputs_tensor= Dense(outputs,activation='softmax')(x)
    resnet50 = Model(input_tensor, outputs_tensor)
    resnet50.summary()
    return resnet50

from tensorflow.keras.applications import ResNet50,VGG16

def Own(inputs,outputs):
    x, y, z = inputs
    model = Sequential()
    # convolution layer
    # padding = 'valid' (행열수 줄어듬), 'same' ( 행열수 보존 )
    # filter 개수는 보통 32,64...
    # Conv2D : input_shape -> ( 높이,너비,채널수 )
    # 채널수는 흑백 : 1  컬럼 : 3(RGB)
    # strides = (1,1) default
    # convolution도 여러개로
    model.add(
        Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu, input_shape=(x, y, z),padding='same'))
    model.add(
        Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu, padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(
        Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu),padding='same')
    model.add(
        Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu),padding='same')
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu))

    # 4차원 데이터를 2차원으로 축소하기
    model.add(Flatten())

    # full connected
    model.add(Dense(units=1024, activation=activations.relu))
    model.add(Dropout(0.3),name='Dropout_Regularization')
    model.add(Dense(units=outputs, activation=activations.softmax))

    model.summary()

    return model

def img64NN(inputs,outputs):
    x, y, z = inputs
    model = Sequential()

    model.add(
        Conv2D(filters=64, kernel_size=(5, 5),strides=(1,1),
               activation='relu', input_shape=(x, y, z),
               padding='same',use_bias=True))
    model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),
                           padding='same'))
    # model.add(Dropout(0.5))
    model.add(
        Conv2D(filters=64, kernel_size=(3, 3),strides=(1,1),
               activation='relu',
               padding='same',use_bias=True))
    model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),
                           padding='same'))
    #model.add(Dropout(0.5))
    # model.add(Dropout(0.5))
    # L3
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
   # model.add(Dropout(0.5))
    # L4
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
    # model.add(Dropout(0.5))
    # L5
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
    # model.add(Dropout(0.5))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),
                           padding='same'))
    # 4차원 데이터를 2차원으로 축소하기
    model.add(Flatten())
    # kernel_regularizer=tf.keras.regularizers.l2(0.001)
    # full connected
    model.add(Dense(units=384, activation=activations.relu,kernel_regularizer=tf.keras.regularizers.l2(0.001),use_bias=True))
    # model.add(Dropout(0.5))
    model.add(Dense(units=192, activation=activations.relu,use_bias=True))
    model.add(Dense(units=outputs, activation=activations.softmax))
    model.summary()

    return model

def img224NN(inputs,outputs):
    x, y, z = inputs
    model = Sequential()
    # convolution layer
    # padding = 'valid' (행열수 줄어듬), 'same' ( 행열수 보존 )
    # filter 개수는 보통 32,64...
    # Conv2D : input_shape -> ( 높이,너비,채널수 )
    # 채널수는 흑백 : 1  컬럼 : 3(RGB)
    # strides = (1,1) default
    # convolution도 여러개로
    model.add(
        Conv2D(filters=64, kernel_size=(5, 5),strides=(1,1),
               activation='relu', input_shape=(x, y, z),
               padding='same',use_bias=True))
    model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),
                           padding='same'))
    model.add(Dropout(0.2))

    model.add(
        Conv2D(filters=64, kernel_size=(3, 3),strides=(1,1),
               activation='relu',
               padding='same',use_bias=True))
    model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),
                           padding='same'))
    model.add(Dropout(0.2))
    # L3
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
    model.add(Dropout(0.2))
    # L4
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
    model.add(Dropout(0.2))
    # L5
    model.add(
        Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
               activation='relu',
               padding='same', use_bias=True))
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),
                           padding='same'))

    # 4차원 데이터를 2차원으로 축소하기
    model.add(Flatten())

    # full connected
    model.add(Dense(units=384, activation=activations.relu,
                    use_bias=True))
    model.add(Dropout(0.5))
    model.add(Dense(units=192, activation=activations.relu,
                    use_bias=True))
    model.add(Dropout(0.5))

    model.add(Dense(units=outputs, activation=activations.softmax))

    model.summary()

    return model