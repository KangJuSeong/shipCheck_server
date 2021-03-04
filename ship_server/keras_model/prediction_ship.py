import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
import os


def ai_module(img):
    start_time = time.time()
    model = tensorflow.keras.models.load_model(os.getcwd().replace('\\', '/') + '/keras_model/save_model/keras_model.h5'
                                               , compile=False)
    print("모델 로딩 시간 : ", time.time() - start_time)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    image = img.resize(size)
    image_array = np.asarray(image)
    normalized_image_array = image_array / 255.0
    data[0] = normalized_image_array
    start_time = time.time()
    prediction = model.predict(data)
    print("예측 종료 시간 : ", time.time() - start_time)
    return prediction
