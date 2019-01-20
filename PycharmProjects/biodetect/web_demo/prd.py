from bottle import route, run, request, static_file
import time
import pandas as pd
# from Predict import fire_all
# from webdemo.processing import fire_all
# import profile


html = '''
<html>
    <body>
        <value value="predict result is" />
    </body>
    <h2>The probability of bot is:</h2>
            <table border="1" >
            <Caption> {0} </Caption>
            </table>
    <h2>Total duration is：</h2>
            <table border="1" >
            <Caption> {1} </Caption>
            </table>
</html>
'''


@route('/')
def root():
    return static_file('output.html', root='.')


@route('/predict', method='POST')
def predict():
    start_time = time.time()
    # Get the data

    upload = request.files.get('output')
    mydata = pd.read_csv(upload.file)
    # print(mydata.head())
    # mydata = list(csv.reader(upload.file, delimiter=','))
    # result = fire_all(mydata)

    result = 0
    duration = time.time() - start_time
    print(result)

    # Encode image to png in base64
    #  io = StringIO()
    #  fig.savefig(io, format='png')
    #  data = io.getvalue().encode('base64')
    return html.format(result, duration)


run(host='localhost', port=8071, debug=True)
