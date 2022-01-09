
# Drowsiness detector algorithm - based on blinks, yawns, travel duration and time


# import packages
from __future__ import print_function
from imutils.video import VideoStream
from keras.models import load_model
from imutils import face_utils
from collections import deque
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import threading
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

EYE_ASPECT_RATIO_THRESHOLD = 0.2  # eye aspect ratio threshold
EMAIL_THRESHOLD = 3  # number of alarms before sending email


class DrowsinessDetector:

	def __init__(self, vs, username, contact_name, contact_email):

		self.vs = vs
		self.username = username
		self.contact_name = contact_name
		self.contact_email = contact_email

		self.thread = None
		self.stop_event = None
		self.root = tk.Tk()
		self.panel = None

		# start a thread that constantly pools the video sensor for the most recently read frame
		self.stop_event = threading.Event()
		self.thread = threading.Thread(target=self.video_loop, args=())
		self.thread.start()

		# stop button
		btn = tk.Button(self.root, text="Stop", command=self.on_close)
		btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

		# set a callback to handle when the window is closed
		self.root.wm_title("Driver Drowsiness Detection")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

		self.root.resizable(False, False)

	def video_loop(self):

		start_drive_time = last_frame_time = datetime.datetime.now()  # beginning time; last time a frame was analyzed

		alarm_on = False  # boolean variable indicating whether the alarm is on or off
		alarm_counter = 0  # number of times the alarm was on

		yawn_queue = deque()  # yawn window queue
		blink_counter = yawn_counter = 0  # number of blinks / yawns

		detector = dlib.get_frontal_face_detector()  # initialize the face detector
		predictor = dlib.shape_predictor("../Data/shape_predictor_68_face_landmarks.dat")  # create facial landmark predictor using the shape predictor

		model = load_model("../Data/Model/yawn_detection.h5")  # load the yawning classification model

		while not self.stop_event.is_set():

			frame = self.vs.read()  # grab the frame from the threaded video file stream
			frame = imutils.resize(frame, width=450)  # resize the frame
			gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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

					print(blink_counter, yawn_counter)

					# reset queues and counters to
					yawn_queue = deque()
					blink_counter = 0
					yawn_counter = 0

					# alarm
					if not alarm_on:  # check if the alarm is not on
						# start a thread to have the alarm sound played in the background
						alarm_thread = threading.Thread(target=drowsiness_alert.sound_alarm)
						alarm_thread.deamon = True
						alarm_thread.start()
						alarm_on = True  # turn the alarm on
						alarm_counter += 1  # increment the alarm counter

						"""# email
						if alarm_counter == EMAIL_THRESHOLD:  # check if the alarm sounded a specific number of times - this way the email can be sent only once
							# start a thread to send an email to emergency contact in the background
							email_thread = threading.Thread(target=drowsiness_alert.send_email, args=(self.username, self.contact_name, self.contact_email))
							email_thread.deamon = True
							email_thread.start()"""

					#cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # draw the alarm on the frame

				else:  # not classified as drowsy
					alarm_on = False  # reset the alarm

			cv2.drawContours(frame, [cv2.convexHull(shape[42:48])], -1, (0, 255, 0), 1)  # compute convex hull and visualize left eye
			cv2.drawContours(frame, [cv2.convexHull(shape[36:42])], -1, (0, 255, 0), 1)  # compute convex hull and visualize right eye
			cv2.drawContours(frame, [shape[48:60]], -1, (0, 255, 0), 1)  # visualize lips

			frame = Image.fromarray(frame, mode="RGB")
			frame = ImageTk.PhotoImage(frame)

			if self.panel is None:  # initialize the panel
				self.panel = tk.Label(image=frame)
				self.panel.image = frame
				self.panel.pack(side="left", padx=10, pady=10)

			else:  # update the panel
				self.panel.configure(image=frame)
				self.panel.image = frame

	def on_close(self):
		# set the stop event, cleanup the camera, and allow the rest of the quit process to continue
		print("on_close")
		self.stop_event.set()
		self.vs.stream.release()
		#self.vs.stop()
		self.root.destroy()
		self.thread = None


def start_driving(username, contact_name, contact_email):
	"""Start the video stream and the drowsiness detection loop"""
	vs = VideoStream(src=0).start()  # start the video stream thread, 0 indicates index of webcam on system
	time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up

	# start the app
	dd = DrowsinessDetector(vs, username, contact_name, contact_email)
	dd.root.mainloop()


start_driving("a", "a", "a")
