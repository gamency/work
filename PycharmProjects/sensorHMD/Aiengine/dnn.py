import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# from tensorflow.python.framework import ops
# ops.reset_default_graph()
#
# #data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_1.csv'
# data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv'
#
#
# train_df = pd.read_csv(data_dir)
# # df_stop = train_df[train_df['scenario'] == 0]
# #
# # labels_true_of_stop = np.array(df_stop['class']).astype(int)
# # train_data_stop = df_stop.iloc[:, 0:40]
#
#
# column_name = list(train_df.columns)
# scenario_column_number = column_name.index('scenario')
#     # print(scenario_column_number)
#
# df_stop = train_df[train_df['scenario'] == 0]
#
# class_index = (df_stop['class'] != 0)
# df_stop.loc[class_index, 'class'] = 1
#
# labels_true_of_stop = np.array(df_stop['class']).astype(int)
# train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
#
# #X_train, X_test, y_train, y_test = train_test_split(train_data_stop, labels_true_of_stop, test_size=0.4)
#
#
#
# #data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_mini_test_1.csv'
# data_dir = '../Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv'
#
#
# test_df = pd.read_csv(data_dir)
#
# column_name = list(test_df.columns)
# scenario_column_number = column_name.index('scenario')
#     # print(scenario_column_number)
#
# df_stop_test = test_df[test_df['scenario'] == 0]
#
# class_index = (df_stop_test['class'] != 0)
# df_stop_test.loc[class_index, 'class'] = 1
#
# test_labels_true_of_stop = np.array(df_stop_test['class']).astype(int)
# test_data_stop = df_stop_test.iloc[:, 0:scenario_column_number]
#
# print(test_data_stop.describe())

#
# feature_len = len(test_data_stop.columns)
#
# feature_columns = [tf.contrib.layers.real_valued_column("x",dimension=feature_len)]
#
# # classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
# # hidden_units=[100],
# # n_classes=2,
# # model_dir="../Model/DNN/Threeclass",
# # dropout = 0.2,
# # optimizer = tf.train.AdamOptimizer(1e-4))
#
# classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
# hidden_units=[100],
# n_classes=2,
# model_dir="../Model/DNN/Threeclass",
# dropout = 0.2,
# optimizer = tf.train.AdamOptimizer(1e-4))
#
# # classifier.fit(x = train_data_stop, y = labels_true_of_stop, steps=8000)
#
# # Define the training inputs
# train_input_fn = tf.estimator.inputs.numpy_input_fn(
#       x={"x": np.array(train_data_stop)},
#       y=np.array(labels_true_of_stop),
#       num_epochs=None,
#       shuffle=True)
#
#   # Train model.
# # classifier.train(input_fn=train_input_fn, steps=2000)
#
# classifier.train(train_input_fn, steps=2000)
#
# export_dir="../Model/DNN/test/"
#
# feature_spec = tf.feature_column.make_parse_example_spec(feature_columns)
#
# input_receiver_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
#
# # def serving_input_fn():
# #   x = tf.placeholder(dtype=tf.float32, shape=[None], name='x')
# #   y = tf.placeholder(dtype=tf.float32, shape=[None], name='y')
# #
# #   features = {'x': x, 'y': y}
# #   return tf.contrib.learn.utils.input_fn_utils.InputFnOps(features, None, default_inputs=features)
#
# # def serving_input_receiver_fn():
# #   """Build the serving inputs."""
# #   # The outer dimension (None) allows us to batch up inputs for
# #   # efficiency. However, it also means that if we want a prediction
# #   # for a single instance, we'll need to wrap it in an outer list.
# #   inputs = {"x": tf.placeholder(shape=[None, 240], dtype=tf.float32)}
# #   return tf.estimator.export.ServingInputReceiver(inputs, inputs)
#
# # export_dir = classifier.export_savedmodel(
# #     export_dir_base= export_dir,
# #     serving_input_receiver_fn=serving_input_receiver_fn)
#
# classifier.export_savedmodel(export_dir, input_receiver_fn, as_text=True)
#
#
# train_input_fn = tf.estimator.inputs.numpy_input_fn(
#       x={"x": np.array(train_data_stop)},
#       y=np.array(labels_true_of_stop),
#       num_epochs=1,
#       shuffle=False)
# train_accuracy_score = classifier.evaluate(train_input_fn)['accuracy']
#
# print("\n ************************************train set Accuracy******************: {0:f}".format(train_accuracy_score))
#
# #accuracy_score = classifier.evaluate(x = train_data, y = train_labels_true)['accuracy']
# #print("\n ************************************Accuracy******************: {0:f}".format(accuracy_score))
#
# # accuracy_score = classifier.evaluate(test_input_fn)['accuracy']
# test_input_fn = tf.estimator.inputs.numpy_input_fn(
#       x={"x": np.array(test_data_stop)},
#       y=np.array(test_labels_true_of_stop),
#       num_epochs=1,
#       shuffle=False)
# test_accuracy_score = classifier.evaluate(test_input_fn)['accuracy']
#
# print("\n ************************************test set Accuracy******************: {0:f}".format(test_accuracy_score))
#
# predict_input_fn = tf.estimator.inputs.numpy_input_fn(
#       x={"x": np.array(train_data_stop, dtype=np.float32)},
#       num_epochs=1,
#       shuffle=False)
#
# # train_pre = list(classifier.predict(train_data_stop, as_iterable=True))
# train_pre = list(classifier.predict(predict_input_fn))
# train_predicted_classes = [p["classes"] for p in train_pre]
# print("train prediction is\n", np.array(train_predicted_classes))
# print("train ground true is\n", labels_true_of_stop)
#
#
# predict_input_fn = tf.estimator.inputs.numpy_input_fn(
#       x={"x": np.array(test_data_stop, dtype=np.float32)},
#       num_epochs=1,
#       shuffle=False)
# # test_pre = list(classifier.predict(test_data_stop, as_iterable=True))
# test_pre = list(classifier.predict(predict_input_fn))
# test_predicted_classes = [p["classes"] for p in test_pre]
#
# # print("New Samples, Class Predictions: {}\n".format(test_predicted_classes))
# result = []
# for item in test_predicted_classes:
#     result.append(item)
#
# print("test prediction is\n", np.array(test_predicted_classes))
#
# print(result)
#
#
#
# print("test ground true is\n", test_labels_true_of_stop)



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

