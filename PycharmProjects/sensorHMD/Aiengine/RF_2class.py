import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import pickle


#n_estimators=40, max_depth=45, min_samples_split=5, max_features=5)

def rf_2Class_train(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')

    # treat the class as two class, click, slide behavior here treat as class 1, so use dataframe 'class' as label
    #labels_true = dataframe['class']

    # if use scenario label, uncomment below
    labels_true = dataframe['scenario']
    train_data = dataframe.iloc[:, 0: scenario_column_number]

    # if use scenario label, comment below
    #labels_true[labels_true != 0] = 1

    #labels_true_of_stop = dataframe['scenario']
    #train_data_stop = dataframe.iloc[:, 0 : scenario_column_number]

    X_train, X_test, y_train, y_test = train_test_split(train_data, labels_true, test_size=0.4)

    pipeline = Pipeline([
        ('clf', RandomForestClassifier())
    ])

    parameters = {
        'clf__max_features': (list(range(3, 20, 2))),
        'clf__criterion': ('gini', 'entropy'),
        'clf__max_depth': (None, 2, 5, 10, 15, 30, 60),
        'clf__min_samples_leaf': (1, 2, 5),
        'clf__min_samples_split': (2, 5, 8, 50)
    }

    RF_model = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)

    RF_model.fit(X_train, y_train)
    print('best parameters set is：%0.3f' % RF_model.best_score_)

    print("accuracy at split test set is", RF_model.score(X_test, y_test))

    #filename = '../Model/all_sensor_rf_model_2class.sav'
    #pickle.dump(RF_model, open(filename, 'wb'))

    return RF_model


def __main__():
    #data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_1.csv'
    data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all.csv'

    df = pd.read_csv(data_dir)

    model = rf_2Class_train(df)


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()