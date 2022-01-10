
# Blink score functions


# import packages
from scipy.spatial import distance as dist


def compute_eye_aspect_ratio(eye):
    """The function computes the eye aspect ratio"""
    A = dist.euclidean(eye[1], eye[5])  # euclidean distances between the first set of vertical eye landmarks
    B = dist.euclidean(eye[2], eye[4])  # euclidean distances between the second set of vertical eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # euclidean distance between the horizontal eye landmark
    return (A + B) / (2.0 * C)  # eye aspect ratio


def compute_average_eye_aspect_ratios(shape):
    """The function computes the average of the two eye aspect ratios"""
    left_eye = shape[42:48]  # indexes of left eye
    right_eye = shape[36:42]  # indexes of right eye
    left_eye_aspect_ratio = compute_eye_aspect_ratio(left_eye)  # left eye aspect ratio
    right_eye_aspect_ratio = compute_eye_aspect_ratio(right_eye)  # right eye aspect ratio
    return (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0  # average the eye aspect ratios
