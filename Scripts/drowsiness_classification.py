
# Drowsiness detector algorithm


# import packages
import dlib
import cv2
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
from scipy.spatial import distance as dist
import time
from playsound import playsound
import os

import blinks_detector
import yawning_detector
import time_detector


WORKING_DIRECTORY = os.getcwd().replace("\\", "/").replace("Scripts", "")  # path to working directory
SHAPE_PREDICTOR = WORKING_DIRECTORY + "Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = WORKING_DIRECTORY + "Data/bigwarning.wav"  # path alarm .WAV file
WEBCAM = 0  # index of webcam on system



def compute_drowsiness_score():
    """compute the drowsiness score"""
    blinks_score = blinks_detector.compute_blinks_score()
    yawning_score = yawning_detector.compute_yawning_score()
    time_score = time_detector.compute_time_score()
    score = 100
    return score


def sound_alarm(path):
    """play an alarm sound"""
    playsound(ALARM)

# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR)


# start the video stream thread
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up
