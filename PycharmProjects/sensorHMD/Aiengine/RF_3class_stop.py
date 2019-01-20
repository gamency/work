# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
# from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import pickle


# n_estimators=40, max_depth=45, min_samples_split=5, max_features=5)

def rf_3class_train(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    df_stop = dataframe[dataframe['scenario'] == 0]

    class_index = (df_stop['class'] != 0)
    df_stop.loc[class_index, 'class'] = 1

    labels_true_of_stop = df_stop['class']
    train_data_stop = df_stop.iloc[:, 0:scenario_column_number]

    x_train, x_test, y_train, y_test = train_test_split(train_data_stop, labels_true_of_stop, test_size=0.4)

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

    rf_model = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)

    rf_model.fit(x_train, y_train)
    print('best parameters set is：%0.3f' % rf_model.best_score_)

    print("accuracy at split test set is", rf_model.score(x_test, y_test))
    filename = '../Model/all_sensor_rf_model_3class_50len.sav'
    pickle.dump(rf_model, open(filename, 'wb'))

    return rf_model


def __main__():
    # data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'
    data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv'

    df = pd.read_csv(data_dir)

    model = rf_3class_train(df)
    return model


if __name__ == '__main__':
    print("execute raw data fetch")
    re = __main__()
