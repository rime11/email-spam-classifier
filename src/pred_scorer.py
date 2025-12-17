from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, f1_score, recall_score, roc_auc_score

def evaluate_predictions(scores_df, y_true, y_pred, pred_proba=[],pred_decision = []):
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
    
    if len(pred_proba) == 0 and len(pred_decision) > 0:
        scores['test_AUC'] = roc_auc_score(y_true, pred_decision)
    elif len(pred_decision) == 0 and len(pred_proba) >0:
        scores['test_AUC'] = roc_auc_score(y_true, pred_proba[:, 1])
    else:
        print("To calculate AUC probabilities are needed")

        
    #print(scores)
  
    #add all the scores to the scores df
    scores_df.loc['test_set']= scores
   
    return scores_df