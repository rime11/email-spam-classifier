import pandas as pd
import numpy as np


def clean_data(X, y):
    '''
    Receives original data
    drops nas and emails missing a subject
    drops duplicates
    changes data type of date to datetime
    ===============
    returns cleaned data
    '''
    #combine X and y
    X['Label'] = y['Spam/Ham'].str.strip()
    X['Label'] = X['Label'].map({'ham':0,'spam':1})
    
    #drop emails missing subject and message
    X = X.dropna(subset=['Subject','Message'], how='all')
    #drop emails missing a message
    X = X.dropna(subset=['Message'], how='all')
    #fill emails with missing subject with the words 'no subject'
    X['Subject'] = X['Subject'].fillna('[no subject]')
    #drop duplicates
    X = X.drop_duplicates(subset=['Subject','Message','Date'],keep='first')
    #change date type
    X['Date'] = pd.to_datetime(X['Date'])

    #For y: rename column spam/ham to label
    y= X['Label']
    X = X.drop(columns=['Label'],axis=1)
   
    #make sure that the label does not have extra spaces by using strip
    #y['Label'] = y['Label'].str.strip()
    #ham is 0 and spam is 1
    #y = y['Label'].map({'ham':0,'spam':1})
    
    return X, y

def add_new_features(X):
    '''
    received cleaned data
    adds day_of_week and 
    frequency features
    '''
    #add day of the week
    X['day_of_week'] = X['Date'].dt.dayofweek
    #add repeat frequency
    X['repeat_freq'] =  X.groupby(['Subject', 'Message'])['Message'].transform('count')
    
    return X

def combine_data(X):
    '''
    Adds a new columns to the data where
    the message and subject are combined'''
    X['combined_with_stopwords'] = X['Subject']+' '+X['Message']
    
    return X