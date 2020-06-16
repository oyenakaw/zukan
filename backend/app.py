#!/usr/local/bin/python3
from flask import Flask, request, jsonify, make_response

from io import BytesIO
from PIL import Image as PILImage

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image as TFImage
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np
import os
import base64

import multiprocessing

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import json
with open('resources/imagenet_class_index.json','r',encoding="utf-8") as f:
    _data = json.load(f)
    class_names_to_ja_from_en = dict(zip(list(row['en'] for row in _data),list(row['ja'] for row in _data)))

graph = tf.get_default_graph()
model = ResNet50(weights='imagenet')

def _input(binary_image):
    if binary_image is None:
        return ''

    _img = PILImage.open(BytesIO(binary_image))

    _resize_img = _img.resize((224,224))
    x = TFImage.img_to_array(_resize_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

@app.route('/predict', methods=['POST'])
def predict():
    img_file = request.files['img_file']
    img_file.stream.seek(0)
    img_binary = img_file.stream.read()
    with graph.as_default():
        preds = model.predict(_input(img_binary))

    return make_response(jsonify({
            'image':base64.b64encode(img_binary).decode("utf-8"),
            'label':class_names_to_ja_from_en[decode_predictions(preds, top=1)[0][0][1]]
           }))

@app.route('/health', methods=['GET'])
def health():
  return make_response(jsonify({
            'health': 'OK'
           }))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)

