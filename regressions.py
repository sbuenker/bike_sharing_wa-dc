# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, RidgeCV, PoissonRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from statsmodels.tsa.stattools import adfuller
from sys import argv

# read data
bikes = pd.read_csv('data/finaldata.csv')

# define list of features for regression analysis
calendar_features = [f'dow_{i+1}' for i in range(0,6)] + \
                    [f'month_{i+1}' for i in range(1,12)] + \
                    [f'year_{i+1}' for i in range(2011,2018)] + \
                    ['sin_doy', 'cos_doy', 'sin_dow', 'cos_dow', 'holiday']
weather_features = ['awnd_log', 'prcp_log', 'snow_log',	'snwd_log', 'tmax', 'tmin']
all_features = [*calendar_features, *weather_features]

# define function to train/test model and produce error analysis
def reg_predict(
    df,
    features,
    train_year_end = 2018, # training year from 2011 up until year specified here
    test_year = 2019, # test year must be after train_year_end, must be between 2011 and 2019
    model = 'Linear', # choice of 'Linear', 'Polynomial', 'Ridge', 'Poisson'
    scaling = True, # default scaling (standardization) of x variables
    logbikes = False, # default y variable is not log transformed
    degree = 2, # quadratic polynomial is default for polynomial and ridge regression
    alphas = [0.01,0.1,1,10,100], # regularization grid for ridge regression
    n_estimators = 550, # number of estimators for xgboost regression
    max_features = 'sqrt' # maximum number of features for random forest
):

    ### regression analysis ###

    # define train/test years
    df_train = df[df['year'] <= train_year_end]
    df_test = df[df['year'] == test_year]

    # define X, y for train/test sample
    X_train = df_train[features]
    X_test = df_test[features]
    y_train = df_train['numbikes']
    y_test = df_test['numbikes']

    # scaling standardization for features
    if scaling:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    
    # log choice for number of bikes
    if logbikes:
        y_train = np.log(y_train)
        y_test = np.log(y_test)
    
    # choice for regression models
    if model == 'Linear':
        regr = LinearRegression()
    elif model == 'Polynomial':
        regr = make_pipeline(
            PolynomialFeatures(degree=degree),
            LinearRegression()
            )
    elif model == 'Ridge':
        regr = make_pipeline(
            PolynomialFeatures(degree=degree),
            RidgeCV(alphas=alphas)
            )
    elif model == 'Poisson':
        regr = PoissonRegressor()
    elif model == 'XGBoost':
        regr = XGBRegressor(n_estimators=n_estimators)
    elif model == 'Random Forest':
        regr = RandomForestRegressor(n_estimators=n_estimators, max_features=max_features)
    else:
        assert False, f'Unknown model {model}'
    
    # fitting and prediction
    regr.fit(X_train, y_train)
    y_pred_train = regr.predict(X_train)
    y_pred = regr.predict(X_test)

    # print mape for train/test of model
    print('----------------------------------')
    print(f'{model} regression')
    print(f'Training Period: 2011-{train_year_end}')
    print(f'Test Period: {test_year}')
    print('----------------------------------')
    print(f'Train MAPE: {mean_absolute_percentage_error(y_train, y_pred_train).round(3)}')
    print(f'Test MAPE: {mean_absolute_percentage_error(y_test, y_pred).round(3)}')
    print('----------------------------------')

    ### residuals analysis ###

    # define residuals and subplots
    residuals_test = y_test - y_pred
    fig, ax = plt.subplots(1, 2, figsize=(12,4))
    fig.suptitle(f'Residual Analysis: Test Period {test_year}', fontsize=12)

    # plot distribution of residuals
    plot_0 = sns.histplot(residuals_test, ax=ax[0], color='Blue')
    plot_0.grid(False)
    ax[0].set_xlabel('Residuals', fontsize=10)
    ax[0].set_ylabel('')
    
    # plot residuals vs predicted
    plot_1 = sns.scatterplot(x=y_pred, y=residuals_test, ax=ax[1], color='Blue')
    plot_1.grid(False)
    ax[1].set_xlabel('Predicted', fontsize=10)
    ax[1].set_ylabel('Residual', fontsize=10)
    plt.show()

    # augmented dickey-fuller test for stationarity of residuals #
    print('ADF Test for Residual Stationarity')
    result = adfuller(residuals_test)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
	    print('\t%s: %.3f' % (key, value))
    print('----------------------------------')

# baseline model 
reg_predict(df=bikes, features=calendar_features)