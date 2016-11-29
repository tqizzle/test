import pandas as pd
import math
from sklearn import linear_model
import numpy as np

train_csv = pd.read_csv('/Users/thomasqin/Downloads/kc_house_train_data.csv')
test_csv = pd.read_csv('/Users/thomasqin/Downloads/kc_house_test_data.csv') 
def logs(x):
    return math.log(x)


def add_columns(frame):
    frame['bedrooms_squared'] = frame['bedrooms'] * frame['bedrooms']
    frame['bed_bath_rooms'] = frame['bedrooms'] * frame['bathrooms']
    frame['log_sqft_living'] = frame['sqft_living'].apply(logs)
    frame['lat_plus_long'] = frame['lat'] + frame['long']
    return frame

train_col = add_columns(train_csv)
test_col = add_columns(test_csv)

train_data = np.array(train_col)
test_data = np.array(test_col)

x1 = test_data[:,[3,4,5,17,18]]
x2 = test_data[:,[3,4,5,17,18,21]]
x3 = test_data[:,[3,4,5,17,18,21,22,23,24]]
y = test_data[:,2]

regr1 = linear_model.LinearRegression()
regr1.fit(x1,y)
regr2 = linear_model.LinearRegression()
regr2.fit(x2,y)
regr3 = linear_model.LinearRegression()
regr3.fit(x3,y)

def rss(x,z):
    return np.mean((x-z)**2)
    
print str(rss(regr1.predict(x1),y)) +  ' is the RSS of model 1'
print str(rss(regr2.predict(x2),y)) +  ' is the RSS of model 2'
print str(rss(regr3.predict(x3),y)) +  ' is the RSS of model 3'


