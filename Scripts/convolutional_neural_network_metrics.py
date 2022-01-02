
# This script calculates the neural network model metrics


# import packages
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from keras.models import load_model
import numpy

# get the actual classes
test_data_generator = ImageDataGenerator(rescale=1./255)
test_set = test_data_generator.flow_from_directory("../Data/Dataset/test", target_size=(256, 256), batch_size=128, color_mode='grayscale', class_mode='categorical')
actual_labels = []
actual_labels.extend(test_set.labels)

# get the predicted classes
model = load_model("../Data/Model/yawn_detection.h5")
predictions = model.predict(test_set)
predicted_classes = numpy.argmax(predictions, axis=1)

# save the confusion matrix
tn, fp, fn, tp = confusion_matrix(y_true=actual_labels, y_pred=predicted_classes).ravel()
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * precision * recall / (precision + recall)
open("../Data/Model/confusion_matrix.txt", "w").write("TP: " + str(tp) + "\nTN: " + str(tn) + "\nFP: " + str(fp) + "\nFN: " + str(fn)
                                                          + "\n\nPrecision: " + str(precision) + "\nRecall: " + str(recall) + "\nF1 score: " + str(f1_score))
