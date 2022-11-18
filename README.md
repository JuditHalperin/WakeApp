# WakeApp

WakeApp is a system that can automatically detect a driver drowsiness in a real-time video stream, using computer vision and neural network (deep learning) algorithms.

The classification is based on blinks, yawns, current time, and travel duration. When the driver appears to be drowsy, the system will play an alarm in the car and send a warning email to an emergency contact.

## Folder Structure

The main folder contains `Data` and `Scripts` directories, a `README` file, and an example video.

`Data` folder includes the alarm sound, email warning message, shape predictor, and background and logo images. `Dataset` contains classified images (train, validation and test), and `Model` includes summary and output, confusion matrix and scores, loss and accuracy plots, and the yawn detection model itself.

`Scripts` folder includes the following Python scripts:

The first GUI page is `start_page.py`, which reads the user details and starts the program. The second page is `drowsiness_classification.py`, which detects the driver drowsiness and displays the video frames.

The blink and yawn detection functions are in `blink_score.py` and `yawn_score.py` respectively. The counter thresholds are calculated in `thresholds.py`. The sound and email functions are listed in `drowsiness_alert.py`.

The yawn classification model was built with `convolutional_neural_network_model.py`, and its scores were evaluated using `convolutional_neural_network_metrics.py`.

To start the app, run `start_page.py`.
