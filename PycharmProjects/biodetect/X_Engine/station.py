import pandas as pd

from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pickle
from xgboost.sklearn import XGBClassifier
from sklearn import metrics


def model_train(x_train, x_test, y_train, y_test, save_model=False):
    # column_name = list(dataframe.columns)
    # scenario_column_number = column_name.index('scenario')
    # # print(scenario_column_number)
    #
    # #df_stop = dataframe[dataframe['scenario'] == 0]
    # dataframe = dataframe[dataframe['scenario'] == 0]
    #
    # #class_index = (df_stop['class'] != 0)
    # class_index = (dataframe['class'] != 0)
    # #df_stop.loc[class_index, 'class'] = 1
    # dataframe.loc[class_index, 'class'] = 1
    #
    # #labels_true_of_stop = df_stop['class']
    # labels_true_of_stop = dataframe['class']
    # #train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
    # train_data_stop = dataframe.iloc[:, 0:scenario_column_number]
    #
    # X_train, X_test, y_train, y_test = train_test_split(train_data_stop, labels_true_of_stop, test_size=0.4)

    pipeline = Pipeline([
        ('clf', XGBClassifier())
    ])

    parameters = {
        'clf__n_estimators': (list(range(10, 500, 100)))
        # 'clf__criterion': ('gini', 'entropy'),
        # 'clf__max_depth': (None, 2, 5, 10, 15, 30, 60),
        # 'clf__min_samples_leaf': (1, 2, 5),
        # 'clf__min_samples_split': (2, 5, 8, 50)
    }

    xg_model = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)

    xg_model.fit(x_train, y_train)
    print('best parameters set is：%0.3f' % xg_model.best_score_)

    print("accuracy at split test set is", xg_model.score(x_test, y_test))

    model_name = ''
    if save_model:
        filename = '../Model/' + model_name
        pickle.dump(xg_model, open(filename, 'wb'))
    print(xg_model.best_params_)

    return xg_model

column_name = list(res.columns)
label_column_number = column_name.index('Bot')

    # train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
ground_true = res['Bot']

train_data = res.iloc[:, 0:label_column_number]

x_train, x_test, y_train, y_test = train_test_split(train_data, ground_true, test_size=0.4)

    # model_name = 'all_sensor_xg_model_3class_50len.sav'

model = model_train(x_train, x_test, y_train, y_test, save_model=False)





def metrics_report(model, validation_data, validation_label):
    print("score is:\n", model.score(validation_data, validation_label))
    print("confusion matrix is:\n", metrics.confusion_matrix(model.predict(validation_data), validation_label))
    target_name = ['none', 'activity']
    print("classification report is:\n", metrics.classification_report(validation_label, model.predict(validation_data),
                                                                       target_names=target_name))
    # print("auc score is:\n", metrics.auc(validation_data, validation_label))
    # print('precision and recall is:\n', metrics.precision_score(validation_label, model.predict(validation_data)))
    # print("F1 score is:\n", metrics.f1_score(validation_label, model.predict(validation_data)))
    print("precision recall with beta = 0.6 \n",
          metrics.precision_recall_fscore_support(validation_label, model.predict(validation_data), beta=0.6))



    # metrics.
    pass


filename = "/Users/kite/PycharmProjects/biometricsdetect/Model/201801171536_bio_stage2xgpc.sav"
pickle.dump(model, open(filename, 'wb'), protocol=2)

