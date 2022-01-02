

# import packages
import time
import cv2
from imutils.video import VideoStream
from keras.models import load_model
import numpy as np
from keras.preprocessing import image


# load model
model = load_model("../Data/Model/yawn_detection.h5")

# get an image from the webcam
WEBCAM = 0  # index of webcam on system
vs = VideoStream(src=WEBCAM).start()
time.sleep(1.0)  # pause for a second to allow the camera sensor to warm up

frame = vs.read()  # grab the frame from the threaded video file stream

frame = cv2.resize(frame, (256, 256))  # resize the frame
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale channels

img_tensor = image.img_to_array(gray)  # (height, width, channels)
img_tensor = np.expand_dims(img_tensor, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
img_tensor /= 255.

# Calling the predict function using keras
prediction = model.predict(img_tensor)
print(prediction)

cv2.imshow("frame",frame)
cv2.waitKey()
