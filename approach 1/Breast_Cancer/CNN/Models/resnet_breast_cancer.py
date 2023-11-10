from __future__ import division
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint
from keras.optimizers import SGD,Adam
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import os
import pdb
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
config.gpu_options.visible_device_list = "0"
set_session(tf.Session(config=config))

####################################################################
#Parameters
####################################################################
img_width, img_height = 224, 224
train_data_dir = '/home/Drive2/aditya/Aug_Data/Training/'
validation_data_dir = '/home/Drive2/aditya/Aug_Data/Validation/'
best_epoch_weights = "/home/Drive2/aditya/Weights/res_best_weights.h5"
last_epoch_weights = "/home/Drive2/aditya/Weights/res_last_weights.h5"
initial_weights = best_epoch_weights
batch_size = 32
epochs1 = 10
epochs2 = 20
####################################################################

benign_train_no = len(os.listdir(train_data_dir+"Benign/"))
insitu_train_no = len(os.listdir(train_data_dir+"InSitu/"))
invasive_train_no = len(os.listdir(train_data_dir+"Invasive/"))
normal_train_no = len(os.listdir(train_data_dir+"Normal/"))
total_train_no = benign_train_no + insitu_train_no + invasive_train_no + normal_train_no

nb_train_samples = total_train_no

benign_validation_no = len(os.listdir(validation_data_dir+"Benign/"))
insitu_validation_no = len(os.listdir(validation_data_dir+"InSitu/"))
invasive_validation_no = len(os.listdir(validation_data_dir+"Invasive/"))
normal_validation_no = len(os.listdir(validation_data_dir+"Normal/"))
total_val_no = benign_validation_no + insitu_validation_no + invasive_validation_no + normal_validation_no

nb_validation_samples = total_val_no

class_weight = {0:max(1.0,1.0*total_train_no/benign_train_no),1:max(1.0,1.0*total_train_no/insitu_train_no),2:max(1.0,1.0*total_train_no/invasive_train_no),3:max(1.0,1.0*total_train_no/normal_train_no)}

input_shape = (img_width, img_height, 3)

checkpointer = ModelCheckpoint(filepath= best_epoch_weights, monitor='val_acc',verbose=1, save_best_only=True,save_weights_only=True)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=90,
    vertical_flip=True,
    horizontal_flip=True)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='rgb',
    seed=0)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='rgb',
    seed=0)

model = ResNet50(include_top=True, weights=None, pooling=None, classes=4)
sgd = SGD(lr=0.001, momentum=0.9, decay=1e-6, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit_generator(train_generator,
    steps_per_epoch=nb_train_samples//batch_size,
    epochs=epochs2,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples//batch_size,
    callbacks=[checkpointer],
    class_weight=class_weight)

model.save_weights(last_epoch_weights)
"""
test_datagen = ImageDataGenerator(rescale=1. / 255)

test_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    color_mode='rgb',
    batch_size=batch_size,
    shuffle=False,
    seed=0)

result = model.predict_generator(
        test_generator,
        steps=nb_validation_samples//batch_size)
"""

#pdb.set_trace()
