from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!'), FileSize(max_size=5000000)]

class UploadFileForm(FlaskForm):
    file = FileField('File',  validators=[InputRequired()])
    submit = SubmitField('Upload File')

@app.route('/', methods=['POST', 'GET'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return f"File '{file.filename}' hase been uploaded"
    return render_template('index.html', form = form)


if(__name__ == "__main__"):
    app.run(debug = True)