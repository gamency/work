import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model.logistic import LogisticRegression
# from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
# from sklearn.metrics import precision_score, recall_score, accuracy_score
import pickle
# from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import scale


def model_train(x_train_stop, x_test_stop, y_train_stop, y_test_stop, save_model=False):
    # column_name = list(dataframe.columns)
    # scenario_column_number = column_name.index('scenario')
    # # print(scenario_column_number)
    #
    # df_stop = dataframe[dataframe['scenario'] == 0]
    #
    # class_index = (df_stop['class'] != 0)
    # df_stop.loc[class_index, 'class'] = 1
    #
    # labels_true_of_stop = df_stop['class']
    # train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
    #
    # #labels_true_of_stop[labels_true_of_stop != 0] = 1
    #
    #
    # X_train_stop, X_test_stop, y_train_stop, y_test_stop = train_test_split(train_data_stop,
    #                                                                         labels_true_of_stop, test_size=0.4)
    # X_train_stop, X_test_stop, y_train_stop, y_test_stop =

    pipeline = Pipeline([
        ('clf', LogisticRegression())
    ])

    parameters = {
        'clf__penalty': ('l1', 'l2'),
        'clf__C': (0.01, 0.1, 1, 10),
    }

    binary_model_stop = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=4)

    binary_model_stop.fit(x_train_stop, y_train_stop)
    print('best parameters set is：%0.3f' % binary_model_stop.best_score_)

    print("accuracy at split test set is", binary_model_stop.score(x_test_stop, y_test_stop))

    print("predict result is\n", binary_model_stop.predict(x_test_stop))

    print("ground result is\n", np.array(y_test_stop))

    model_name = ''
    if save_model:
        filename = '/Users/kite/Desktop/human-machine-detect/Model/all_data_model/' + model_name
        pickle.dump(binary_model_stop, open(filename, 'wb'))

    return binary_model_stop


def __main__():
    data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'

    df = pd.read_csv(data_dir)

    column_name = list(df.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    df_stop = df[df['scenario'] == 0]

    class_index = (df_stop['class'] != 0)
    df_stop.loc[class_index, 'class'] = 1

    labels_true_of_stop = df_stop['class']
    train_data_stop = df_stop.iloc[:, 0:scenario_column_number]

    # labels_true_of_stop[labels_true_of_stop != 0] = 1

    x_train_stop, x_test_stop, y_train_stop, y_test_stop = train_test_split(train_data_stop, labels_true_of_stop,
                                                                            test_size=0.4)

    # model_name = 'all_sensor_rf_model_3class.sav'
    model = model_train(x_train_stop, x_test_stop, y_train_stop, y_test_stop, save_model=False)

    return model


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()
