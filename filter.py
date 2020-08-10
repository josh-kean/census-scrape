import os
import numpy as np
import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.stattools import grangercausalitytests as grainger
import _thread as thread
import time

current_dir = os.getcwd()
med_house_value = 'DP04_0089E'
pd.set_option('use_inf_as_na', True)
threads = []

def get_pickles():
    counties = []
    for (_, _, c) in os.walk(os.path.join(current_dir, 'counties')):
        counties.extend(c)
    return counties

def open_pickle(v):
    metrics = {}
    for c in get_pickles():
        df = pd.read_pickle(os.path.join(current_dir, 'counties', c)) #open dataframe
        name = f'{df["NAME"].values[0][0]}'
        df = df[v]
        if len(df.values) < 8: continue
        df.replace('0', np.nan, inplace=True)
        df = df.astype('float64')
        df.sort_index(inplace=True)
        df = df.interpolate(limit=8, limit_direction='both')
        metrics[c] = [name, *df.values]
        print(metrics[c])
    values = pd.DataFrame(metrics).T
    #values.columns = [name, *[str(x) for x in range(2011, 2019)]]
    values.to_csv(f'{v}.csv')

def open_and_clean_pickle(c):
    #open dataframe
    df = pd.read_pickle(os.path.join(current_dir, 'counties', c))
    #remove duplicate cells
    df = df.T.drop_duplicates().T
    df_names = df[['NAME', 'state', 'county']]
    df = df.drop(['NAME', 'state', 'county'], axis=1)
    return df_names, df

def normalize_data(df):
    df = (df - df.mean())/(df.max() - df.min())
    return df

def granger_test(df, pickle):
    #dickey fuller test
    df.sort_index(inplace=True)
    df = df.replace('0',np.nan)
    df.dropna(axis=1, thresh=3, inplace=True) #get rid of any row with 4 or more NA's
    df = df.astype('float64')
    df = df.interpolate(limit=8, limit_direction='both')
    granger_variables = []
    start = time.time()
    for col in [x for x in df.columns.values if 'PE' not in x]:
        if df[col].nunique() > 4: #require at least 4 unique values
            temp_df = df[[med_house_value,col]].pct_change()
            temp_df = temp_df.interpolate(limit=8, limit_direction='both')
            result = grainger(temp_df, maxlag = 1, verbose=False) #result gives dict 
            res = result[1][0]['ssr_ftest']
            if res[0] > res[1]: 
                granger_variables.append([col, res[0]-res[1]])
        else:
            pass
    print(f'granger filter {time.time() - start}')
    gvdf = pd.DataFrame({c:granger_variables})
    start = time.time()
    gvdf.to_pickle(os.path.join(current_dir, 'data', pickle))
    print(f'save time {time.time() - start}')
    print('removed pickle from buffer')

if __name__ == '__main__':
    open_pickle('B07009_006E')
