from flask import Flask, render_template, request, url_for, redirect, jsonify
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

# Initialize the pre-trained Inception V3 model
model = InceptionV3(weights='imagenet')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField('File',  validators=[InputRequired(), FileAllowed(['mp4'], 'Videos only!'), FileSize(max_size=5000000)])
    submit = SubmitField('Upload File')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data # grab the file
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            return redirect('/')
            # return f"File hase been uploaded"
    else:
        return render_template('index.html', form = form)


if(__name__ == "__main__"):
    app.run(debug = True)