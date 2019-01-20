from flask import Flask, request, render_template
import pandas as pd
from X_Engine.master_lightsaber import lightsaber
import time
import pickle
import numpy as np


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('forms/form_with_static.html')
    elif request.method == 'POST':
        kwargs = {
            'File_Path': request.form['File_Path'],
            # 'isbn': request.form['isbn'],
            # 'author': request.form['author'],
            'developer': request.form['Developer'],
            'submit_value': request.form['submit'],
        }
        print(kwargs['File_Path'])
        file_path = kwargs['File_Path']
        result = predict(file_path)
        kwargs['result'] = result
        return render_template(
            'forms/basic_form_result.html', **kwargs)

def predict(file_path):
    data = pd.read_csv(file_path)
    # col_name = ['Time', 'Xpath_id', 'event_type', 'control_type']
    # data.columns = col_name

    # data = pd.DataFrame()

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