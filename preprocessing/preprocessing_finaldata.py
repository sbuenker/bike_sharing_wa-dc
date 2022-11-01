# import packages
import calendar
import holidays
import pandas as pd
import numpy as np

# import bikes and weather data
bikes = pd.read_csv('data/dc-bikes-daily.csv', parse_dates=["date"])
weather = pd.read_csv('data/weather_dc_historic.csv', parse_dates=["DATE"])

# add day, week, month, year features to bike data
bikes['year'] = bikes['date'].dt.year
bikes['month'] = bikes['date'].dt.month
bikes['week'] = bikes['date'].dt.isocalendar().week
bikes['day'] = bikes['date'].dt.day
bikes['dayofweek'] = bikes['date'].dt.dayofweek
bikes['dayofyear'] = bikes['date'].dt.dayofyear

# add calendar features
us_holidays = holidays.US()
def add_calendar_features(df):
    df_new = df.copy()
    days_in_year = np.where(df['year'].apply(lambda y: calendar.isleap(y)), 366, 365)
    df_new['sin_doy'] = np.sin(2*np.pi*df_new['dayofyear']/days_in_year)
    df_new['cos_doy'] = np.cos(2*np.pi*df_new['dayofyear']/days_in_year)
    df_new['sin_dow'] = np.sin(2*np.pi*df_new['dayofweek']/7)
    df_new['cos_dow'] = np.cos(2*np.pi*df_new['dayofweek']/7)
    df_new = pd.concat([df_new, pd.get_dummies(df_new['dayofweek'], 'dow', drop_first=True)], axis=1)
    df_new = pd.concat([df_new, pd.get_dummies(df_new['year'], 'year', drop_first=True)], axis=1)
    df_new = pd.concat([df_new, pd.get_dummies(df_new['month'], 'month', drop_first=True)], axis=1)
    df_new = pd.concat([df_new, pd.get_dummies(df_new['day'], 'day', drop_first=True)], axis=1)
    df_new['holiday'] = [1 if d in us_holidays else 0 for d in df_new['date']]
    return df_new
bikes = add_calendar_features(bikes)

# rename columns and drop unnecessary colums data
weather.columns = weather.columns.str.lower()
weather.drop(columns=['station',
                      'name', 
                      'latitude', 
                      'longitude', 
                      'elevation', 
                      'awnd_attributes', 
                      'prcp_attributes',
                      'snow_attributes', 
                      'snwd_attributes', 
                      'tavg', 
                      'tavg_attributes', 
                      'tmax_attributes', 
                      'tmin_attributes'
                      ], axis=1, inplace=True)

# missing values encoded as 9999; encode as NaN
weather.fillna({9999: np.nan})

# define log variables for awnd, prcp, snow, snwd, since they are positively skewed
weather["awnd_log"] = np.log(1 + weather["awnd"])
weather["prcp_log"] = np.log(1 + weather["prcp"])
weather["snow_log"] = np.log(1 + weather["snow"])
weather["snwd_log"] = np.log(1 + weather["snwd"])

# merge bikes and weather 
df = pd.merge(left=bikes, right=weather, how='inner', on='date')

# save to csv file
df.to_csv('data/finaldata.csv', index=False)