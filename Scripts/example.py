
# Example of a simple algorithm using OpenCV, Dlib and Imutils libraries.


# import packages
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import cv2


detector = dlib.get_frontal_face_detector()  # initialize the face detector
predictor = dlib.shape_predictor("../Data/shape_predictor_68_face_landmarks.dat")  # load the trained shape predictor

vs = VideoStream(src=0).start()  # initialize the video stream, 0 is the webcam index on the system

while True:  # loop over video frames

    frame = vs.read()  # grab the frame from the video stream
    frame = imutils.resize(frame, width=400)  # resize the frame to have a maximum width of 400 pixels
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert the frame to grayscale

    face = detector(gray_frame, 0)[0]  # detect a single face in the grayscale frame

    (x, y, w, h) = face_utils.rect_to_bb(face)  # convert the Dlib rectangle into an OpenCV bounding box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw a bounding box surrounding the face

    shape = predictor(gray_frame, face)  # predict the location of the face landmark coordinates
    shape = face_utils.shape_to_np(shape)  # convert the prediction to an easily parsable NumPy array

    for (sX, sY) in shape:  # loop over the coordinates
        cv2.circle(frame, (sX, sY), 1, (0, 0, 255), -1)  # draw the coordinates on the image

    cv2.imshow("Frame", frame)  # show the frame

    # break when 'q' key was pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# cleanup
vs.stream.release()
cv2.destroyAllWindows()
