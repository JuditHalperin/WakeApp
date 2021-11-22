from imutils.video import VideoStream
from playsound import playsound
from imutils import face_utils
from threading import Thread
import numpy as np
import imutils
import time
import dlib
import cv2
import os


def sound_alarm(path):
    """play an alarm sound"""
    # play(AudioSegment.from_file(file=path, format="wav"))
    playsound(path)
    print('playing sound using playsound')


def lip_distance(shape):
    '''The function receives indexes of the face and returns the distance between the top lip and the low lip'''
    start_top_lip = shape[50:53]  # start indexes of top lip
    end_top_lip = shape[61:64]  # end indexes of top lip
    start_low_lip = shape[56:59]  # start indexes of low lip
    end_low_lip = shape[65:68]  # end indexes of low lip
    top_lip = np.concatenate((start_top_lip, end_top_lip))  # Finding top lip coordinates
    low_lip = np.concatenate((start_low_lip, end_low_lip))  # Finding low lip coordinates

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance


YAWN_THRESH = 20  # Depends also on the distance of a person from the computer
ALARM_ON = False  # boolean variable indicating whether the alarm is on or off

WORKING_DIRECTORY = os.getcwd().replace("\\", "/").replace("Scripts", "")  # path to working directory
SHAPE_PREDICTOR = WORKING_DIRECTORY + "Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = WORKING_DIRECTORY + "Data/bigwarning.wav"  # path alarm .WAV file
WEBCAM = 0  # index of webcam on system


print("-> Loading the predictor and detector...")
detector = dlib.get_frontal_face_detector()
# detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Faster but less accurate
predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

print("-> Starting Video Stream")
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rect = detector(gray, 0)
    # rects = detector.detectMultiScale(gray, scaleFactor=1.1,  minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    if not rect:
        print('could not find a face')  # message for debugging
        time.sleep(1.0)  # pause for a second before continue
        continue
    shape = predictor(gray, rect[0])
    shape = face_utils.shape_to_np(shape)
    distance = lip_distance(shape)
    lip = shape[48:60]
    cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

    if (distance > YAWN_THRESH):
        cv2.putText(frame, "Yawn Alert", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if not ALARM_ON:  # check if the alarm is not on
            ALARM_ON = True  # turn the alarm on
            # start a thread to have the alarm sound played in the background
            t = Thread(target=sound_alarm, args=(ALARM,))
            t.deamon = True
            t.start()
    else:
        ALARM_ON = False  # reset the alarm

    cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
