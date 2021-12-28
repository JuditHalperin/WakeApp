import keras
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import tensorflow as tf
#from keras import metrics
from tensorflow import keras
import sklearn.metrics as metrics
import numpy
from keras.models import load_model
plt.style.use('dark_background')
import os




def plot_imgs(directory, top=10):
    all_item_dirs = os.listdir(directory)
    item_files = [os.path.join(directory, file) for file in all_item_dirs][:5]

    plt.figure(figsize=(20, 20))

    for i, img_path in enumerate(item_files):
        plt.subplot(10, 10, i + 1)

        img = plt.imread(img_path)
        plt.tight_layout()
        plt.imshow(img, cmap='gray')
data_path = "C:\\Users\\ortal\\source\\repos\\DriverDrowsinessDetection\\Data\\Dataset\\train"

directories = ['/no_yawn', '/yawn']

for j in directories:
    plot_imgs(data_path+j)
batch_size = 128
train_datagen = ImageDataGenerator(horizontal_flip = True,
                                  rescale = 1./255,
                                  zoom_range = 0.2,
                                  validation_split = 0.1)

test_datagen = ImageDataGenerator(rescale = 1./255)
train_data_path = "C:\\Users\\ortal\\source\\repos\\DriverDrowsinessDetection\\Data\\Dataset\\train"
test_data_path = "C:\\Users\\ortal\\source\\repos\\DriverDrowsinessDetection\\Data\\Dataset\\test"

train_set = train_datagen.flow_from_directory(train_data_path, target_size = (256,256),
                                              batch_size = batch_size,
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_data_path, target_size = (256,256),
                                              batch_size = batch_size,
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')
actual_labels=[]
actual_labels.extend(test_set.labels)
classes = 2
"""
model = Sequential()
# input layer,creating the first layer input_shape are the variables
# The first hidden layer.
#Here we are learning a total of 32 filters and then we use Max Pooling to reduce the spatial dimensions of the output volume.
# (Activation function decides, whether a neuron should be activated or not by calculating weighted sum and further adding bias with it)
model.add(Conv2D(32, (3,3), padding = 'same', input_shape = (256,256,1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

#The second hidden.
#Here we are learning a total of 64 filters and then we use Max Pooling to reduce the spatial dimensions of the output volume.
model.add(Conv2D(64, (3,3), padding = 'same', activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

#The Third hidden layer.
#Here we are learning a total of 128 filters and then we use Max Pooling to reduce the spatial dimensions of the output volume.
model.add(Conv2D(128,(3,3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(64, activation = 'relu'))

model.add(Dense(classes, activation = 'softmax'))

print(model.summary())
model.compile(loss = 'categorical_crossentropy',optimizer = 'adam' , metrics = ['accuracy'])



model_path="yawn_detection1.h5"
#A callback object can perform actions at various stages of training:
#first parameter is the string representing our filename template.
#we would like to monitor In this case, the validation Accuracy test (val_accuracy).
#Since we are working with score,height is better, so we set mode="max".
#Setting save_best_only=True ensures that the latest best model will not be overwritten.
#the verbose=1 setting simply logs a notification to our terminal when a model is being serialized to disk during training.

checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', verbose=1,
                              save_best_only=True, mode='max')

#checkpoint = ModelCheckpoint(model_path, monitor='val_loss',save_best_only=True, mode='min')

#check points
callbacks_list = [checkpoint]
num_epochs = 40
training_steps=train_set.n//train_set.batch_size
validation_steps =test_set.n//test_set.batch_size
history = model.fit_generator(train_set, epochs=num_epochs, steps_per_epoch=training_steps,validation_data=test_set,
                    validation_steps=validation_steps, callbacks = callbacks_list)
                    """
model = load_model("yawn_detection1.h5")
predictions = model.predict(test_set)
predicted_classes = numpy.argmax(predictions, axis=1)
#tf.keras.metrics.confusion_matrix(actual_labels, predictions)
#tf.math.confusion_matrix(actual_labels, predictions, num_classes=2)
#matrix = tf.math.confusion_matrix(actual_labels.argmax(axis=1), predictions.argmax(axis=1))
#print (predictions[0], actual_labels[0])

confusion_matrix = metrics.confusion_matrix(y_true=actual_labels, y_pred=predicted_classes)
print(confusion_matrix)

"""
plt.figure(figsize=(20,10))
plt.subplot(1, 2, 1)
plt.suptitle('Optimizer : Adam', fontsize=10)
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.show()
plt.figure(figsize=(20,10))
plt.subplot(1, 2, 1)
plt.suptitle('Optimizer : Adam', fontsize=10)
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.show()
"""