test_d = [2.5472699707521631, 262.34615323932348, 40409.896169330685, 201.02212855636239, 4380086.3667088235, 3176009829.4468203, 1.4178142268036926, 0.4385979586685409, 0.662267286424855, 0.75470372536277663, -0.79144875633990108, -0.0019123648429070297, 0.042870278874807766, 0.12926798895500519, -1.2799509165768266, 1.4092189055318318, 4.6328826192043593e-14, -24.285109741850878, 654.76188852021914, 1.5661742909165997, 0.28133975951703305, 241.30185850147834, 35910.658709136667, 189.50107838515501, 5085330.5371061778, 3112653932.3170829, 0.14264710850242404, 0.0079465741257098155, 0.089143559081460363, 0.73387084291088178, -0.12344483280973831, 0.0002112160356734483, 0.00460889651138539, 0.10100490262490065, -0.015737569236358342, 0.116742471861259, -1.2622823793162485e-15, 16.961504387674523, 327.98485963606743, 0.16838548127088129, 10.879040628951522, 332.51029276024309, 36959.849599415073, 192.24944629156951, 28.221009563908638, 2458840971.4638371, 10.296940709494855, 0.003620901213579423, 0.060173924698156619, -0.41285452013963442, 3.2612266032147446, 0.008167447919633248, 0.28203455999221183, 10.297242501029098, 0.0, 10.297242501029098, 8.9980106698916984e-14, 36.492791580663116, 1331.8153079712981, 10.297610728402683, 49.925424594395643, 332.51513376946673, 36956.096689180202, 192.23968552091475, 264.7404723947007, 2458245345.6382165, 41.188607883906712, 0.52845275738215525, 0.72694756164537433, -0.6879224416448716, 8.4096362246338305, 0.037481549995792576, 1.128323152650056, 41.188970004116392, 0.0, 41.188970004116392, -5.8675286851439523e-14, 36.462125724384002, 1330.3168057158568, 41.202645309783456, 310.47804201136063, 332.09537895363388, 37003.089062118481, 192.36187008375251, -5293.4731901909181, 2462840336.5691409, 165.09698670214638, 146.06961431027986, 12.085926290950143, -0.10629908249860323, 5.8155297902607677, 0.2330916231316527, 4.534193961743437, 164.75588001646557, 0.0, 164.75588001646557, -1.1038392422335619e-12, 35.913439724357133, 1303.2672788328284, 165.70106956362636, 131.96209228150298, 332.08287352701467, 37048.121042683895, 192.4788846670821, 29627.02283050563, 2468336107.8588295, 116.84591791844518, 74.675536015270183, 8.6415007964629726, 0.29950367051521454, 5.0235647142341486, 0.09907063985097823, 3.2088640205004473, 116.5, -5.6363636363636367, 122.13636363636364, -4.2085779305978122e-13, 35.871272160980006, 1301.8165488103507, 117.16834993830403, 1.40488086801221, 325.79088829341481, 37966.378859286466, 194.84963140659636, 145184.91258861581, 2569856870.7043428, 46.926322158765423, 263.23975445538633, 16.224665002870978, 0.10948119079979825, -0.36230815167042274, -0.0010547153663755305, 1.3604078740491454, 4.583333333333333, -43.5, 48.083333333333336, 1.6659069956848072e-13, -26.703987428028533, 818.43785300506875, 49.650243175011212, 383.0, 328.92833084737509, 37675.785316225345, 194.10251239029685, 447683.26246721618, 2543895917.455183, 745.48327065838623, 113639.78926457182, 337.10501222107604, 0.050617004658163919, -0.85604015474406225, 0.2875375375375375, 22.392534033082548, 466.0, -588.0, 1054.0, -1.3884005056752358e-11, -5.9837684009231138, 508.69604717955002, 817.31817549837956, 700.0, 319.91943680873476, 39064.776160226465, 197.64811195715092, 268444.32412419992, 2690543589.9435973, 623.02146413433013, 94246.198170858595, 306.9954367264416, 0.33190421198289033, -0.30634520637320006, 0.5255255255255256, 19.021446173033436, 409.0, -434.0, 843.0, -1.4059420294643132e-11, -2.593863409075869, 377.55789364271413, 694.4825411772423]

