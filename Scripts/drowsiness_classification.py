
# Drowsiness detector algorithm - based on blink, yawning, travel duration and time


# import packages
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import imutils
import time
import dlib
import cv2
import os


# import scripts
import blink_score
import yawn_score
import time_score
import drowsiness_alert


# thresholds
EMAIL_THRESHOLD = 5  # number of alarms before sending email
# MORE THRESHOLDS #


def run(username, contact):
    """
    The main function loops the video stream to detect driver drowsiness.
    contact = (name, email address) of emergency contact.
    """

    os.chdir(os.getcwd().replace("\\", "/").replace("Scripts", ""))  # set working directory

    alarm_on = False  # boolean variable indicating whether the alarm is on or off
    blinks_counter = 0  # number of blinks per minute?
    yawns_counter = 0  # number of yawns per minute?
    alarm_counter = 0  # number of times the alarm was on

    detector = dlib.get_frontal_face_detector()  # initialize dlib's face detector (HOG-based)
    predictor = dlib.shape_predictor("Data/shape_predictor_68_face_landmarks.dat")  # create facial landmark predictor using the shape predictor

    vs = VideoStream(src=0).start()  # start the video stream thread, 0 indicates index of webcam on system
    time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up

    while True:

        frame = vs.read()  # grab the frame from the threaded video file stream
        frame = imutils.resize(frame, width=450)  # resize the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

        face = detector(gray, 0)  # detect faces in the grayscale frame - assuming there is only one face
        if not face:
            # DO SOMETHING IN GUI #
            time.sleep(1.0)  # pause for a second before continue
            continue

        shape = predictor(gray, face[0])  # determine the facial landmarks for the face region
        shape = face_utils.shape_to_np(shape)  # convert the facial landmark (x, y)-coordinates to a NumPy array

        eye_aspect_ratios = blink_score.compute_average_eye_aspect_ratios(shape)
        lips_distance = yawn_score.compute_lips_distance(shape)
        # travel_duration = ?
        # time = ?

        cv2.drawContours(frame, [cv2.convexHull(shape[42:48])], -1, (0, 255, 0), 1)  # compute convex hull and visualize left eye
        cv2.drawContours(frame, [cv2.convexHull(shape[36:42])], -1, (0, 255, 0), 1)  # compute convex hull and visualize right eye
        cv2.drawContours(frame, [shape[48:60]], -1, (0, 255, 0), 1)  # visualize lips

        if True:  # CONDITION
            # UPDATE COUNTERS
            if True:  # CHECK COUNTERS

                # alarm:
                if not alarm_on:  # check if the alarm is not on
                    # start a thread to have the alarm sound played in the background
                    alarm_thread = Thread(target=drowsiness_alert.sound_alarm)
                    alarm_thread.deamon = True
                    alarm_thread.start()
                    alarm_on = True  # turn the alarm on
                    alarm_counter += 1  # increment the alarm counter

                    # email:
                    if alarm_counter == EMAIL_THRESHOLD:  # check if the alarm sounded a specific number of times - this way the email can be sent only once
                        # start a thread to send an email to emergency contact in the background
                        email_thread = Thread(target=drowsiness_alert.send_email, args=(username, contact[0], contact[1]))
                        email_thread.deamon = True
                        email_thread.start()

                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the alarm on the frame

        else:
            alarm_on = False  # reset the alarm
            cv2.putText(frame, "Drowsiness Score: {:.2f}".format(drowsiness_score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the drowsiness score on the frame

        cv2.imshow("Frame", frame)  # show the frame

        if (cv2.waitKey(1) & 0xFF) == ord("q"):  # if the `q` key is pressed, break from the loop
            break

    # cleanup
    vs.stream.release()
    cv2.destroyAllWindows()
