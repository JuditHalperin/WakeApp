
# Blinks detector algorithm


# import packages
from scipy.spatial import distance as dist
from imutils import face_utils
import cv2


# grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def eye_aspect_ratio(eye):
    """compute the eye aspect ratio"""
    A = dist.euclidean(eye[1], eye[5])  # euclidean distances between the first set of vertical eye landmarks
    B = dist.euclidean(eye[2], eye[4])  # euclidean distances between the second set of vertical eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # euclidean distance between the horizontal eye landmark
    return (A + B) / (2.0 * C)


def visualize_eyes(frame, leftEye, rightEye):
    """compute the convex hull for the left and right eye, then visualize each of the eyes on the frame"""
    cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
    return frame


def compute_blinks_score(frame, shape):
    """compute the blinks score"""
    leftEye, rightEye = shape[lStart:lEnd], shape[rStart:rEnd]  # extract the left and right eye coordinates
    leftEAR, rightEAR = eye_aspect_ratio(leftEye), eye_aspect_ratio(rightEye)  # compute the eye aspect ratios
    score = (leftEAR + rightEAR) / 2.0  # average the eye aspect ratios
    frame = visualize_eyes(frame, leftEye, rightEye)  # visualize the eyes on the frame
    return score, frame  # return the blinks score and the frame
