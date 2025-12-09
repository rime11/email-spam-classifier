import pandas as pd
import numpy as np
import datetime 

def combine_data(subject, message):
    '''
    Receives a subject and message
    subject is optional it can be left blank
    combines subject and message
    ===============
    returns a dataframe with new columns:
        'combined_with_stopwords, day_of_week, repeat_freq
    '''
    current_date = datetime.now()
    df = pd.DataFrame({
        'combined_with_stopwords': [f'{subject.strip()} {message.strip()}'],
        'day_of_week':[current_date.weekday()],#today's date 
        'repeat_freq': [1] #frequency is 1
    })