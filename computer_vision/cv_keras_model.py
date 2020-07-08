from tensorflow.keras.applications import ResNet50,VGG16,ResNet152
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras import models, layers
from tensorflow.python.keras import losses
from tensorflow.keras import Input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import BatchNormalization, Conv2D, Activation, Dense, GlobalAveragePooling2D, MaxPooling2D, \
    ZeroPadding2D, Add
from tensorflow.python.keras import losses
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Activation # 레이어 추가
from tensorflow.keras import activations,optimizers,metrics #케라스 자체로만 하면 최신 버전 사용 가능
from tensorflow.python.keras.layers import Conv2D,MaxPooling2D,Flatten,Dropout

def keras_vgg16(classes):
    base_model = VGG16(weights='imagenet',include_top=False,input_shape=(224,224,3))

    model = Sequential()
    model.add(base_model)
    model.add(Flatten())
    model.add(Dense(256, activation='relu', name='Dense_Intermediate'))
    model.add(Dropout(0.1, name='Dropout_Regularization'))
    model.add(Dense(classes, activation='softmax', name='Output'))
    for cnn_block_layer in model.layers[0].layers:
        cnn_block_layer.trainable = False
    model.layers[0].trainable = False
    # Compile the model. I found that RMSprop with the default learning
    # weight worked fine.
    model.summary()

    return model

def keras_resnet50(clsses):
    # create the base pre-trained model
    base_model = ResNet50(weights='imagenet', include_top=False)

    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    # let's add a fully-connected layer
    x = Dense(1024, activation='relu')(x)
    # and a logistic layer -- let's say we have 200 classes
    predictions = Dense(clsses, activation='softmax')(x)

    # this is the model we will train2
    model = Model(inputs=base_model.input, outputs=predictions)

    # first: train2 only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional resnet50 layers
    for layer in base_model.layers:
        layer.trainable = False
    model.summary()
    return model


def keras_resnet152(clsses):
    # create the base pre-trained model
    base_model = ResNet152(weights='imagenet', include_top=False)

    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    # let's add a fully-connected layer
    x = Dense(1024, activation='relu')(x)
    # and a logistic layer -- let's say we have 200 classes
    predictions = Dense(clsses, activation='softmax')(x)

    # this is the model we will train2
    model = Model(inputs=base_model.input, outputs=predictions)

    # first: train2 only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional resnet50 layers
    # for layer in base_model.layers:
    #     layer.trainable = False
    model.summary()
    return model

'''
# train2 the model on the new data for a few epochs
model.fit(...)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train2 the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train2 the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from tensorflow.keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train2 our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit(...)
'''