{"event_info":"{\"mouse_event_type\":[1,1,0,1,1,1,1,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,0,0,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3],\"Action\":[\"0\",\"38\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"38\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"38\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"38\",\"0\",\"0\",\"0\",\"38\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"38\",\"0\",\"38\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"39\"],\"key_event_type\":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\"Time\":[1516950045851,1516950045920,1516950046242,1516950326720,1516950326736,1516950326751,1516950326768,1516950326784,1516950326802,1516950326818,1516950326835,1516950326851,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950326868,1516950327243,1516950327445,1516950327645,1516950327766,1516950327782,1516950327798,1516950327817,1516950327832,1516950327848,1516950327865,1516950327882,1516950328246,1516950330209,1516950330216,1516950330255,1516950330319,1516950330351,1516950330383,1516950330645,1516950330712,1516950330719,1516950330732,1516950331044,1516950332950,1516950332966,1516950332982,1516950332999,1516950333015,1516950333032,1516950333049,1516950333065,1516950333083,1516950333099,1516950333116,1516950333132,1516950333149,1516950333365,1516950333382,1516950333399,1516950333415,1516950333432,1516950333449,1516950333466,1516950333482,1516950333499,1516950333515,1516950333532,1516950333549,1516950333566,1516950333589,1516950333598,1516950333615,1516950333632,1516950333649,1516950333665,1516950333682,1516950333699,1516950333715,1516950333732,1516950333749,1516950333766,1516950333783,1516950333798,1516950334045,1516950334486,1516950334509,1516950334806,1516950334809,1516950334815,1516950334816,1516950334832,1516950334832,1516950334849,1516950334849,1516950334865,1516950334866,1516950334882,1516950334883,1516950334898,1516950334899,1516950334916,1516950334917,1516950334934,1516950334935,1516950334949,1516950334950,1516950334966,1516950334966,1516950334983,1516950334983,1516950335039,1516950335039,1516950335278,1516950335278,1516950335286,1516950335286,1516950335298,1516950335299,1516950335316,1516950335317,1516950335332,1516950335333,1516950335349,1516950335349,1516950335365,1516950335366,1516950335382,1516950335382,1516950335398,1516950335399,1516950335415,1516950335416,1516950335432,1516950335432,1516950335449,1516950335449,1516950335465,1516950335466,1516950335482,1516950335483,1516950335499,1516950335499,1516950335516,1516950335516,1516950335532,1516950335533,1516950335807,1516950335808,1516950335815,1516950335815,1516950335832,1516950335832,1516950335848,1516950335849,1516950335865,1516950335866,1516950335882,1516950335883,1516950335899,1516950335899,1516950335916,1516950335916,1516950335932,1516950335933,1516950335949,1516950335950,1516950335967,1516950335967,1516950335982,1516950335983,1516950335998,1516950335999,1516950336015,1516950336016,1516950336032,1516950336032,1516950336049,1516950336049,1516950336065,1516950336066,1516950336082,1516950336083,1516950336099,1516950336099,1516950336115,1516950336115,1516950336132,1516950336132,1516950336639,1516950336639,1516950336663,1516950336663,1516950336703,1516950336703,1516950336751,1516950336752,1516950336823,1516950336823,1516950337336,1516950337336,1516950337367,1516950337368,1516950337407,1516950337407,1516950338384],\"dialog_type\":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\"op_x\":[700,573,573,781,804,836,844,850,852,853,853,851,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,846,845,838,832,824,814,804,804,1010,1010,1010,1010,1009,1009,1009,1009,1009,1009,1009,888,833,771,710,660,629,595,577,567,559,556,556,558,558,561,565,569,571,574,575,575,576,576,576,576,576,576,576,576,576,576,577,579,581,582,584,584,585,585,585,585,585,585,585,585,586,586,587,587,588,588,589,589,591,591,592,592,594,594,595,595,597,597,597,597,598,598,598,598,598,598,598,598,599,599,601,601,603,603,605,605,608,608,612,612,615,615,617,617,619,619,621,621,623,623,623,623,624,624,625,625,625,625,625,625,627,627,631,631,635,635,640,640,643,643,646,646,648,648,650,650,651,651,652,652,653,653,654,654,655,655,656,656,657,657,659,659,659,659,660,660,660,660,660,660,661,661,661,661,661,661,661,661,662,662,661,661,661,661,661,661,661],\"op_y\":[324,395,395,392,376,349,341,335,333,332,332,335,340,340,341,344,349,355,367,387,387,387,388,388,388,388,388,388,388,388,340,340,340,388,389,391,400,410,422,436,449,449,454,454,454,454,454,454,454,454,454,454,454,454,446,436,425,414,407,400,396,394,393,392,392,390,390,395,401,407,410,414,415,416,417,417,417,417,418,418,418,418,419,419,419,420,420,421,421,421,421,422,422,422,422,422,422,422,422,422,422,422,422,422,423,423,423,423,423,423,423,423,423,423,423,423,423,423,423,423,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,424,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,425,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426,426]}","true_info":"{\"correct_y\":608,\"correct_x\":608,\"scenario\":1,\"slidebarleft_x\":350,\"slidebarleft_y\":572,\"slidebarright_y\":450,\"terminal\":0,\"slidebarright_x\":414}"}



