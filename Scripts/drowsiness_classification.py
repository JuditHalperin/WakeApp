
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
from pydub import AudioSegment
from pydub.playback import play

import blinks_detector
import yawning_detector
import time_detector


SHAPE_PREDICTOR = "Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = "Data/bigwarning.wav"  # path alarm .WAV file
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
    play(AudioSegment.from_file(file=path, format="wav"))


