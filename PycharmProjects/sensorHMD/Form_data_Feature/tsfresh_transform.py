from tsfresh import extract_features
import numpy as np
import pandas as pd
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features

data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Rss_clean_data_all_1.csv'

dataframe = pd.read_csv(data_dir)


index = list(range(0,41))

timeseries_df = dataframe.iloc[:, index]

timeseries = timeseries_df.iloc[:,[1,2,3,9,10,11,-4]]

class_lable = []
for index in np.unique(timeseries_df.id):
    class_lable.append(timeseries_df.loc[index * 50, 'class'])
    #print(index)

class_lable = np.array(class_lable)

extracted_features = extract_features(timeseries, column_id="id")



#extracted_features = extract_features(timeseries, column_id="id", column_sort="time")

#impute(extracted_features)
#features_filtered = select_features(extracted_features, y)