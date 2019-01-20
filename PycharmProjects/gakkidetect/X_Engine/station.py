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