def model_train(X_train, X_test, y_train, y_test, save_model = False):
    feature_len = len(X_train.columns)

    feature_columns = [tf.contrib.layers.real_valued_column("x", dimension = feature_len)]

    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[100],
                                            n_classes=2,
                                            model_dir="../Model/DNN/Threeclass",
                                            dropout = 0.2,
                                            optimizer = tf.train.AdamOptimizer(1e-4))

    # classifier.fit(x=X_train, y=y_train, steps=8000)

    # Define the training inputs
    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_train)},
                                                        y=np.array(y_train),
                                                        num_epochs=None,
                                                        shuffle=True)
    # Train model.
    classifier.train(input_fn=train_input_fn, steps=2000)

    # export_dir = "../Model/DNN/test/"
    #
    # feature_spec = tf.feature_column.make_parse_example_spec(feature_columns)
    #
    # input_receiver_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
    #
    #
    # classifier.export_savedmodel(export_dir, input_receiver_fn, as_text=True)
    print("start evaluate")
    train_input_fn1 = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_train)},
                                                        y=np.array(y_train),
                                                        num_epochs=None,
                                                        shuffle=True)
    print("got input fn")
    train_accuracy_score = classifier.evaluate(train_input_fn1)['accuracy']

    print("\n ************************************train set Accuracy******************: {0:f}".format(train_accuracy_score))

    test_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_test)},
                                                       y=np.array(y_test),
                                                       num_epochs=1,
                                                       shuffle=False)

    test_accuracy_score = classifier.evaluate(test_input_fn)['accuracy']

    print("\n ************************************train set Accuracy******************: {0:f}".format(test_accuracy_score))

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_train, dtype=np.float32)},
                                                          num_epochs=1,
                                                          shuffle=False)

    # train_pre = list(classifier.predict(train_data_stop, as_iterable=True))
    train_pre = list(classifier.predict(predict_input_fn))
    train_predicted_classes = [p["classes"] for p in train_pre]
    print("train prediction is\n", np.array(train_predicted_classes))
    print("train ground true is\n", y_train)

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_test, dtype=np.float32)},
                                                          num_epochs=1,
                                                          shuffle=False)

    # train_pre = list(classifier.predict(train_data_stop, as_iterable=True))
    test_pre = list(classifier.predict(predict_input_fn))
    test_predicted_classes = [p["classes"] for p in test_pre]
    print("test prediction is\n", np.array(test_predicted_classes))
    print("test ground true is\n", y_test)

    return 0


def __main__():
    #data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'
    data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all.csv'

    df = pd.read_csv(data_dir)

    column_name = list(df.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    df_stop = df[df['scenario'] == 0]

    class_index = (df_stop['class'] != 0)
    df_stop.loc[class_index, 'class'] = 1

    labels_true_of_stop = np.array(df_stop['class']).astype(int)
    train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
    tf.gradients([x])


    X_train, X_test, y_train, y_test = train_test_split(train_data_stop, labels_true_of_stop, test_size=0.4)

    # model_name = 'all_sensor_rf_model_3class.sav'

    model = model_train(X_train, X_test, y_train, y_test, save_model = False)


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()