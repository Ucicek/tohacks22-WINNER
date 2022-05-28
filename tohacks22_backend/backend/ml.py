# data science libraries
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

np.random.seed(1000)

# print validation statement
print("all resources loaded")


def HAM10000(path):
    print('processing HAM10000 algorithm')

    # getting the image
    im = Image.open(path[1:])
    im = np.asarray(im)
    im = np.resize(im, (1,28,28,3))
    print(im.shape)

    # working with the model
    model = tf.keras.models.load_model('ml_model/model.h5')
    pred = model.predict(im)[0]
    print(pred)

    pred = tf.math.argmax(pred)
    print(pred)

    class_labels = ['akiec', 'bcc', 'df', 'bcc', 'nv', 'vasc', 'mel']
    specific_labels = {
        'nv': 'melanocytic nevi (nv)',
        'mel': 'melanoma (mel)',
        'bkl': 'benign keratosis-like lesions (solar lentigines / seborrheic keratoses and lichen-planus like keratoses) (bkl)',
        'bcc': 'basal cell carcinoma (bcc)',
        'akiec': 'Actinic keratoses and intraepithelial carcinoma / Bowens disease (akiec)',
        'vasc': 'vascular lesions (angiomas, angiokeratomas, pyogenic granulomas and hemorrhage) (vasc)',
        'df': 'dermatofibroma (df)'
    }
    label = specific_labels[class_labels[pred]]

    return label