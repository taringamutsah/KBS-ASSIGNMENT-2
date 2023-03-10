from flask import Flask, render_template, request, url_for, redirect, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import io
import json
import cv2
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from flask import Flask, request, jsonify
import pandas as pd

# Initialize the pre-trained Inception V3 model
model = InceptionV3(weights='imagenet')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# class UploadFileForm(FlaskForm):
#     file = FileField('File',  validators=[InputRequired(), FileAllowed(['mp4'], 'Videos only!'), FileSize(max_size=5000000)])
#     submit = SubmitField('Upload File')

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File size exceeds 5 MB limit.')
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
     
        # Extract the video from the request
        file = request.files['video']
        filename = file.filename

        #save the video in local file
        file.save('static/files/videos/' + filename)
        video = file.read()
        path = f'static/files/videos/{file.filename}'

        # Split the video into frames
        cap = cv2.VideoCapture(path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()

        # Feed the frames into the Inception V3 model to detect objects
        results = []
        for frame in frames:
            # Preprocess the frame for the Inception V3 model
            img = cv2.resize(frame, (299, 299))
            img = preprocess_input(img)
            img = tf.expand_dims(img, axis=0)

            # Feed the frame into the Inception V3 model to detect objects
            preds = model.predict(img)
            preds = decode_predictions(preds, top=3)[0]

            # Save the output of the model for each frame
            frame_results = []
            for pred in preds:
                frame_results.append({'label': pred[1], 'probability': float(pred[2])})
            results.append(frame_results)
        data = jsonify(results)
        # data_path =  os.path.join(app.static_folder, 'files','json')
        # with open(data_path, 'w') as f:
        #     json.dump(data, f)
        # results.to_csv(f"static/files/json/{file.filename}", header=True)
        df = pd.DataFrame(results)
        df.to_json(f"static/files/json/{file.filename}.json", orient="records")
        return redirect(url_for('objects', name = file.filename ))
    else:
        return render_template('index.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/objects',methods=['POST', 'GET'])
def objects():
    object_name = request.args.get('name')
    with open(f'static/files/json/{object_name}.json', 'r') as f:
        data = json.load(f)
    return render_template('objects.html', object_name = object_name, data = data)

if(__name__ == "__main__"):
    app.run(debug = True)