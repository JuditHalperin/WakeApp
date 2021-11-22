
# Drowsiness detector algorithm - based on blink, yawning, travel duration and time


# import packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from playsound import playsound
from imutils import face_utils
from threading import Thread
import numpy as np
import imutils
import smtplib
import time
import dlib
import cv2
import ssl
import os


MAIL_THRESHOLD = 5  # number of alarms before sending mail


def compute_eye_aspect_ratio(eye):
    """The function computes the eye aspect ratio"""
    A = dist.euclidean(eye[1], eye[5])  # euclidean distances between the first set of vertical eye landmarks
    B = dist.euclidean(eye[2], eye[4])  # euclidean distances between the second set of vertical eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # euclidean distance between the horizontal eye landmark
    return (A + B) / (2.0 * C)


def compute_average_eye_aspect_ratios(shape):
    """The function computes the average of the two eye aspect ratios"""
    left_eye = shape[42:48]  # indexes of left eye
    right_eye = shape[36:42]  # indexes of right eye

    left_eye_aspect_ratio = compute_eye_aspect_ratio(left_eye)  # left eye aspect ratio
    right_eye_aspect_ratio = compute_eye_aspect_ratio(right_eye)  # right eye aspect ratio

    return (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0  # average the eye aspect ratios


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


def sound_alarm():
    """The function plays an alarm sound"""
    playsound("Data/bigwarning.wav")


def send_email(username, contact_name, contact_email):
    """The function sends an email to an emergency contact, letting him know the driver is asleep"""
    sender_email = "driver.drowsiness.detection.mail@gmail.com"
    sender_password = "0586169890"
    message = open("Data/email_message.txt").read().replace("CONTACT_NAME", contact_name).replace("DRIVER_NAME", username)  # read the message and paste contact and driver names
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=ssl.create_default_context()) as server:
        server.login(sender_email, sender_password)  # log into sender account
        server.sendmail(sender_email, contact_email, message)  # send the email to emergency contact


def run(username, contact):
    """
    main function looping video stream and detecting driver drowsiness.
    contact = (name, email address) of emergency contact.
    """

    os.chdir(os.getcwd().replace("\\", "/").replace("Scripts", ""))  # set working directory

    alarm_on = False  # boolean variable indicating whether the alarm is on or off
    blinks_counter = 0  # number of blinks per minute?
    yawns_counter = 0  # number of yawns per minute?
    alarm_counter = 0  # number of time the alarm was on

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

        eye_aspect_ratios = compute_average_eye_aspect_ratios(shape)
        lips_distance = compute_lips_distance(shape)
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
                    alarm_thread = Thread(target=sound_alarm)
                    alarm_thread.deamon = True
                    alarm_thread.start()
                    alarm_on = True  # turn the alarm on
                    alarm_counter += 1  # increment the alarm counter

                    # email:
                    if alarm_counter == MAIL_THRESHOLD:  # check if the alarm sounded a specific number of times - this way the email can be sent only once
                        # start a thread to send an email to emergency contact in the background
                        mail_thread = Thread(target=send_email, args=(username, contact[0], contact[1]))
                        mail_thread.deamon = True
                        mail_thread.start()

                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw an alarm on the frame

        else:  # drowsiness score is below the threshold
            alarm_on = False  # reset the alarm
            cv2.putText(frame, "Drowsiness Score: {:.2f}".format(drowsiness_score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the drowsiness score on the frame

        cv2.imshow("Frame", frame)  # show the frame

        if (cv2.waitKey(1) & 0xFF) == ord("q"):  # if the `q` key is pressed, break from the loop
            break

    # cleanup
    vs.stream.release()
    cv2.destroyAllWindows()
