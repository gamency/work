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
import time
from Fetch_raw_data_file import   generate_data_frame
from Clean_raw_data import clean_data
from Rss_statistict import  calc_Rss_statistict
from Time_Freq_featurelization import calc_time_freq_statistict
from Aiengine import RF
from Aiengine import XG



sensor_dimension_name = ['Acc_x', 'Acc_y', 'Acc_z', 'Gra_x', 'Gra_y', 'Gra_z', 'Gyr_x', 'Gyr_y', 'Gyr_z',
                         'Light', 'LAcc_x', 'LAcc_y', 'LAcc_z', 'Mag_x', 'Mag_y', 'Mag_z', 'Pres', 'Prox', 'ReHum',
                         'Rov_w', 'Rov_x', 'Rov_y', 'Rov_z', 'SteCou', 'TSD_value', 'id', 'scenario', 'behavior', 'class']


def DatanFeaturelizaiton(harbour_load, raw_data = False, predicting = False):
    if raw_data:
        raw_data_df = generate_data_frame(harbour_load)
    else:
        raw_data_df = harbour_load
    # print(train_raw_data_df.head())
    # VisualizationData(train_raw_data_df)
    # if predicting :
    #     clean_raw_df = raw_data_df
    # else:
    #     clean_raw_df = clean_data(raw_data_df, '', False)
    # print(clean_raw_df.head())
    # VisualizationData(clean_raw_df)

    direct_raw_df = raw_data_df.loc[:, sensor_dimension_name]
    print(direct_raw_df.describe())
    # Rss_clean_raw_df = calc_Rss_statistict(clean_raw_df, '', False)
    # print(Rss_clean_raw_df.head())
    # VisualizationData(Rss_clean_raw_df)

    # Feat_Rss_clean_raw_data_df = calc_time_freq_statistict(Rss_clean_raw_df,
    #                                                        './Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv',
    #                                                        save_file=False)
    # print(Feat_Rss_clean_raw_data_df.head())
    # VisualizationData(Rss_clean_raw_df)

    return direct_raw_df


def harbour_delivery(harbour, predicting = False):
    # ticket = {}
    ticket = pd.DataFrame()
    print(harbour)
    print(len(harbour))
    # for loadindex in list(range(len(harbour))):
    #     print("parth is ", harbour[loadindex])
    #     ticket[loadindex] = DatanFeaturelizaiton(harbour[loadindex], predicting)
    #     ticket = DatanFeaturelizaiton(harbour, predicting)
    ticket = DatanFeaturelizaiton(harbour, raw_data= True, predicting = False)
    # ticket = DatanFeaturelizaiton(loads)

    return ticket






def fire_on(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('id')
    df_station = dataframe[dataframe['scenario'] == 0]

    class_index = (df_station['class'] != 0)
    df_station.loc[class_index, 'class'] = 1

    train_label_ground_true = df_station['class']

    train_data = df_station.iloc[:, 0:scenario_column_number]

    print(train_label_ground_true)

    return train_data, train_label_ground_true




def __main__():
    # Feat_Rss_clean_raw_data_Test = DatanFeaturelizaiton(data_dir[0])
    base_dir = '/Users/kite/Desktop/human-machine-detect/Data'

    train_data_dir = base_dir + '/All_data'
    test_data_dir = base_dir + '/short_behavior_test_data'

    data_dir = [train_data_dir, test_data_dir]
    start_time = time.time()
    res = harbour_delivery(data_dir[0], predicting=False)

    train_data, train_label_ground_true = fire_on(res)

    # print(train_data.head())
    print(train_data.describe())

    X_train_stop, X_test_stop, y_train_stop, y_test_stop = train_test_split(train_data, train_label_ground_true,
                                                                            test_size=0.4)

    model = XG.model_train(X_train_stop, X_test_stop, y_train_stop, y_test_stop, False)
    # start_time = time.time()

    # print("**************************************res is")
    # print(res.head)
    # Predicting(res, '')
    # print("predict duration is: ",time.time() - start_time)
    filename = './Model/RF/direct3class.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()