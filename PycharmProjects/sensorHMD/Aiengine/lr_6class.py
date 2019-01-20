import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, accuracy_score
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale


def lr_6Class_train(dataframe):
    labels_true = dataframe['class']
    train_data = dataframe.iloc[:, 0:40]

    X_train, X_test, y_train, y_test = train_test_split(train_data, labels_true, test_size=0.4)

    pipeline = Pipeline([
        ('clf', LogisticRegression())
    ])

    parameters = {
        'clf__penalty': ('l1', 'l2'),
        'clf__C': (0.01, 0.1, 1, 10),
    }

    train_model = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)

    train_model.fit(X_train, y_train)

    print('best parameters set is：%0.3f' % train_model.best_score_)

    print("accuracy at split test set is", train_model.score(X_test, y_test))

    print("predict result is\n", train_model.predict(X_test))

    print("ground result is\n", np.array(y_test))



    #filename = '/Users/kite/Desktop/human-machine-detect/Model/all_data_model/Acc_gyr_lr_model_2class.sav'
    #pickle.dump(binary_model_stop, open(filename, 'wb'))

    return train_model

def __main__():
    data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'

    df = pd.read_csv(data_dir)

    model = lr_6Class_train(df)


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()