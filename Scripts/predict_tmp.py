

from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np


def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(256, 256), color_mode='grayscale')
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])
        plt.axis('off')
        plt.show()

    return img_tensor



# load model
model = load_model("yawn_detection1.h5")

# image path
img_path = '84.jpg'

# load a single image
new_image = load_image(img_path)

# check prediction
pred = model.predict(new_image)
print (pred)
#predictions = (model.predict(X) > 0.5).astype(int)