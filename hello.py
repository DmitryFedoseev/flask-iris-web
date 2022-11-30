from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file 
import numpy as np
import os
import joblib
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import pandas as pd


app = Flask(__name__)

knn = joblib.load('knn.pkl')
 
@app.route('/')
def hello_world():  
    print(1+2)
    return "<h1>Hello my best friend nikita!!!!</h1>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = mean(nums)
    print(nums_mean)
    return str(nums_mean)

@app.route('/iris/<param>')
def iris(param):

    param = param.split(',')  
    param = [float(num) for num in param]
    
    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param) 

    return str(predict)

@app.route('/show_image')
def show_image():
    return '<img src="/static/irissetosa.jpg" alt="iris setosa">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)

@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()

        param = content['flower'].split(',')  
        param = [float(num) for num in param]

        param = np.array(param).reshape(1, -1)
        predict = knn.predict(param) 

        predict = {'class':str(predict[0])}
    except:
        return redirect(url_for('bad_request')) 

    return jsonify(predict) 

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name.data)
        
        f = form.file.data
        filename = form.name.data + '.csv'
        #f.save(os.path.join(
        #    filename
        #))

        df = pd.read_csv(f, header=None)
        print(df.head())

        predict = knn.predict(df)

        print(predict)

        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)

        return send_file(filename,
                        mimetype='text/csv',
                        download_name=filename,
                        as_attachment=True)

    return render_template('submit.html', form=form)