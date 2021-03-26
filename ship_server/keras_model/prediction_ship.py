import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
import os


def ai_module(img):
    model_path = os.listdir(os.getcwd().replace('\\', '/') + '/keras_model/save_model/')
    model_name = os.getcwd().replace('\\', '/') + '/keras_model/save_model/' + model_path[0]
    model = tensorflow.keras.models.load_model(model_name, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = img.resize(size)
    image_array = np.asarray(image)
    normalized_image_array = image_array / 255.0
    data[0] = normalized_image_array
    prediction = model.predict(data)
    return prediction
