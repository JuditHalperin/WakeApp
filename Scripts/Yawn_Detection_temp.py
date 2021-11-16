

import cv2  # imports OpenCV library and associated functions and methods
import numpy as np  # imports numpy as "np" library and associated functions and methods
import dlib  # imports dlib library and associated functions
import os


WORKING_DIRECTORY = os.getcwd().replace("\\", "/").replace("Scripts", "")  # path to working directory
SHAPE_PREDICTOR = WORKING_DIRECTORY + "Data/shape_predictor_68_face_landmarks.dat"  # path to facial landmark predictor
ALARM = WORKING_DIRECTORY + "Data/bigwarning.wav"  # path alarm .WAV file
WEBCAM = 0  # index of webcam on system


predictor = dlib.shape_predictor(SHAPE_PREDICTOR)  # creates a variable that stores the method of face decection from dlib library
detector = dlib.get_frontal_face_detector()  # creates a variable that stores another method that dlib provides for detecting faces


def get_landmarks(im):  # creating a function that gets the landmarks on the face to make the code easier (detector returns cordinates of major facial features)
    rects = detector(im, 1)  # creates a variable that returns the number of faces in the screen

    if len(rects) > 1:  # To check if there are more than 1 faces, if yes, return an empty matrix
        print("Toomanyfaces")
        return np.matrix([0])

    if len(rects) == 0:  # To check if there are 0 faces, if yes, return an empty matrix
        print("Toofewfaces")
        return np.matrix([0])

    return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])  # if there is exactly 1 face, the predictor method is used to append cordinates of facial features in a numpy matrix


def upper_lip(landmarks):  # To find out the mean cordinates of the upper lip position
    top_lip = []  # Creates a new list

    for i in range(50, 53):  # Creating a range from "50" to "53" because they represent the upper lip in dlib face predictor
        top_lip.append(landmarks[i])  # Appending the same in the top lip list created above

    for j in range(61, 64):  # Creating a range from "61" to "64" because they represent the upper lip in dlib face predictor
        top_lip.append(landmarks[j])

    top_lip_point = (np.squeeze(np.asarray(top_lip)))  # This function removes any cordinate that is not in x,y format
    top_mean = np.mean(top_lip_point, axis=0)  # Finds the mean of the upper lip cordinates so that it can be subtracted from the mean cordinates of lower lip

    return int(top_mean[1])  # Return int value of the mean of the cordinates of upper lip


def low_lip(landmarks):  # To find out the mean cordinates of the lower lip position
    lower_lip = []  # Creates a new list

    for i in range(65, 68):  # Creating a range from "65" to "68" because they represent the lower lip in dlib face predictor
        lower_lip.append(landmarks[i])

    for j in range(56, 59):  # Creating a range from "56" to "59" because they represent the lower lip in dlib face predictor
        lower_lip.append(landmarks[j])

    lower_lip_point = (np.squeeze(np.asarray(lower_lip)))  # This function removes any cordinate that is not in x,y format
    lower_mean = np.mean(lower_lip_point, axis=0)  # Finds the mean of the lower lip cordinates so that it can be subtracted from the mean cordinates of lower lip

    return int(lower_mean[1])  # Return int value of the mean of the cordinates of lower lip


def decision(image):  # Creating a function that returns the distance between the upper and the lower lip
    landmarks = get_landmarks(image)  # Creates a varible that stores the cordinates returned from the function (get_landmarks) created above

    if (landmarks.all() == [0]):  # If no landmarks are created, return nothing
        return -10

    top_lip = upper_lip(landmarks)  # Creates a variable that stores the mean of the cordinates returned by the function "upper_lip" created above
    lower_lip = low_lip(landmarks)  # Creates a variable that stores the mean of the cordinates returned by the function "lower_lip" created above
    distance = abs(top_lip - lower_lip)  # Subtracts the mean values of the two lips to find distance

    return distance


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Creates a varible that stores a method of OpenCV
yawns = 0  # Creates a counter for yawns
mouth_open = False  # This variable will be used below to help know if the mouth has been closed after yawning

while (True):  # While loop helps taking multiple frames from detection and keep the program on until told to shut
    ret, frame = cap.read()  # ret stores the boolean value returned from read method. If yes, then the camera is on and face/faces are being detected
    distance = decision(frame)  # Creates a variable that stores the distance value between two lips returned by the function created above

    if (ret == True):  # If ret is True, the program moves forward
        landmarks = get_landmarks(frame)
        if (landmarks.all() != [0]):  # This checks if the landmarks created are not null
            l1 = []  # New list is created to store boundary cordinates of the entire lips

            for k in range(48, 60):  # 48-60 in DLIB that defines the lips of a face
                l1.append(landmarks[k])  # Appends the coridnates of the lips using landmakrs function created above

            l2 = np.asarray(l1)
            lips = cv2.convexHull(l2)  # convexHull is a mathematic form of tracing a curve by cordinates
            cv2.drawContours(frame, [lips], -1, (0, 255, 0), 1)  # Draws countours on the lips for asthetic purposes

        if (distance > 35):  # If distance is more than 35, we change the boolean value of mouth_open to True, it acts as a flag
            mouth_open = True

        if (distance < 20) and mouth_open:  # Now condition is if the mouth is now closed (based on distance betweent the two lips) and that the mouth was previously open
            yawns = yawns + 1  # Increment the yawn count
            mouth_open = False  # Flag the mouth_open to false again so it can be used again

        cv2.putText(frame, "Yawn Count: " + str(yawns), (50, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0, 255, 255))  # This shows a text on given cordinates on the image itelf
        cv2.imshow("Subject Yawn Count", frame)  # This streams the video being captured on the screen

        if cv2.waitKey(1) == 27:  # Waits for ESCAPE key to be pressed to break out of the code
            break
    else:
        continue

cap.release()  # Once out of the while loop, this is automatically executed and it stops the video stream
cv2.destroyAllWindows()  # Shut the streaming video
