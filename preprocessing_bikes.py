# import packages
import glob
import pandas as pd
import numpy as np

# define path names
path = 'data/bike'
csv_files = glob.glob(path + '/*.csv')

# create function to parse csv file and collapse data with groupby statement
def parse_file(f):
    df = pd.read_csv(f)
    df.rename(columns = {'Start date': 'startdate'}, inplace=True)
    df['startdate'] = pd.to_datetime(df['startdate'])
    df['dailydate'] = df['startdate'].dt.date
    df_date = df.groupby('dailydate')['startdate'].count().reset_index()
    df_date = df_date.rename({'dailydate': 'date', 'startdate': 'numbikes'}, axis=1)
    return df_date

# read all csv files, concatenate them, sort in ascending order by date
df_all = []
for f in csv_files:
    parsed_df = parse_file(f)
    df_all.append(parsed_df)
df_bike = pd.concat(df_all).reset_index(drop=True)
df_bike = df_bike.sort_values(by='date', ascending=True)
df_bike['date'] = pd.to_datetime(df_bike['date']) 
df_bike.reset_index(drop=True)

# create log(numbikes) variable
df_bike['log_numbikes'] = np.log(df_bike['numbikes'])

# save to csv file
df_bike.to_csv('data/dc-bikes-daily.csv', index=False)