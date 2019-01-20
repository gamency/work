import time
import pickle
import numpy as np
import pandas as pd
import os
import json
from werkzeug import secure_filename
from flask import Flask, request, render_template
from X_Engine.master_lightsaber import lightsaber


UPLOAD_FOLDER = './tmpfile/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# bp = Blueprint('PredictService', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('uploadfile/form_with_static_upload.html')
    elif request.method == 'POST':
        # kwargs = {
        #     'direct_data': request.form['direct_data'],
        #     # 'developer': request.form['Developer'],
        #     # 'submit_value': request.form['submit'],
        # }
        # print(kwargs['direct_data'])
        # file_path = kwargs['direct_data']

        csv_file = request.files['file']

        if csv_file and allowed_file(csv_file.filename):
            csv_filename = secure_filename(csv_file.filename)
            csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename))

        df = pd.read_csv(UPLOAD_FOLDER + csv_filename)

        try:
            result = predict(df)[0]
            result = np.float32(result)
        except:
            print("lalalala got an error")
            result = "0.59613 galigali happen"

        os.remove(os.path.join(UPLOAD_FOLDER, csv_filename))

        # result = 0.0

        return render_template('uploadfile/predict_form_result.html', result=result)
    else:
        pass


@app.route('/direct_data', methods=['GET', 'POST'])
def direct_data():
    if request.method == 'GET':
        return render_template('uploadfile/form_with_static_direct_data.html')
    elif request.method == 'POST':
        kwargs = {
        'direct_data': request.form['direct_data'],
        # 'developer': request.form['Developer'],
        # 'submit_value': request.form['submit'],
        #     'Label': request.form['Label']
        }
        print(kwargs['direct_data'])
        file_path = kwargs['direct_data']
        jdf = json.loads(file_path)
        # df = pd.read_json(file_path['mouseEvents'])
        print(jdf['mouseEvents'])
        df = pd.DataFrame(jdf)
        df.to_csv("./tmpfile/direct_tmp.csv")
        # result = predict(df)
        # print(csv_file.filename)
        # print("**********",kwargs['Label'])
        # csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename))

        try:
            result = predict(df)[0]
            result = np.float32(result)
        except:
            print("lalalala got an error")
            result = "0.59613 galigali happen"
        # result = 0.89631
        kwargs['result'] = result

        # with open("test.txt", "wb") as fo:
        #     fo.write("This is Test Data")

        return render_template('uploadfile/predict_form_result.html',result=result)
        # return render_template('uploadfile/form_with_static_visualization_data.html')
    else:
        pass


@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'GET':
        return render_template('uploadfile/form_with_static_visualization_data.html')
    elif request.method == 'POST':
        kwargs = {
        # 'direct_data': request.form['direct_data'],
        'Label': request.form['Label'],
        # 'submit_value': request.form['submit'],
        }
        # print(kwargs['direct_data'])
        print("###########",kwargs['Label'])
        result = 0.0
        label = kwargs['Label']
        # direct_data_label()
        # return render_template('uploadfile/predict_form_result.html', result=kwargs['Label'])
        return render_template('uploadfile/predict_form_result.html', result=kwargs['Label'])

    else:
        pass


def predict(data):
    verify_info = {}
    verify_info["terminal"] = 0
    start_time = time.time()

    if verify_info["terminal"] == 0:
        JEDIP1 = "../Model/h5_behavior_login_registert.sav"
        JEDI = pickle.load(open(JEDIP1, 'rb'))
        print("terminal is H5")
    elif verify_info["terminal"] == 1:
        JEDIP2 = "../Model/ios_sensor_threesensor.sav"
        JEDI = pickle.load(open(JEDIP2, 'rb'))
        print("terminal is Andriod")
    elif verify_info["terminal"] == 2:
        JEDIP3 = "../Model/ios_sensor_threesensor.sav"
        JEDI = pickle.load(open(JEDIP3, 'rb'))
        print("terminal is Ios")
    else:
        return obi_won(0, 0)

    # try:
    #     result = lightsaber(data, JEDI, verify_info)
    #     print("Unexpected error:", sys.exc_info()[0])
    # except:
    #     print("lalalala got an error",obi_won(0, 0))
    #     return obi_won(0, 0)

    result = lightsaber(data, JEDI, verify_info)
    # print(type(result))
    result = np.float32(result)

    print("duration is: ", time.time() - start_time)
    print("the final result is: ", result)

    return result


def direct_data_label(battelfile, label):
    # print("label is", label)
    # print("battlefile is", battelfile)

    battelfile.append(label)

    return battelfile
