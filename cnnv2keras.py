
# Importing libraries 
import keras
from keras.models import Sequential 
from keras.layers import Dense, Conv2D, Flatten, LeakyReLU, MaxPooling2D
import numpy  as np
import pandas as pd
import cv2
from   random import shuffle
from   tqdm   import tqdm
import os
import time

# Storing image directories 
TRAIN_DIR = 'C:\\Users\\Aditya\\Desktop\\FRAMES\\WarpDetectionSystem\\TrainingData'
TEST_DIR  = 'C:\\Users\\Aditya\\Desktop\\FRAMES\\WarpDetectionSystem\\TestingData'

# Defining image size
IMG_X  = 525
IMG_Y  = 158

# Defining a function to extract labels from image file names

def label_image (img):
    labels = img.split('.')[0]
    if   labels == 'PerfectCorners'  : return [1,0]
    elif labels == 'WarpedCorners'  : return [0,1]

# Defining a function to prepare training data
def create_training_data():
    training_data = []
    for image in os.listdir(TRAIN_DIR):
        label = label_image(image)
        path  = os.path.join(TRAIN_DIR,image)
        img   = cv2.resize(cv2.imread(path,0),(IMG_X, IMG_Y))
        training_data.append([np.array(img),np.array(label)])
    shuffle(training_data)
    np.save('training_data.npy',training_data)
    return training_data

# Defining a function to prepare testing data

def process_testing_data():
    testing_data = []
    for image in os.listdir(TEST_DIR):
        img_num = image.split('.')[0]
        path    = os.path.join(TEST_DIR, image)
        img     = cv2.resize(cv2.imread(path,0),(IMG_X, IMG_Y))
        testing_data.append([np.array(img),np.array(img_num)])
    np.save('testing_data.npy',testing_data)
    return testing_data

# Creating training and testing dataset

# training_data = create_training_data()

testing_data  = process_testing_data()

"""### Building the convolutional network """

# Creating the model
LR          = 1e-3
num_classes = 2
MODEL_NAME  = 'TestModel-{}-{}.model'.format(LR,'ConvNet')

# Building the network

model = Sequential()

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))
          
model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Conv2D(16, kernel_size = (3,3),input_shape = (IMG_X,IMG_Y,1), padding = 'same'))
model.add(LeakyReLU(alpha=LR))
model.add(MaxPooling2D((2,2),padding='same'))

model.add(Flatten())
          
model.add(Dense(2,activation='softmax'))
model.compile(loss = 'binary_crossentropy',optimizer = keras.optimizers.Adam(), metrics = ['accuracy'])

# Splitting training data to training  and validation dataset
train          = training_data[:-50]
validation_set = training_data[-150:]

# Feeding data to the network 
X = np.array([i[0] for i in train]).reshape(-1,IMG_X,IMG_Y,1)
Y = np.array([i[1] for i in train])
validation_x = np.array([i[0] for i in validation_set]).reshape(-1,IMG_X,IMG_Y, 1)
validation_y = np.array([i[1] for i in validation_set])

model.fit(X, Y, validation_data=(validation_x, validation_y), epochs=20)

model.save(MODEL_NAME)

from keras.models import load_model

loading_model = load_model('C:\\Users\\Aditya\\Desktop\\FRAMES\\WarpDetectionSystem\\TestModel-0.001-ConvNet.model')
test_data = testing_data 
with open("CNNv2Prediction.csv",'w') as f:
    f.write('id,label\n')
with open("CNNv2Prediction.csv",'a') as f:
    for num, data in enumerate(test_data):
        if num%1000 == 0: print('write {} line'.format(num))
        img_num = data[1]
        img_data = data[0]
        orig = img_data
        data = img_data.reshape(-1,IMG_X,IMG_Y,1)
        model_out = model.predict([data])[0]
        f.write('{},{}\n'.format(img_num, model_out[0]))
print('done')

