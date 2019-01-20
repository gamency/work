from tsfresh import extract_features
import numpy as np
import pandas as pd
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features


data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Rss_clean_data_all_1.csv'

dataframe = pd.read_csv(data_dir)