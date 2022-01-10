
# Neural network model for the yawn classification


# import packages
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
import matplotlib.pyplot as plt

# dataset paths
train_data_path = "../Data/Dataset/train"
validation_data_path = "../Data/Dataset/validation"

# define an image generator to format images before using them
train_data_generator = ImageDataGenerator(horizontal_flip=True, rescale=1./255, zoom_range=0.2, validation_split=0.1)
validation_data_generator = ImageDataGenerator(rescale=1./255)

# pre-process images using the image generator
train_set = train_data_generator.flow_from_directory(train_data_path, target_size=(256, 256), batch_size=128, color_mode='grayscale', class_mode='categorical')
validation_set = validation_data_generator.flow_from_directory(validation_data_path, target_size=(256, 256), batch_size=128, color_mode='grayscale', class_mode='categorical')

# model layers building: create a sequence of layers by adding one layer at a time until the network architecture is satisfying
model = Sequential()

# The activation function decides whether a neuron should be activated or not, by calculating weighted sum and further adding bias with it
# Max-Pooling is used to reduce the spatial dimensions of an model_output.txt volume

# the first layer (input): learning 32 filters
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(256, 256, 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# the second layer: learning 64 filters
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# the third layer: learning 128 filters
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# flatten the multi-dimensional input tensors into a single dimension
model.add(Flatten())

# add dense layer, which is a connected deeply neural network layer
model.add(Dense(64, activation='relu'))
classes = 2
model.add(Dense(classes, activation='softmax'))

# summarize the model
with open("../Data/Model/model_summary.txt", "w") as file:
    model.summary(print_fn=lambda x: file.write(x + '\n'))

# configure the learning process before training the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# define the model path
model_path = "../Data/Model/yawn_detection.h5"

# modelCheckpoint: a callback object that can perform actions at various stages of the training, and can monitor either the accuracy or the loss
checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
# checkpoint = ModelCheckpoint(model_path, monitor='val_loss',save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# define the number of epochs, which is an arbitrary cutoff, used to separate training into distinct phases, which is useful for logging and periodic evaluation
num_epochs = 50

# train the model
history = model.fit_generator(train_set, epochs=num_epochs, validation_data=validation_set, callbacks=callbacks_list)

# plot loss and accuracy
plt.figure(figsize=(20, 10))
plt.suptitle('Optimizer : Adam', fontsize=10)

plt.subplot(1, 2, 1)
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')

# save and show plots
plt.savefig("../Data/Model/loss_and_accuracy_plot.png")
plt.show()
