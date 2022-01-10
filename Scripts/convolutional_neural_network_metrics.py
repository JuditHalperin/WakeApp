
# Neural network model metrics for the yawn classification


# import packages
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import os


def load_image(img_path):
    """This function loads an image"""
    img = image.load_img(img_path, target_size=(256, 256), color_mode='grayscale')
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.
    return img_tensor


# load model
model = load_model("../Data/Model/yawn_detection.h5")

# initialize metrics
tn = fp = fn = tp = 0

# loop over 'yawn' class
for img in os.listdir("../Data/Dataset/test/yawn"):
    predictions = model.predict(load_image("../Data/Dataset/test/yawn/" + img))
    if predictions[0][0] < predictions[0][1]:  # predicted 'yawn'
        tp += 1
    else:  # predicted 'not yawn'
        fn += 1

# loop over 'not yawn' class
for img in os.listdir("../Data/Dataset/test/no_yawn"):
    predictions = model.predict(load_image("../Data/Dataset/test/no_yawn/" + img))
    if predictions[0][0] > predictions[0][1]:  # predicted 'not yawn'
        tn += 1
    else:  # predicted 'yawn'
        fp += 1

# calculate precision, recall and f1_score
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * precision * recall / (precision + recall)

# save results
open("../Data/Model/confusion_matrix.txt", "w").write("TP: " + str(tp) + "\nTN: " + str(tn) + "\nFP: " + str(fp) + "\nFN: " + str(fn) + "\n\nPrecision: " + str(precision) + "\nRecall: " + str(recall) + "\nF1 score: " + str(f1_score))
