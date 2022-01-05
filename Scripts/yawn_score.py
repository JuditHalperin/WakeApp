
# Yawn score functions

# (Note: the first function can be used to detect yawns relaying on the distance between the lips.
# Our algorithm uses a neural network model for the yawning classification, so this function is not used)


# import packages
from keras.preprocessing import image
import numpy as np
import cv2


def compute_lips_distance(shape):
    """The function receives indexes of the face, and returns the distance between the top lip and the low lip"""
    start_top_lip = shape[50:53]  # start indexes of top lip
    end_top_lip = shape[61:64]  # end indexes of top lip
    start_low_lip = shape[56:59]  # start indexes of low lip
    end_low_lip = shape[65:68]  # end indexes of low lip
    top_lip = np.concatenate((start_top_lip, end_top_lip))  # top lip coordinates
    low_lip = np.concatenate((start_low_lip, end_low_lip))  # low lip coordinates
    top_mean = np.mean(top_lip, axis=0)  # top lip mean
    low_mean = np.mean(low_lip, axis=0)  # low lip mean
    return abs(top_mean[1] - low_mean[1])  # distance between the top and the low lips


def process_frame(gray_frame):
    """The function processes the frame before using the model"""
    frame = cv2.resize(gray_frame, (256, 256))  # resize the frame
    frame = image.img_to_array(frame)  # convert frame to array (height, width, channels)
    frame = np.expand_dims(frame, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    frame /= 255.  # set values [0, 1]
    return frame


def predict_yawn(gray_frame, model):
    """The function checks for yawn in the grayscale frame, and returns the predictions of [not yawn, yawn]"""
    return model.predict(process_frame(gray_frame))[0]
