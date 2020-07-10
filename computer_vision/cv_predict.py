
import numpy as np
from recipe_recommendation.computer_vision.cv_model import ResNet

class Prediction:
    def __init__(self,model_path,label_path):
        self.model = ResNet((224, 224, 3), 144)
        self.model.load_weights(model_path)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['accuracy', 'top_k_categorical_accuracy', 'categorical_crossentropy'])
        # make label dictionary
        self.labeling_dict = dict()
        f = open(label_path, 'r', encoding='utf-8')
        label_list = f.readlines()
        for label in label_list:
            key, value = label.strip('\n').split(':')
            self.labeling_dict[key] = value

    def predict_label(self,img_array):
        prediction = self.model.predict(img_array)
        # one_hot_encoding convert to integer
        prediction = np.argmax(prediction[0])
        prediction = self.labeling_dict[str(int(prediction))]
        print('predict : ', prediction)
        return prediction
if __name__ == '__main__':
    pass
