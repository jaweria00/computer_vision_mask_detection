# -*- coding: utf-8 -*-
"""mask_detection_jiya.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ou51C8QP1siLUd7dB3DR81Vs266cxvSq
"""

import keras_preprocessing
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint


#for accuracy and loss graph
import matplotlib.pyplot as plt

import tensorflow
print(keras.__version__)
print(tensorflow.__version__)

train_data_path = "/content/drive/MyDrive/Colab Notebooks/mask detection/dataset/train"
validation_data_path = "/content/drive/MyDrive/Colab Notebooks/mask detection/dataset/valid"

# check for augmented images
def plotImages(images_arr):
  fig, axes = plt.subplots(1, 5, figsize=(20, 20))
  axes = axes.flatten()
  for img, ax in zip(images_arr, axes):
    ax.imshow(img)
  plt.tight_layout()
  plt.show()

# this is the augmentation configuration we will use for trainig
#it generates more images using the parameters defined below
# deep learning requires a lot of datasets for prediction model to work well
#use augmentation configuration to generate more images using datasets, and use 
#the parameters as shown below, augemnt images based on parameters below(zoom, crop, resize etc)
training_datagen = ImageDataGenerator(rescale=1./255,
                                      rotation_range=40,
                                      width_shift_range=0.2,
                                      height_shift_range=0.2,
                                      shear_range=0.2,
                                      zoom_range=0.2,
                                      horizontal_flip=True,
                                      fill_mode='nearest')

#this data will read images from dataset(from train data) 
# and generate batches of augmented data indefinitely
training_data = training_datagen.flow_from_directory(train_data_path, #target directory we want to use
                                                     target_size=(200,200), #resize the images to this
                                                     batch_size= 128,
                                                     class_mode= 'binary') #since we use binary_crossentropy loss, we need binary

training_data.class_indices

#rescaling
#augmentation configuration to be used for validation
valid_datagen = ImageDataGenerator(rescale=1./255)
#we now apply similar generator for the validation data(above we did it for training data)
validation_data = valid_datagen.flow_from_directory(validation_data_path, #target directory we want to use
                                                     target_size=(200,200), #resize the images to this
                                                     batch_size= 128,
                                                     class_mode= 'binary') #since we use binary_crossentropy loss, we need binary

validation_data.class_indices

#check to see augmented images
images=[training_data[0][0][0] for i in range(5)]
plotImages(images)

#save the best model among all the epochs
model_path = '/content/drive/MyDrive/Colab Notebooks/mask detection/model/model.h5'
checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]