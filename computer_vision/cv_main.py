from datetime import datetime

import tensorboard
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
from recipe_recommendation.computer_vision.cv_model import ResNet,Own,img64NN,img224NN
from recipe_recommendation.computer_vision.cv_dataset import DataSet
from recipe_recommendation.computer_vision.cv_keras_model import keras_resnet50,keras_vgg16,keras_resnet152
from tensorflow.python.keras import losses

if __name__ == '__main__':
    # tf.debugging.set_log_device_placement(True)

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        # 텐서플로가 첫 번째 GPU만 사용하도록 제한
        try:
            tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        except RuntimeError as e:
            # 프로그램 시작시에 접근 가능한 장치가 설정되어야만 합니다
            print(e)
    with tf.device('/GPU:0'):
        writer = tf.summary.create_file_writer('')
        inputs = (224,224,3)
        outputs = 144
        epochs = 10
        batchs = 10
        opt = 'adam'

        # 같은 모델이라도 옵션이 다를수 있는 부가적인 이름을 추가해쥇요

        modelname_detail = '_extraction_224'
        dataset_version = '_extraction_224'


        dataset = DataSet(inputs,outputs)
        print(' ############모델 선택하기##################\n'
              ' Own : o \n'
              ' ResNet : r \n'
              ' Keras50 : k \n'
              ' VGG16 : v \n'
              ' Keras152 : 152\n'
              ' img64 : 64\n'
              ' img224 : 224\n'
              ' .... : \n')
        command_key = input('키를 입력하세요( 대소문자 상관없음 ) : ').lower()


        # choice model and built model graph of end compile
        if command_key in ('r','ㄱ'):
            model = ResNet(inputs,outputs)
            modelname = f'resnet{modelname_detail}'
        elif command_key in ('o','ㅐ'):
            model = Own(inputs,outputs)
            modelname = f'own{modelname_detail}'
        elif command_key in ('k','ㅏ'):
            model = keras_resnet50(outputs)
            modelname = f'keras50{modelname_detail}'
        elif command_key in ('v','ㅍ'):
            model = keras_vgg16(outputs)
            modelname = f'vgg16{modelname_detail}'
        elif command_key in ('152'):
            model = keras_resnet152(outputs)
            modelname = f'keras152{modelname_detail}'
        elif command_key in ('64'):
            model = img64NN(inputs,outputs)
            modelname = f'img64{modelname_detail}'
        elif command_key in ('224'):
            model = img224NN(inputs,outputs)
            modelname = f'img224{modelname_detail}'

        earlystop = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=1)
        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=f'../../data/computer_vision_data/{modelname}__checkpoint.h5',
                                                        monitor='accuracy')
        logdir="../../logs/fit/"+datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=f'../../data/computer_vision_data/{modelname}_checkpoint.h5',
            save_weights_only=False,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True)

        model_path = f'../../data/computer_vision_data/{modelname}_model.h5'
        model.compile(loss=losses.categorical_crossentropy, optimizer=opt,
                      metrics=['accuracy', 'top_k_categorical_accuracy', 'categorical_crossentropy'])

        # create or load model path


        # if exist model load and evaluate
        # or not exist create model and fit(train2) and evaluate and save model
        if os.path.isfile(model_path): # exist model
            print("Yes. it is a file")
            model.load_weights(model_path)
        elif os.path.isdir(model_path):
            print("Yes. it is a directory")
        elif os.path.exists(model_path):
            print("Something exist")
        else: # not exist model
            print("Nothing")



        train_dataset = dataset.tfrecord_dataset(f'../../data/computer_vision_data/train{dataset_version}.tfrecord')

        train_dataset = train_dataset.batch(batchs)
        valid_dataset = dataset.tfrecord_dataset(f'../../data/computer_vision_data/valid{dataset_version}.tfrecord')
        valid_dataset = valid_dataset.batch(batchs)
        print('fitting 중입니다.')
        # model.fit(train_dataset, epochs=epochs,batch_size=batchs, verbose=1,validation_data=valid_dataset)

        history = model.fit(train_dataset, epochs=epochs,callbacks=[tensorboard_callback],
                            verbose=1,validation_data=valid_dataset)
        # model.save(model_path)

        with open(f'../../data/graph/trainHistory{modelname}', 'wb') as file_pi:
            pickle.dump(history.history, file_pi)

        # ## draw graph ##
        # plt.figure(figsize=(16,10))
        # plt.plot(history.epoch, history.history['val_accuracy'],
        #                '--', label='val'.title() + '_accuracy')
        # plt.plot(history.epoch, history.history['accuracy'],
        #          color='r', label='tset'.title() + ' _accuracy')
        # plt.xlabel('Epochs')
        # plt.ylabel('accuracy'.title())
        # plt.title(f'{modelname}_accuracy')
        # plt.legend()
        #
        # plt.xlim([0, max(history.epoch)])
        # plt.savefig(f'../../data/graph/{modelname}_accuracy.jpg')
        # plt.show()
        ## draw graph ##

        # test_dataset = dataset.tfrecord_dataset(f'../../data/computer_vision_data/test{dataset_version}.tfrecord')
        # test_dataset = test_dataset.shuffle(buffer_size=500)


        # print('evaluate 중입니다.')
        # test_loss, test_acc, test_top_k, test_cate_cross = model.evaluate(test_dataset, batch_size=batchs, verbose=1)
        # print('test_acc : %.4f' % test_acc)
        # print('test_loss : %.4f' % test_loss)
        # print('test_top_k : %.4f' % test_top_k)
        # print('test_categoricat_crossentropy : %.4f' % test_cate_cross)
        # print('-' * 50)
