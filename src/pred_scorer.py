from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, f1_score, recall_score, roc_auc_score

def evaluate_predictions(y_true, y_pred, scores_df, y_pred_proba=None):
    '''
    Takes true labels and predictions, returns scores using your scorer metrics
    '''
    scores = {}
    
    scores['test_F1'] = round(f1_score(y_true, y_pred, pos_label=1),4)
    scores['test_Precision'] = precision_score(y_true, y_pred)
    scores['test_Recall'] = recall_score(y_true, y_pred)
    scores['test_Recall_ham'] = recall_score(y_true, y_pred, pos_label=0)
    scores['test_Accuracy'] = accuracy_score(y_true, y_pred)
    scores = {k:round(v,4) for k,v in scores.items()}
    print(scores)
    # For AUC, you need probabilities
    if y_pred_proba is not None:
        scores['AUC'] = roc_auc_score(y_true, y_pred_proba[:, 1])  # probability of positive class
    else:
        scores['AUC'] = None

    #add all the scores to the scores df
    scores_df.loc['test_set']= scores
    
    return scores_df