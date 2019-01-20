import tensorflow as tf
import numpy as np
import pandas as pd
from Xengine import DatanFeaturelizaiton



data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv'
train_df = pd.read_csv(data_dir)

df_station = train_df[train_df['scenario'] == 0]

class_index = (df_station['class'] != 0)
df_station.loc[class_index, 'class'] = 1

train_label_ground_true = df_station['class']

train_data = df_station.iloc[:, 0:scenario_column_number]



raw_data = True
if raw_data == True:
    base_dir = '/Users/kite/Desktop/human-machine-detect/Data'
    df = base_dir + '/short_behavior_test_data'
else:
    # data_dir = './Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv'
    data_dir = '/Users/kite/Desktop/human-machine-detect/output.csv'
    df = pd.read_csv(data_dir)

Feat_Rss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data, predicting = True)

df_station_te = Feat_Rss_clean_test_data_df[Feat_Rss_clean_test_data_df['scenario'] == 0]

class_index = (df_station_te['class'] != 0)
df_station_te.loc[class_index, 'class'] = 1

test_label_ground_true = df_station_te['class']

test_data = df_station_te.iloc[:, 0:scenario_column_number]



in_units = 40
h1_units = 100
# h2_units = 20
# h3_units = 20
# h4_units = 20
# h5_units = 20



W1 = tf.Variable(tf.truncated_normal([in_units, h1_units], stddev=0.1))
b1 = tf.Variable(tf.zeros([h1_units]))

# W2 = tf.Variable(tf.zeros([h1_units, h2_units]))
# b2 = tf.Variable(tf.zeros([h2_units]))

# W3 = tf.Variable(tf.zeros([h2_units, h3_units]))
# b3 = tf.Variable(tf.zeros([h3_units]))
#
# W4 = tf.Variable(tf.zeros([h3_units, h4_units]))
# b4 = tf.Variable(tf.zeros([h4_units]))


W5 = tf.Variable(tf.zeros([h5_units, 2]))
b5 = tf.Variable(tf.zeros([2]))


x = tf.placeholder(tf.float32, [None, in_units])
keep_prob = tf.placeholder(tf.float32)

hidden1 = tf.nn.relu(tf.matmul(x, W1) + b1)
#h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)


hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

hidden2 = tf.nn.relu(tf.matmul(hidden1_drop, W2) + b2)
hidden2_drop = tf.nn.dropout(hidden2, keep_prob)

#hidden3 = tf.nn.relu(tf.matmul(hidden2_drop, W3) + b3)
#hidden3_drop = tf.nn.dropout(hidden3, keep_prob)

#hidden4 = tf.nn.relu(tf.matmul(hidden3_drop, W4) + b4)
#hidden4_drop = tf.nn.dropout(hidden4, keep_prob)

y = tf.nn.softmax(tf.matmul(hidden2_drop, W5) + b5)

y_ = tf.placeholder(tf.float32, [None, 3])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
#train_step = tf.train.AdagradOptimizer(0.01).minimize(cross_entropy)
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)


correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
#correct_prediction = tf.equal(y, y_)


accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))