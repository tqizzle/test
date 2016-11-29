# -*- coding: utf-8 -*-

"""
Created on Thu Jun 30 17:24:57 2016
@author: thomasqin
"""

import pandas as pd
import os
import json as js
import numpy as np
file_dir = os.path.dirname(os.path.abspath(__file__))

products = pd.read_csv(str(file_dir)+'/amazon_baby_subset.csv')
products = products.fillna({'review':''})

with open(str(file_dir)+'/important_words.json') as data:
    important_words = js.load(data)
    
def remove_punctuation(text):
    import string
    return text.translate(None, string.punctuation)
    
products['review_clean'] = products['review'].apply(remove_punctuation)

for word in important_words:
    products[word] = products['review_clean'].apply(lambda s: s.split().count(word))

#how many product reviews have the word perfect?
#len(products[products['perfect'] > 0]) == 2955

def get_numpy_data(dataframe,features,label):
    dataframe['constant'] = 1
    features = ['constant'] + features
    features_frame = dataframe[features]
    feature_matrix = features_frame.as_matrix()
    label_sarray = dataframe[label]
    label_array = label_sarray.as_matrix()
    return (feature_matrix, label_array)
    
(feature_matrix,sentiment) = get_numpy_data(products,important_words,'sentiment')

#how many features are in feature_matrix?
#len(feature_matrix[0]) == 194

def predict_probability(feature_matrix, coefficients):

    import math
    score = np.dot(feature_matrix,coefficients)
    predictions = 1/(1 + np.exp(-score))
    return predictions
    
def feature_derivative(errors, feature):
    derivative = np.dot(errors,feature)
    return derivative
    
def compute_log_likelihood(feature_matrix, sentiment, coefficients):
    indicator = (sentiment==+1)
    scores = np.dot(feature_matrix, coefficients)
    lp = np.sum((indicator-1)*scores - np.log(1. + np.exp(-scores)))
    return lp
    
def logistic_regression(feature_matrix,sentiment,initial_coefficients,step_size,max_iter):
    coefficients = np.array(initial_coefficients)
    for itr in range(max_iter):
        predictions = predict_probability(feature_matrix,coefficients)
        indicator = (sentiment==+1)
        errors = indicator - predictions
        for j in xrange(len(coefficients)):
            derivative = feature_derivative(errors, feature_matrix[:,j])
            coefficients[j] = coefficients[j] + step_size * derivative
        
        if itr <= 15 or (itr <= 100 and itr % 10 == 0) or (itr <= 1000 and itr % 100 == 0) \
        or (itr <= 10000 and itr % 1000 == 0) or itr % 10000 == 0:
            lp = compute_log_likelihood(feature_matrix, sentiment, coefficients)
            print 'iteration %*d: log likelihood of observed labels = %.8f' % \
                (int(np.ceil(np.log10(max_iter))), itr, lp)
    return coefficients
            
initial_coefficients = np.zeros(194)
step_size = 1e-7
max_iter = 301


coefficients = logistic_regression(feature_matrix,sentiment,initial_coefficients,step_size,max_iter)
#is log likelihood increasing or decreasing?  increasing

scores = np.dot(feature_matrix,coefficients)
positive = [x for x in scores if x > 0]

#how many reviews have positive sentiment?
len(positive) = 25126


#what is the accuracy of the prediction?
actual = len(products[products['sentiment'] == 1])
=26579
25126 / float(26579)

or

25126 / 53072
accuracy = []
for i in xrange(len(scores)):
    if scores[i] * products['sentiment'][0] > 0:
        accuracy.append(1)
    else:
        accuracy.append(0)




coefficients = list(coefficients[1:])
word_coefficient_tuples = [(word, coefficient) for word, coefficient in zip(important_words, coefficients)]
word_coefficient_tuples = sorted(word_coefficient_tuples, key = lambda x:x[1], reverse = True)

#what word is not in the top 10 most positive words?
word_coefficient_tuples[:10]
cheap

#what word is not in the top 10 most negative words?
