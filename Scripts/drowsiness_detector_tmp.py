
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
from playsound import playsound

import blinks_detector
import yawning_detector
import time_detector


EYE_AR_THRESH = 0.3  # eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 48  # number of frames ratio
COUNTER = 0  # consecutive frames where the eye aspect ratio is below threshold
ALARM_ON = False  # boolean variable indicating whether the alarm is on or off

SHAPE_PREDICTOR = "../Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = 'C:/Networks/work/bigwarning.wav'  # path alarm .WAV file
WEBCAM = 0  # index of webcam on system


def sound_alarm(path):
    """play an alarm sound"""
 #   play(AudioSegment.from_file(file=path, format="wav"))
    playsound(ALARM)
    print('playing sound using  playsound')


def eye_aspect_ratio(eye):
    """compute the eye aspect ratio"""
    A = dist.euclidean(eye[1], eye[5])  # euclidean distances between the first set of vertical eye landmarks
    B = dist.euclidean(eye[2], eye[4])  # euclidean distances between the second set of vertical eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # euclidean distance between the horizontal eye landmark
    return (A + B) / (2.0 * C)


def compute_drowsiness_score():
    """compute the drowsiness score"""
    blinks_score = blinks_detector.compute_blinks_score()
    yawning_score = yawning_detector.compute_yawning_score()
    time_score = time_detector.compute_time_score()
    score = 100
    return score


# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

# grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up


# loop over frames from the video stream
while True:

    frame = vs.read()  # grab the frame from the threaded video file stream
    frame = imutils.resize(frame, width=450)  # resize the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

    face = detector(gray, 0)  # detect faces in the grayscale frame - we assume there is only one face
    if not face: break  # DO SOMETHING

    shape = predictor(gray, face[0])  # determine the facial landmarks for the face region
    shape = face_utils.shape_to_np(shape)  # convert the facial landmark (x, y)-coordinates to a NumPy array

    leftEye, rightEye = shape[lStart:lEnd], shape[rStart:rEnd]  # extract the left and right eye coordinates
    leftEAR, rightEAR = eye_aspect_ratio(leftEye), eye_aspect_ratio(rightEye)  # compute the eye aspect ratios
    ear = (leftEAR + rightEAR) / 2.0  # average the eye aspect ratios

    # compute the convex hull for the left and right eye, then visualize each of the eyes
    leftEyeHull = cv2.convexHull(leftEye)
    rightEyeHull = cv2.convexHull(rightEye)
    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

    if ear < EYE_AR_THRESH:  # check if the eye aspect ratio is below the blink threshold
        COUNTER += 1  # increment the blink frame counter
        if COUNTER >= EYE_AR_CONSEC_FRAMES:  # check if the eyes were closed for a sufficient number
            if not ALARM_ON:  # check if the alarm is not on
                ALARM_ON = True  # turn the alarm on
                # start a thread to have the alarm sound played in the background
                t = Thread(target=sound_alarm, args=(ALARM,))
                t.deamon = True
                t.start()
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw an alarm on the frame

    else:  # eye aspect ratio is not below the blink threshold
        COUNTER = 0  # reset the counter
        ALARM_ON = False  # reset the alarm
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the eye aspect ratio on the frame

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# cleanup
cv2.destroyAllWindows()
vs.stop()
