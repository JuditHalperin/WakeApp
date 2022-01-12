# WakeApp
Artificial Intelligence Project, 2022

WakeApp is a system that can automatically detect a driver drowsiness in a real-time video stream, using computer vision and neural network (deep learning) algorithms.

The classification is based on blinks, yawns, current time, and travel duration. When the driver appears to be drowsy, the system will play an alarm in the car and send a warning email to an emergency contact.

# Folder Structure
The main folder contains ‘Data’ and ‘Scripts’ directories, a README file, and an example video.

‘Data’ folder includes the alarm sound, email warning message, shape predictor, and background and logo images. ‘Dataset’ contains classified images (train, validation and test), and ‘Model’ includes summary and output, confusion matrix and scores, loss and accuracy plots, and the yawn detection model itself.

‘Scripts’ folder includes the following Python scripts:

The first GUI page is ‘start_page’, which reads the user details and starts the program. The second page is ‘drowsiness_classification’, which detects the driver drowsiness and displays the video frames.

The blink and yawn detection functions are in ‘blink_score’ and ‘yawn_score’ respectively. The counter thresholds are calculated in ‘thresholds’. The sound and email functions are listed in ‘drowsiness_alert’.

The yawn classification model was built with ‘convolutional_neural_network_model’, and its scores were evaluated using ‘convolutional_neural_network_metrics’.

To start the app, run ‘start_page’.
