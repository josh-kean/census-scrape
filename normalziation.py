import os
import numpy as np
import pandas as pd
from matplotlib import pyplot
from sklearn import preprocessing

pd.options.display.max_columns = 10

#remove any duplicate columns
#columns = df.columns.drop_duplicates().tolist()
columns = ['B25126_041E', 'B25042_012E','B25042_009E','DP04_0089E']

#transformation: log, sqrt
#smoothing: weekly/monthly average, rolling average
#differencing: 

def select_columns(df, columns):
    return df[columns].astype(float)

def normalize_data(df):
    df.sort_index(inplace=True)
    return (df -df.mean())/(df.max() - df.min()) #enact this after replacing outlier data

def remove_outliers(df):
    df = normalize_data(df)
    for c in df.columns.values:
        std = df[c].std() #standard deviation of specific column
        df[c] = df[c].apply(lambda x: x if abs(x) < std else None)
        df[c].interpolate(inplace=True)
    return df

#plot cleaned up data
df.plot()
pyplot.show()
