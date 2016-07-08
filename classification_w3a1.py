# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 17:24:57 2016

@author: thomasqin
"""

import pandas as pd
import os
import json as js
import sklearn as sk
import sklearn.tree as st
import numpy as np

file_dir = os.path.dirname(os.path.abspath(__file__))

loans = pd.read_csv(str(file_dir)+'/lending-club-data.csv')


with open(str(file_dir)+'/module-5-assignment-1-train-idx.json') as data:
    train_idx = js.load(data)
    
with open(str(file_dir)+'/module-5-assignment-1-validation-idx.json') as data:
    validation_idx = js.load(data)

train_data = loans.iloc[train_idx]
validation_data = loans.iloc[validation_idx]

loans['safe_loans'] = loans['bad_loans'].apply(lambda x: +1 if x==1 else -1)

features = ['grade',                     # grade of the loan
            'sub_grade',                 # sub-grade of the loan
            'short_emp',                 # one year or less of employment
            'emp_length_num',            # number of years of employment
            'home_ownership',            # home_ownership status: own, mortgage or rent
            'dti',                       # debt to income ratio
            'purpose',                   # the purpose of the loan
            'term',                      # the term of the loan
            'last_delinq_none',          # has borrower had a delinquincy
            'last_major_derog_none',     # has borrower had 90 day or worse rating
            'revol_util',                # percent of available credit being used
            'total_rec_late_fee',        # total late fees received to day
           ]
target = 'safe_loans'

loans = loans[features + [target]]


def get_numpy_data(dataframe,features,label):
    dataframe['constant'] = 1
    features = ['constant'] + features
    features_frame = dataframe[features]
    feature_matrix = features_frame.as_matrix()
    label_sarray = dataframe[label]
    label_array = label_sarray.as_matrix()
    return (feature_matrix, label_array)

(loans_matrix, loans_labels) = get_numpy_data(loans,features,target)

decision_tree_model = st.DecisionTreeClassifier(max_depth = 6)
small_model = st.DecisionTreeClassifier(max_depth = 2)

