# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 17:24:57 2016

@author: thomasqin
"""

import pandas as pd
import os
import json as js
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
len(products[products['perfect'] > 0]) == 2955

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
len(feature_matrix[0]) == 194
