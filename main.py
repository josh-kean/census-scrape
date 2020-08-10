import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression

current_location = os.getcwd()
group_data = os.path.join(current_location, 'counties')

df = pd.read_pickle(os.path.join(group_data,'09_015.pickle'))

'''
B25126_041E,int,Estimate!!Total!!Renter occupied!!Householder 15 to 34 years!!Built 1990 to 1999,B25126
B25042_012E,int,Estimate!!Total!!Renter occupied!!2 bedrooms,B25042
B25042_009E,int,Estimate!!Total!!Renter occupied,B25042
DP04_0089E,int,Estimate!!VALUE!!Owner-occupied units!!Median (dollars),DP04
DP03_0004E,int,Estimate!!EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Employed,DP03
'''

years = df.index.values
columns = ['B25126_041E', 'B25042_012E','B25042_009E','DP04_0089E']

new_df = df[columns]
new_df = pd.to_datetime(df)
print(new_df)