{"answerPosition":{"curTime":1520217979473,"point":{"x":235,"y":10}},"correctX":675,"correctY":733,"initialTimeStamp":1520217876374,"mouseEvents":[{"action":0,"eventType":1,"point":{"x":8,"y":1004},"timestamp":89633},{"action":0,"eventType":1,"point":{"x":41,"y":984},"timestamp":89650},{"action":0,"eventType":1,"point":{"x":94,"y":962},"timestamp":89666},{"action":0,"eventType":1,"point":{"x":165,"y":945},"timestamp":89683},{"action":0,"eventType":1,"point":{"x":238,"y":937},"timestamp":89700},{"action":0,"eventType":1,"point":{"x":285,"y":937},"timestamp":89717},{"action":0,"eventType":1,"point":{"x":299,"y":937},"timestamp":89733},{"action":0,"eventType":1,"point":{"x":309,"y":937},"timestamp":89767},{"action":0,"eventType":1,"point":{"x":310,"y":937},"timestamp":89934},{"action":0,"eventType":1,"point":{"x":333,"y":930},"timestamp":89951},{"action":0,"eventType":1,"point":{"x":368,"y":917},"timestamp":89967},{"action":0,"eventType":1,"point":{"x":444,"y":899},"timestamp":89984},{"action":0,"eventType":1,"point":{"x":632,"y":882},"timestamp":90001},{"action":0,"eventType":1,"point":{"x":823,"y":888},"timestamp":90018},{"action":0,"eventType":1,"point":{"x":1009,"y":925},"timestamp":90034},{"action":0,"eventType":1,"point":{"x":1010,"y":925},"timestamp":90250},{"action":0,"eventType":1,"point":{"x":1021,"y":919},"timestamp":90268},{"action":0,"eventType":1,"point":{"x":1038,"y":911},"timestamp":90284},{"action":0,"eventType":1,"point":{"x":1058,"y":903},"timestamp":90300},{"action":0,"eventType":1,"point":{"x":1103,"y":890},"timestamp":90317},{"action":0,"eventType":1,"point":{"x":1156,"y":879},"timestamp":90334},{"action":12,"eventType":1,"point":{"x":1193,"y":874},"timestamp":90350},{"action":0,"eventType":0,"point":{"x":1193,"y":874},"timestamp":90608},{"action":12,"eventType":1,"point":{"x":749,"y":1042},"timestamp":94201},{"action":0,"eventType":0,"point":{"x":749,"y":1042},"timestamp":94409},{"action":12,"eventType":1,"point":{"x":159,"y":1017},"timestamp":94574},{"action":0,"eventType":0,"point":{"x":159,"y":1017},"timestamp":94808},{"action":12,"eventType":1,"point":{"x":9,"y":997},"timestamp":94935},{"action":0,"eventType":0,"point":{"x":9,"y":997},"timestamp":95209},{"action":12,"eventType":1,"point":{"x":461,"y":912},"timestamp":101585},{"action":0,"eventType":2,"point":{"x":461,"y":912},"timestamp":101595},{"action":0,"eventType":1,"point":{"x":466,"y":913},"timestamp":101619},{"action":0,"eventType":1,"point":{"x":466,"y":913},"timestamp":101623},{"action":0,"eventType":1,"point":{"x":469,"y":914},"timestamp":101635},{"action":0,"eventType":1,"point":{"x":469,"y":914},"timestamp":101635},{"action":0,"eventType":1,"point":{"x":470,"y":915},"timestamp":101652},{"action":0,"eventType":1,"point":{"x":470,"y":915},"timestamp":101653},{"action":0,"eventType":1,"point":{"x":472,"y":916},"timestamp":101669},{"action":0,"eventType":1,"point":{"x":472,"y":916},"timestamp":101669},{"action":0,"eventType":1,"point":{"x":476,"y":917},"timestamp":101685},{"action":0,"eventType":1,"point":{"x":476,"y":917},"timestamp":101686},{"action":0,"eventType":1,"point":{"x":477,"y":918},"timestamp":101702},{"action":0,"eventType":1,"point":{"x":477,"y":918},"timestamp":101703},{"action":0,"eventType":1,"point":{"x":479,"y":919},"timestamp":101718},{"action":0,"eventType":1,"point":{"x":479,"y":919},"timestamp":101720},{"action":0,"eventType":1,"point":{"x":484,"y":920},"timestamp":101735},{"action":0,"eventType":1,"point":{"x":484,"y":920},"timestamp":101736},{"action":0,"eventType":1,"point":{"x":486,"y":921},"timestamp":101752},{"action":0,"eventType":1,"point":{"x":486,"y":921},"timestamp":101753},{"action":0,"eventType":1,"point":{"x":488,"y":922},"timestamp":101769},{"action":0,"eventType":1,"point":{"x":488,"y":922},"timestamp":101769},{"action":0,"eventType":1,"point":{"x":492,"y":923},"timestamp":101785},{"action":0,"eventType":1,"point":{"x":492,"y":923},"timestamp":101786},{"action":0,"eventType":1,"point":{"x":497,"y":924},"timestamp":101802},{"action":0,"eventType":1,"point":{"x":497,"y":924},"timestamp":101802},{"action":0,"eventType":1,"point":{"x":502,"y":925},"timestamp":101818},{"action":0,"eventType":1,"point":{"x":502,"y":925},"timestamp":101819},{"action":0,"eventType":1,"point":{"x":503,"y":926},"timestamp":101836},{"action":0,"eventType":1,"point":{"x":503,"y":926},"timestamp":101836},{"action":0,"eventType":1,"point":{"x":508,"y":927},"timestamp":101852},{"action":0,"eventType":1,"point":{"x":508,"y":927},"timestamp":101853},{"action":0,"eventType":1,"point":{"x":509,"y":928},"timestamp":101869},{"action":0,"eventType":1,"point":{"x":509,"y":928},"timestamp":101869},{"action":0,"eventType":1,"point":{"x":514,"y":929},"timestamp":101885},{"action":0,"eventType":1,"point":{"x":514,"y":929},"timestamp":101886},{"action":0,"eventType":1,"point":{"x":518,"y":930},"timestamp":101901},{"action":0,"eventType":1,"point":{"x":518,"y":930},"timestamp":101902},{"action":0,"eventType":1,"point":{"x":522,"y":931},"timestamp":101918},{"action":0,"eventType":1,"point":{"x":522,"y":931},"timestamp":101919},{"action":0,"eventType":1,"point":{"x":525,"y":932},"timestamp":101936},{"action":0,"eventType":1,"point":{"x":525,"y":932},"timestamp":101936},{"action":0,"eventType":1,"point":{"x":529,"y":933},"timestamp":101952},{"action":0,"eventType":1,"point":{"x":529,"y":933},"timestamp":101952},{"action":0,"eventType":1,"point":{"x":532,"y":934},"timestamp":101969},{"action":0,"eventType":1,"point":{"x":532,"y":934},"timestamp":101970},{"action":0,"eventType":1,"point":{"x":535,"y":935},"timestamp":101985},{"action":0,"eventType":1,"point":{"x":535,"y":935},"timestamp":101986},{"action":0,"eventType":1,"point":{"x":539,"y":936},"timestamp":102002},{"action":0,"eventType":1,"point":{"x":539,"y":936},"timestamp":102003},{"action":0,"eventType":1,"point":{"x":541,"y":937},"timestamp":102019},{"action":0,"eventType":1,"point":{"x":541,"y":937},"timestamp":102020},{"action":0,"eventType":1,"point":{"x":546,"y":938},"timestamp":102035},{"action":0,"eventType":1,"point":{"x":546,"y":938},"timestamp":102038},{"action":0,"eventType":1,"point":{"x":551,"y":939},"timestamp":102051},{"action":0,"eventType":1,"point":{"x":551,"y":939},"timestamp":102053},{"action":0,"eventType":1,"point":{"x":553,"y":940},"timestamp":102068},{"action":0,"eventType":1,"point":{"x":553,"y":940},"timestamp":102069},{"action":0,"eventType":1,"point":{"x":557,"y":941},"timestamp":102085},{"action":0,"eventType":1,"point":{"x":557,"y":941},"timestamp":102086},{"action":0,"eventType":1,"point":{"x":562,"y":942},"timestamp":102102},{"action":0,"eventType":1,"point":{"x":562,"y":942},"timestamp":102103},{"action":0,"eventType":1,"point":{"x":563,"y":943},"timestamp":102118},{"action":0,"eventType":1,"point":{"x":563,"y":943},"timestamp":102119},{"action":0,"eventType":1,"point":{"x":564,"y":944},"timestamp":102136},{"action":0,"eventType":1,"point":{"x":564,"y":944},"timestamp":102138},{"action":0,"eventType":1,"point":{"x":567,"y":945},"timestamp":102152},{"action":0,"eventType":1,"point":{"x":567,"y":945},"timestamp":102153},{"action":0,"eventType":1,"point":{"x":569,"y":946},"timestamp":102168},{"action":0,"eventType":1,"point":{"x":569,"y":946},"timestamp":102170},{"action":0,"eventType":1,"point":{"x":571,"y":947},"timestamp":102185},{"action":0,"eventType":1,"point":{"x":571,"y":947},"timestamp":102186},{"action":0,"eventType":1,"point":{"x":572,"y":948},"timestamp":102202},{"action":0,"eventType":1,"point":{"x":572,"y":948},"timestamp":102203},{"action":0,"eventType":1,"point":{"x":574,"y":949},"timestamp":102219},{"action":0,"eventType":1,"point":{"x":574,"y":949},"timestamp":102219},{"action":0,"eventType":1,"point":{"x":577,"y":950},"timestamp":102235},{"action":0,"eventType":1,"point":{"x":577,"y":950},"timestamp":102236},{"action":0,"eventType":1,"point":{"x":582,"y":951},"timestamp":102252},{"action":0,"eventType":1,"point":{"x":582,"y":951},"timestamp":102254},{"action":0,"eventType":1,"point":{"x":584,"y":952},"timestamp":102268},{"action":0,"eventType":1,"point":{"x":584,"y":952},"timestamp":102269},{"action":0,"eventType":1,"point":{"x":589,"y":953},"timestamp":102285},{"action":0,"eventType":1,"point":{"x":589,"y":953},"timestamp":102287},{"action":0,"eventType":1,"point":{"x":594,"y":954},"timestamp":102303},{"action":0,"eventType":1,"point":{"x":594,"y":954},"timestamp":102304},{"action":0,"eventType":1,"point":{"x":595,"y":955},"timestamp":102319},{"action":0,"eventType":1,"point":{"x":595,"y":955},"timestamp":102320},{"action":0,"eventType":1,"point":{"x":599,"y":956},"timestamp":102335},{"action":0,"eventType":1,"point":{"x":599,"y":956},"timestamp":102337},{"action":0,"eventType":1,"point":{"x":600,"y":957},"timestamp":102352},{"action":0,"eventType":1,"point":{"x":600,"y":957},"timestamp":102353},{"action":0,"eventType":1,"point":{"x":604,"y":958},"timestamp":102369},{"action":0,"eventType":1,"point":{"x":604,"y":958},"timestamp":102369},{"action":0,"eventType":1,"point":{"x":609,"y":959},"timestamp":102385},{"action":0,"eventType":1,"point":{"x":609,"y":959},"timestamp":102386},{"action":0,"eventType":1,"point":{"x":611,"y":960},"timestamp":102402},{"action":0,"eventType":1,"point":{"x":611,"y":960},"timestamp":102403},{"action":0,"eventType":1,"point":{"x":614,"y":961},"timestamp":102419},{"action":0,"eventType":1,"point":{"x":614,"y":961},"timestamp":102420},{"action":0,"eventType":1,"point":{"x":616,"y":962},"timestamp":102436},{"action":0,"eventType":1,"point":{"x":616,"y":962},"timestamp":102437},{"action":0,"eventType":1,"point":{"x":620,"y":963},"timestamp":102452},{"action":0,"eventType":1,"point":{"x":620,"y":963},"timestamp":102453},{"action":0,"eventType":1,"point":{"x":623,"y":964},"timestamp":102468},{"action":0,"eventType":1,"point":{"x":623,"y":964},"timestamp":102470},{"action":0,"eventType":1,"point":{"x":624,"y":965},"timestamp":102486},{"action":0,"eventType":1,"point":{"x":624,"y":965},"timestamp":102487},{"action":0,"eventType":1,"point":{"x":626,"y":966},"timestamp":102502},{"action":0,"eventType":1,"point":{"x":626,"y":966},"timestamp":102504},{"action":0,"eventType":1,"point":{"x":630,"y":967},"timestamp":102519},{"action":0,"eventType":1,"point":{"x":630,"y":967},"timestamp":102519},{"action":0,"eventType":1,"point":{"x":633,"y":968},"timestamp":102535},{"action":0,"eventType":1,"point":{"x":633,"y":968},"timestamp":102536},{"action":0,"eventType":1,"point":{"x":638,"y":969},"timestamp":102552},{"action":0,"eventType":1,"point":{"x":638,"y":969},"timestamp":102553},{"action":0,"eventType":1,"point":{"x":640,"y":970},"timestamp":102569},{"action":0,"eventType":1,"point":{"x":640,"y":970},"timestamp":102570},{"action":0,"eventType":1,"point":{"x":643,"y":971},"timestamp":102585},{"action":0,"eventType":1,"point":{"x":643,"y":971},"timestamp":102587},{"action":0,"eventType":1,"point":{"x":645,"y":972},"timestamp":102602},{"action":0,"eventType":1,"point":{"x":645,"y":972},"timestamp":102603},{"action":0,"eventType":1,"point":{"x":646,"y":973},"timestamp":102618},{"action":0,"eventType":1,"point":{"x":646,"y":973},"timestamp":102620},{"action":0,"eventType":1,"point":{"x":651,"y":974},"timestamp":102636},{"action":0,"eventType":1,"point":{"x":651,"y":974},"timestamp":102637},{"action":0,"eventType":1,"point":{"x":654,"y":975},"timestamp":102652},{"action":0,"eventType":1,"point":{"x":654,"y":975},"timestamp":102652},{"action":0,"eventType":1,"point":{"x":655,"y":976},"timestamp":102669},{"action":0,"eventType":1,"point":{"x":655,"y":976},"timestamp":102670},{"action":0,"eventType":1,"point":{"x":660,"y":977},"timestamp":102686},{"action":0,"eventType":1,"point":{"x":660,"y":977},"timestamp":102686},{"action":0,"eventType":1,"point":{"x":662,"y":978},"timestamp":102702},{"action":0,"eventType":1,"point":{"x":662,"y":978},"timestamp":102703},{"action":0,"eventType":1,"point":{"x":667,"y":979},"timestamp":102718},{"action":0,"eventType":1,"point":{"x":667,"y":979},"timestamp":102719},{"action":0,"eventType":1,"point":{"x":671,"y":980},"timestamp":102736},{"action":0,"eventType":1,"point":{"x":671,"y":980},"timestamp":102736},{"action":0,"eventType":1,"point":{"x":675,"y":981},"timestamp":102752},{"action":0,"eventType":1,"point":{"x":675,"y":981},"timestamp":102753},{"action":0,"eventType":1,"point":{"x":679,"y":982},"timestamp":102768},{"action":0,"eventType":1,"point":{"x":679,"y":982},"timestamp":102770},{"action":0,"eventType":1,"point":{"x":682,"y":983},"timestamp":102786},{"action":0,"eventType":1,"point":{"x":682,"y":983},"timestamp":102787},{"action":0,"eventType":1,"point":{"x":683,"y":984},"timestamp":102802},{"action":0,"eventType":1,"point":{"x":683,"y":984},"timestamp":102804},{"action":0,"eventType":1,"point":{"x":687,"y":985},"timestamp":102818},{"action":0,"eventType":1,"point":{"x":687,"y":985},"timestamp":102820},{"action":0,"eventType":1,"point":{"x":688,"y":986},"timestamp":102835},{"action":0,"eventType":1,"point":{"x":688,"y":986},"timestamp":102837},{"action":0,"eventType":1,"point":{"x":690,"y":987},"timestamp":102852},{"action":0,"eventType":1,"point":{"x":690,"y":987},"timestamp":102853},{"action":0,"eventType":1,"point":{"x":695,"y":988},"timestamp":102869},{"action":0,"eventType":1,"point":{"x":695,"y":988},"timestamp":102870},{"action":0,"eventType":1,"point":{"x":693,"y":989},"timestamp":102885},{"action":0,"eventType":1,"point":{"x":693,"y":989},"timestamp":102886},{"action":13,"eventType":3,"point":{"x":693,"y":989},"timestamp":102894}],"scenario":1,"slideBarLowerRight":{"x":482,"y":932},"slideBarTopLeft":{"x":440,"y":892},"terminal":0}