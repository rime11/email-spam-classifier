from flask import Flask, request, render_template, jsonify 
import pandas as pd
import numpy as np
import joblib 
from datetime import datetime
import os

print('Starting app')
#initialize falsk app
app = Flask(__name__)

#load trained pipline, does it once when the app starts
print('Importing new pipline')
try:
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'spam_trained_model.joblib')
    pipeline = joblib.load(model_path)
    print('Pipeline imported successfully')
except Exception as e:
    pipeline = None
    print(f"Exact error:{type(e).__name__}:{e}\nCould not load the pipeline")


def process_user_input(subject, message):
    '''
    Receives subject and message from user input
    combines them into a dataframe with the same structure
    as the one used for training
    '''
    current_date = datetime.now()
    df = pd.DataFrame({
        'combined_with_stopwords': [f'{subject.strip()} {message.strip()}'],
        'day_of_week':[current_date.weekday()],#today's date 
        'repeat_freq': [1] #frequency is 1
    })
    return df

def convert_score_to_prob(pred):
    """
    Convert LinearSVC decision function to probabilities
    Args:
        pred (array): Decision function scores from LinearSVC
        Returns:
        array: probability of ham, probability of spam 
        """
    spam_prob = 1 / (1 + np.exp(-pred))
    return [1 - spam_prob, spam_prob] 

@app.route('/') #when the page is visited the flask app is run
def home():
    '''Home page with the form'''
    return render_template('index.html')

@app.route('/predict', methods=['Post']) #runs the prediction once submit is hit
def predict():
    '''Gets data from http form and Handles the prediction'''
    try:
        subject = request.form.get('subject','')
        message = request.form.get('message','')

        if not message:
            return jsonify({'error':'message cannot be empty'})
        
        #process user input
        precessed_input = process_user_input(subject, message)
        
        #make prediction
        result = (pipeline.predict(precessed_input))[0] #0 for spam
        predict_score = (pipeline.decision_function(precessed_input))[0]
        predict_proba = convert_score_to_prob(predict_score)

        prediction = "Spam" if result == 1 else "Not Spam"

        return jsonify(
            {'prediction':prediction,
             'Spam_probability':f'{round(predict_proba[1]*100,2)}', 
             'Ham_probability':f'{round(predict_proba[0]*100,2)}'
             }
        )
    except Exception as e:
        print('Error in route')
        return jsonify({'error':str(e)})
    
print('finished')

@app.route('/predict_api', methods=['Get','Post'])#localhost\predict_api
def predict_api():
    '''API endpoint for programmatic access'''
    try:    
        data = request.get_json()
        subject = data.get('subject','')
        message = data.get('message','')
        print('message received')
        if not message:
            return jsonify({'error':'message cannot be empty'})
        
        #process user input
        precessed_input = process_user_input(subject, message)
        
        #make prediction
        result = (pipeline.predict(precessed_input))[0] #0 for spam
        predict_score = (pipeline.decision_function(precessed_input))[0]
        predict_proba = convert_score_to_prob(predict_score)

        prediction = "Spam" if result == 1 else "Not Spam"

        return jsonify(
          
            {'Prediction':prediction,
             'Spam probability':predict_proba[1]*100,
             'Ham probability':predict_proba[0]*100
             }
             
        )
    except Exception as e:
        print('Error in route')
        return jsonify({'error':str(e)}) 
    
    
if __name__=='__main__':
    #app.run(debug=True)
    #port = int(os.environ.get('PORT', 5000)) #Elastic Beanstalk (and most cloud providers) inject a PORT environment variable when running. Locally, it defaults to 5000
    app.run(host = '0.0.0.0',port = 8080, debug=False) #allows access from outside the container (needed in EB).
    