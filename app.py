from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__)

class UploadFileForm(FlaskForm):
    file = FileField('File')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


if(__name__ == "__main__"):
    app.run(debug = True)