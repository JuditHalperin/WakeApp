
# Yawn score functions


# import packages
import numpy as np


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
