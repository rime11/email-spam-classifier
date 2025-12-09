from scipy.sparse import hstack
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def tfidf(data, best_param, model):
    data['Label'] = y
    X = data.drop(columns=['Label'], axis=1)

    preprocessor = ColumnTransformer([
                            #name, transformation, columns to transform
                            ('tfidf',TfidfVectorizer(max_features=best_param), 'combined_with_stopwords'),
                            #scale engineered features
                            ('scaled_features', StandardScaler(),['day_of_week', 'repeat_freq'])
                                ])
   

    pipeline = Pipeline([
                ('preprocessor',preprocessor),
                ('model',model)
            ])

    print("Fitting model to vectorized data")
    pipeline.fit(X,y)

    return pipeline, X,y

    
   


