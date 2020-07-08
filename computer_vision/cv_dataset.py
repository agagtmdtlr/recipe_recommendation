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
from tensorflow.python.keras.layers import Conv2D,MaxPooling2D,Flatten,Dropout

import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import math

class DataSet:
    def __init__(self,input,output):
        self.x,self.y,self.z = input
        self.classes = output

    # Create a description of the features.
    def _parse_function(self,example_proto):
        # Parse the input `tf.Example` proto using the dictionary above.
        feature_description = {
            'image': tf.io.FixedLenFeature([], tf.string, default_value='' ),
            'label': tf.io.FixedLenFeature([], tf.int64, default_value=0 )
        }
        # Load one example
        parsed_features = tf.io.parse_single_example(example_proto, feature_description)

        # Turn your saved image string into an array
        parsed_features['image'] = tf.io.decode_raw(parsed_features['image'], out_type=tf.float32)
        # image = parsed_features['image']
        image = tf.cast(parsed_features['image'], tf.float32) / 255.0

        image = tf.reshape(image, [self.x, self.y ,self.z])

        classes = self.classes
        label = tf.one_hot(parsed_features['label'],classes)
        label = tf.reshape(label, [classes])
        # label = parsed_features['label']

        # parsed_features['image'] = tf.reshape(parsed_features['image'],shape=(224,224,3))
        # return {'image':parsed_features['image'],'label':parsed_features["label"],'x':parsed_features['x'],
        #         'y':parsed_features['y'],'z':parsed_features['z']}
        return image,label

    def tfrecord_dataset(self,path):
        dataset = tf.data.TFRecordDataset(path,compression_type='GZIP')
        return dataset.map(self._parse_function)