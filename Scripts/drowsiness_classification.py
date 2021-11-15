
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

DROWSINESS_SCORE_THRESHOLD = 12345  # CHOOSE THRESHOLD  # drowsiness score threshold
ALARM_THRESHOLD = 48  # number of bad scored frames before beeping the alarm
MAIL_THRESHOLD = 5  # number of alarms before sending mail


def compute_drowsiness_score(frame, shape):
    """compute the drowsiness score and mark the eyes and the lips on the frame"""
    blinks_score, frame = blinks_detector.compute_blinks_score(frame, shape)  # compute blinks score
    yawning_score, frame = yawning_detector.compute_yawning_score(frame, shape)  # compute yawning score
    time_score = time_detector.compute_time_score()  # compute time score
    score = 1234  # CALCULATE THE SCORE #
    return score, frame


def sound_alarm(path):
    """play an alarm sound"""
    playsound(path)
    print('playing sound using  playsound')


def send_mail(name, address):
    """send a mail to emergency contact letting him know the driver is asleep"""
    # SEND MAIL #


def run(name, address, webcam=0):
    """main function looping video stream. webcam = index of webcam on system"""

    frame_counter = 0  # count how many consecutive frames where the drowsiness score is above threshold
    alarm_counter = 0  # count how many times the alarm was on
    alarm_on = False  # boolean variable indicating whether the alarm is on or off

    detector = dlib.get_frontal_face_detector()  # initialize dlib's face detector (HOG-based)
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR)  # create facial landmark predictor
    vs = VideoStream(src=webcam).start()  # start the video stream thread
    time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up

    while True:  # loop over frames from the video stream

        frame = vs.read()  # grab the frame from the threaded video file stream
        frame = imutils.resize(frame, width=450)  # resize the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

        face = detector(gray, 0)  # detect faces in the grayscale frame - assuming there is only one face
        if not face: continue  # DO SOMETHING #
        shape = predictor(gray, face[0])  # determine the facial landmarks for the face region
        shape = face_utils.shape_to_np(shape)  # convert the facial landmark (x, y)-coordinates to a NumPy array

        drowsiness_score, frame = compute_drowsiness_score(frame, shape)  # compute the drowsiness score based on blink, yawning, duration and time

        if drowsiness_score > DROWSINESS_SCORE_THRESHOLD:  # check if the drowsiness score is above the threshold
            frame_counter += 1  # increment the frame counter
            if frame_counter >= ALARM_THRESHOLD:  # check if the drowsiness score is high for a sufficient number
                if not alarm_on:  # check if the alarm is not on
                    # start a thread to have the alarm sound played in the background
                    alarm_thread = Thread(target=sound_alarm, args=(ALARM,))
                    alarm_thread.deamon = True
                    alarm_thread.start()
                    alarm_on = True  # turn the alarm on
                    alarm_counter += 1  # increment the alarm counter
                    if alarm_counter == MAIL_THRESHOLD:  # check if the alarm beeped a sufficient number
                        # start a thread to send a mail in the background
                        mail_thread = Thread(target=send_mail, args=(name, address))
                        mail_thread.deamon = True
                        mail_thread.start()
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw an alarm on the frame

        else:  # drowsiness score is below the threshold
            frame_counter = 0  # reset the drowsiness counter
            alarm_on = False  # reset the alarm
            cv2.putText(frame, "Drowsiness Score: {:.2f}".format(drowsiness_score), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the drowsiness score on the frame

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, cleanup and break from the loop
        if key == ord("q"):
 #           cv2.destroyAllWindows()
  #          vs.stop()
            break
        else:
            continue
    # cleanup
    vs.stream.release()
    cv2.destroyAllWindows()






