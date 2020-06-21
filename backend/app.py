#!/usr/local/bin/python3
from flask import Flask, request, jsonify, make_response

from io import BytesIO
from PIL import Image as PILImage

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image as TFImage
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from retry import retry
import tensorflow as tf
import numpy as np
import os
import base64
import json
import mysql.connector as dbc

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

with open('resources/imagenet_class_index.json','r',encoding="utf-8") as f:
    _data = json.load(f)
    class_names_to_ja_from_en = dict(zip(list(row['en'] for row in _data),list(row['ja'] for row in _data)))

graph = tf.get_default_graph()
model = ResNet50(weights='imagenet')
#model = load_model('resources/zukan_labeling_model.h5')

@retry(dbc.Error, tries=3, delay=10)
def db_connect():
    conn = dbc.connect (
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD'),
        database=os.environ.get('DB_DATABASE_NAME')
    )
    return conn

conn = db_connect()
conn.ping(reconnect=True)
    
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
    
    label = class_names_to_ja_from_en[decode_predictions(preds, top=1)[0][0][1]]

    cur = conn.cursor()
    user = "user"
    title = "title"
    image_data = base64.b64encode(img_binary).decode("utf-8")
    conn.start_transaction()
    stmt = f"INSERT INTO zukan (user_id,title,image_data,image_label) \
                VALUES ('{user}','{title}','{image_data}','{label}')"
    cur.execute(stmt)
    conn.commit()
    cur.close()

    return make_response(jsonify({
            'label':label
           }))

@app.route('/health', methods=['GET'])
def health():
    health = False
    health = conn.is_connected()
    return make_response(jsonify({
            'health': health
           }))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
