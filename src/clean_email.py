import string
stop_words = set(stopwords.words('english'))  

def clean_text(email):
    '''
    parameters: an email
    
    function removes:
    Lowercase
    Tokenize
    Remove stopwords (and punctuation)
    returns: string of emails
   
    '''
    #remove punctuations
    no_punc_text =  ''.join([ch for ch in email.lower() if ch not in set(string.punctuation)])

    #tokenize text returns a list of tokens
    tokens = word_tokenize(no_punc_text)
    
    #remove stop words
    new_text = ' '.join([word for word in tokens if word not in stop_words])# returns a series
    
    return new_text 