import glob

import numpy as np
import pandas as pd
from keras import backend as K
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.classification import classification_report
from sklearn.preprocessing import LabelEncoder


def read_image(path):
    im = load_img(path,target_size=(150,150))
    return img_to_array(im)


def prepare_data(data_folder, img_width, img_height):
    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)
    K.image_data_format(),input_shape

    print('Getting the images from the data folder')

    images = glob.glob(data_folder + '/**/*jpg')
    images_series = pd.Series(images)
    labels = images_series.apply(lambda x: x.split('/')[-2])

    le = LabelEncoder()
    y = le.fit_transform(labels.values)
    print("{} classes were found:{}".format(len(le.classes_), le.classes_))

    dataset = np.ndarray(shape=(len(images_series), img_height, img_width, 3),
                         dtype=np.float32)

    for ix, path in images_series.iteritems():
        dataset[ix] = read_image(path)
    print("Total number of images in the dataset: {}".format(dataset.shape[0]))
    print("Dimensions of images in the dataset: {}".format(dataset.shape[1:]))

    return dataset, y


def zvsn_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(150, 150, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    return model


def predict(model, datagen, input_features):
    test_gen = datagen.flow(input_features, shuffle=False)
    output = model.predict_generator(test_gen)
    return output


def print_metrics(actual, predicted):
    predicted_ = (predicted > 0.5).astype('int64').ravel()
    print(classification_report(actual, predicted_))
