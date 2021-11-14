
# Drowsiness detector algorithm


# import packages
import dlib
import cv2
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import time
from playsound import playsound
import os

# import scripts
import blinks_detector
import yawning_detector
import time_detector


WORKING_DIRECTORY = os.getcwd().replace("\\", "/").replace("Scripts", "")  # path to working directory
SHAPE_PREDICTOR = WORKING_DIRECTORY + "Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = WORKING_DIRECTORY + "Data/bigwarning.wav"  # path alarm .WAV file
WEBCAM = 0  # index of webcam on system

DROWSINESS_SCORE_THRESHOLD = 12345  # CHOOSE THRESHOLD  # drowsiness score threshold
FRAMES_THRESHOLD = 48  # number of frames threshold
COUNTER = 0  # consecutive frames where the drowsiness score is above threshold
ALARM_ON = False  # boolean variable indicating whether the alarm is on or off


def compute_drowsiness_score(frame, shape):
    """compute the drowsiness score"""
    blinks_score, frame = blinks_detector.compute_blinks_score(frame, shape)
    yawning_score, frame = yawning_detector.compute_yawning_score(frame, shape)
    time_score = time_detector.compute_time_score()
    score = 12345  # CALCULATE THE SCORE #
    return score, frame


def sound_alarm(path):
    """play an alarm sound"""
    playsound(ALARM)


def send_mail(name, address):
    """send a mail to emergency contact letting him know the driver is asleep"""
    # SEND MAIL #


# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

# start the video stream thread
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up


# loop over frames from the video stream
while True:

    frame = vs.read()  # grab the frame from the threaded video file stream
    frame = imutils.resize(frame, width=450)  # resize the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

    face = detector(gray, 0)  # detect faces in the grayscale frame - assuming there is only one face
    if not face: continue  # DO SOMETHING #
    shape = predictor(gray, face[0])  # determine the facial landmarks for the face region
    shape = face_utils.shape_to_np(shape)  # convert the facial landmark (x, y)-coordinates to a NumPy array

    # compute the drowsiness score based on blink, yawning, duration and time
    drowsiness_score, frame = compute_drowsiness_score(frame, shape)

    if drowsiness_score > DROWSINESS_SCORE_THRESHOLD:  # check if the drowsiness score is above the threshold
        COUNTER += 1  # increment the frame counter
        if COUNTER >= FRAMES_THRESHOLD:  # check if the drowsiness score is high for a sufficient number
            if not ALARM_ON:  # check if the alarm is not on
                ALARM_ON = True  # turn the alarm on
                # start a thread to have the alarm sound played in the background
                t = Thread(target=sound_alarm, args=(ALARM,))
                t.deamon = True
                t.start()
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw an alarm on the frame

    else:  # drowsiness score is below the threshold
        COUNTER = 0  # reset the counter
        ALARM_ON = False  # reset the alarm
        cv2.putText(frame, "Drowsiness Score: {:.2f}".format(drowsiness_score), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the drowsiness score on the frame

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, cleanup and break from the loop
    if key == ord("q"):
        cv2.destroyAllWindows()
        vs.stop()
        break
