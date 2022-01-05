
# Drowsiness detector algorithm - based on blinks, yawns, travel duration and time


# import packages
from imutils.video import VideoStream
from keras.models import load_model
from imutils import face_utils
from collections import deque
from threading import Thread
import datetime
import imutils
import time
import dlib
import cv2


# import scripts
import blink_score
import yawn_score
import thresholds
import drowsiness_alert


FRAMES_PER_SECOND = 3  # number of frame per a second the drowsiness classification is based on
MINUTES_PER_WINDOW = 5  # approximate number of minutes the frame window contains
WINDOW_SIZE = 60 * MINUTES_PER_WINDOW * FRAMES_PER_SECOND  # frame window size (60 seconds * minutes * frames)

EYE_ASPECT_RATIO_THRESHOLD = 0.3  # eye aspect ratio threshold
EMAIL_THRESHOLD = 3  # number of alarms before sending email


# username, contact_name, contact_email


def main():
    """The main function loops the video stream to detect driver drowsiness"""

    start_drive_time = last_frame_time = datetime.datetime.now()  # beginning time; last time a frame was analyzed

    alarm_on = False  # boolean variable indicating whether the alarm is on or off
    alarm_counter = 0  # number of times the alarm was on

    yawn_queue = deque()  # blink / yawn window queue
    blink_counter = yawn_counter = 0  # number of blinks / yawns

    detector = dlib.get_frontal_face_detector()  # initialize dlib's face detector (HOG-based)
    predictor = dlib.shape_predictor("../Data/shape_predictor_68_face_landmarks.dat")  # create facial landmark predictor using the shape predictor

    model = load_model("../Data/Model/yawn_detection.h5")  # load the yawning classification model

    vs = VideoStream(src=0).start()  # start the video stream thread, 0 indicates index of webcam on system
    time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up

    while True:

        frame = vs.read()  # grab the frame from the threaded video file stream
        frame = imutils.resize(frame, width=450)  # resize the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

        face = detector(gray_frame, 0)  # detect faces in the grayscale frame - assuming there is only one face
        if not face:
            # DO SOMETHING IN GUI #
            time.sleep(1.0)  # pause for a second before continue
            continue

        shape = predictor(gray_frame, face[0])  # determine the facial landmarks for the face region
        shape = face_utils.shape_to_np(shape)  # convert the facial landmark (x, y)-coordinates to a NumPy array

        if datetime.datetime.now() - last_frame_time >= datetime.timedelta(seconds=1/FRAMES_PER_SECOND):  # if a sufficient time passed since the previous frame was analysed

            # to detect drowsiness, check for a blink and a yawn in the frame:

            last_frame_time = datetime.datetime.now()  # update the last time a frame was analyzed

            # blink - by computing the eye aspect ratios
            if blink_score.compute_average_eye_aspect_ratios(shape) < EYE_ASPECT_RATIO_THRESHOLD:
                blink_counter += 1

            else:
                blink_counter = 0

            """
            if len(blink_queue) > WINDOW_SIZE:  # if the queue is full
                blink_counter -= 1 if blink_queue.popleft() else 0  # pop the first frame (oldest) out, and update the counter
            blink_queue.append(blink)  # insert the new frame to the end of the queue
            blink_counter += 1 if blink else 0  # update the counter
            """

            # yawn - by using the yawn classification model
            prediction = yawn_score.predict_yawn(gray_frame, model)  # [not yawn, yawn]
            yawn = prediction[0] <= prediction[1] and True or False
            if len(yawn_queue) > WINDOW_SIZE:  # if the queue is full
                yawn_counter -= 1 if yawn_queue.popleft() else 0  # pop the first frame (oldest) out, and update the counter
            yawn_queue.append(yawn)  # insert the new frame to the end of the queue
            yawn_counter += 1 if yawn else 0  # update the counter

            # compute the current time and the drive duration to determine the thresholds (late and long time = more sensitive thresholds)
            current_time = datetime.datetime.now()
            travel_duration = current_time - start_drive_time

            # compare the counters to thresholds to see if the driver is classified as drowsy - based on blinks OR yawns
            if blink_counter >= thresholds.blink_count_threshold(current_time, travel_duration) or \
                    yawn_counter >= thresholds.yawn_count_threshold(current_time, travel_duration):

                # reset queues and counters to
                yawn_queue = deque()
                blink_counter = yawn_counter = 0

                # alarm
                if not alarm_on:  # check if the alarm is not on
                    # start a thread to have the alarm sound played in the background
                    alarm_thread = Thread(target=drowsiness_alert.sound_alarm)
                    alarm_thread.deamon = True
                    alarm_thread.start()
                    alarm_on = True  # turn the alarm on
                    alarm_counter += 1  # increment the alarm counter

                    """
                    # email
                    if alarm_counter == EMAIL_THRESHOLD:  # check if the alarm sounded a specific number of times - this way the email can be sent only once
                        # start a thread to send an email to emergency contact in the background
                        email_thread = Thread(target=drowsiness_alert.send_email, args=(username, contact_name, contact_email))
                        email_thread.deamon = True
                        email_thread.start()
                    """

                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the alarm on the frame

            else:  # not classified as drowsy
                alarm_on = False  # reset the alarm

        cv2.drawContours(frame, [cv2.convexHull(shape[42:48])], -1, (0, 255, 0), 1)  # compute convex hull and visualize left eye
        cv2.drawContours(frame, [cv2.convexHull(shape[36:42])], -1, (0, 255, 0), 1)  # compute convex hull and visualize right eye
        cv2.drawContours(frame, [shape[48:60]], -1, (0, 255, 0), 1)  # visualize lips

        cv2.imshow("Frame", frame)  # show the frame

        if (cv2.waitKey(1) & 0xFF) == ord("q"):  # if the `q` key is pressed, break from the loop
            break

    # cleanup
    vs.stream.release()
    cv2.destroyAllWindows()


main()
