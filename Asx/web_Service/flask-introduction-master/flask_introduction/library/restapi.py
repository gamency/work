from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/dashboard')
def request_info():
    calculate = {'get':0, 'post':1, 'put':1, 'patch':0, 'delete':0}
    sumall = 0

    for key, value in calculate.items():
        sumall += value
    calculate['total'] = sumall

    return render_template('resfulapi/restful.html',summary = calculate)