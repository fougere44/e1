import numpy as np
import pandas as pd
import random
import cv2

import os
import sys
from os import listdir
from os.path import isfile, join

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from PIL import Image

import keras
import keras.backend as K
from keras.models import load_model
from keras.layers import Input, Dense, merge
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, Reshape, BatchNormalization, SeparableConv2D, Activation
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import metrics

import sklearn
from sklearn.metrics import mean_squared_error

import mlflow
import mlflow.tensorflow


mlflow.tensorflow.autolog()


def load_photos(directory):
    '''
    Loads the photo from the directory and return arrays of images and labels
    '''
    images = []
    directions = []
    vitesses = []
    dir_list = listdir(directory)
    random.shuffle(dir_list)
    for name in dir_list:
        filename = directory + '/' + name
        image = load_img(filename, target_size=(120, 160))
        # est ce nécessaire de resize ?
        image = img_to_array(image)
        images.append(image)
        direction = float((name.split('_')[2]).split('.jpg')[0])
        directions.append(direction)
        vitesse = float(name.split('_')[1])
        vitesses.append(vitesse)
    return images, directions, vitesses

X, Y, Z = load_photos("../data/images_data/images/circuits/entrainement")
print('Images chargées pour entraînement :',len(X))

X = np.array(X)
X /= 255.0


def mirror_image(X,Y,Z):
    '''
    Do a horizontal flip on every images of the dataset
    '''
    X_mirror = []
    Y_mirror = []
    Z_mirror = []
    i=0

    for image in X:
        image = cv2.flip(image, 1)# 1 correspond to horizontal
        X_mirror.append(image)
        Y_mirror.append(np.flip(Y[i]))
        Z_mirror.append(np.flip(Z[i]))
        i=i+1
    return X_mirror,Y_mirror, Z_mirror


def random_brightness(X,Y,Z):
    X_bright = []
    Y_bright = []
    Z_bright = []
    i=0

    for image in X:
        # HSV (Hue, Saturation, Value) is also called HSB ('B' for Brightness).
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        ratio = 1 + 0.8 * (np.random.rand() - 0.5)
        hsv[:,:,2] =  hsv[:,:,2] * ratio
        tmp = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        X_bright.append(tmp)
        Y_bright.append(Y[i])
        Z_bright.append(Z[i])
        i=i+1
    return X_bright, Y_bright, Z_bright


#Here we augment the data with the previously declared functions, you should adapt if you don't want to use all the
# augmentation functions
X_bright, Y_bright, Z_bright = random_brightness(X, Y, Z)
X_tmp = np.concatenate((X, X_bright))
Y_tmp = np.concatenate((Y, Y_bright))
Z_tmp = np.concatenate((Z, Z_bright))

X_mirror, Y_mirror, Z_mirror = mirror_image(X_tmp,Y_tmp,Z_tmp)
X_final = np.concatenate((X_tmp, X_mirror))
Y_final = np.concatenate((Y_tmp, Y_mirror))
Z_final = np.concatenate((Z_tmp, Z_mirror))


print('Le dataset est desormais composé de', len(Z_final),'images')
y_final = [(Y_final), (Z_final)]


#define our model
def getModelCustom():

    model_name = "../models/output_model/test_custom_v3.h5"
    K.clear_session()

    #Building the model
    img_in = Input(shape=(120, 160, 3), name='img_in')
    x = img_in

    #Conv Layer 1
    x = Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(x)

    #Conv Layer 2
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

    
    #Conv Layer 3
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)


    #Conv Layer 4
    x = Conv2D(256, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(x)


    #Conv Layer 5
    x = Conv2D(256, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(x)


    #Conv Layer 6
    x = Conv2D(512, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(x)
    

    x = Flatten(name='flattened')(x)
    # Flatten to 1D (Fully connected)
    

    x = Dense(1024, activation='relu', use_bias=False)(x)                                   
    x = Dropout(0.4)(x)                                                      
    x = Dense(512, activation='relu', use_bias=False)(x)                                     
    x = Dropout(0.2)(x)

    angle_out = Dense(1, activation='linear', name='angle_out', use_bias=False)(x)  
    throttle_out = Dense(1, activation='linear', name='throttle_out', use_bias=False)(x)
  
    model = Model(inputs=[img_in], outputs=[angle_out, throttle_out])

    model.compile(loss='mse', optimizer="adam", metrics=[metrics.mean_squared_error, metrics.mean_absolute_error, metrics.categorical_accuracy])

    best_checkpoint = keras.callbacks.ModelCheckpoint(model_name, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

    try:
        h_custom = model.fit(X_final, y_final, batch_size=64, validation_split=0.2, epochs=50, verbose=1, callbacks=[best_checkpoint])
    except NameError:
        print('Augmented data have not been found, original data will be used')
        h_custom = model.fit(X, Y, batch_size=64, epochs=50, validation_split=0.2, verbose=1, callbacks=[best_checkpoint])
        
    history_custom = pd.DataFrame(h_custom.history, index=h_custom.epoch)
    history_custom.to_csv('../models/dataframe_model/test_custom_v3.csv', index = False)

    model.summary()

    return model

#model_custom = getModelCustom()




def getModelDonkeyCar():

    model_name_donkey = "../models/output_model/test_donkey_v3.h5"

    model = keras.models.load_model("../models/model_entree/mypilot.h5")

    model.compile(optimizer='adam', loss = 'mse',
            metrics=[metrics.mean_squared_error, 
                       metrics.mean_absolute_error, 
                       #metrics.mean_absolute_percentage_error,
                       metrics.categorical_accuracy])

    best_checkpoint_2 = keras.callbacks.ModelCheckpoint(model_name_donkey, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

    try:
        h_donkey = model.fit(X_final, y_final, batch_size=64, validation_split=0.2, epochs=50, verbose=1, callbacks=[best_checkpoint_2])
    except NameError:
        print('Augmented data have not been found, original data will be used')
        h_donkey = model.fit(X, Y, batch_size=64, epochs=50, validation_split=0.2, verbose=1, callbacks=[best_checkpoint_2])

    history_donkey = pd.DataFrame(h_donkey.history, index=h_donkey.epoch)
    history_donkey.to_csv('../models/dataframe_model/test_donkey_v3.csv', index = False) 

    model.summary()

    return model


model_donkey = getModelDonkeyCar()







