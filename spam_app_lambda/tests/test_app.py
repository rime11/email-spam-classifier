#Tests that the app code behaves correctly on GitHub Actions 
#GitHub Actions runs it automatically on every push
'''
Does /predict_api return status 200?
Does the response JSON contain the keys Prediction, Spam probability, Ham probability?
Does an empty message return an error instead of crashing?
Do the two probabilities add up to 100?
'''

import pytest
import numpy as np
from unittest.mock import MagicMock, patch
 
 
# --- Mock the model before importing app ---
# This is necessary because app.py loads the model at startup.
# In GitHub Actions there is no model file, so we fake it.
mock_pipeline = MagicMock()
mock_pipeline.predict.return_value = np.array([1])          # 1 = Spam
mock_pipeline.decision_function.return_value = np.array([2.0])  # high score = confident spam
 
with patch("joblib.load", return_value=mock_pipeline):
    from app import app
 
 
# --- Test client setup ---
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
 
 
# ---------------------------------------------------------------
# HOME ROUTE
# ---------------------------------------------------------------
def test_home_page_loads(client):
    """Home page should return 200"""
    response = client.get("/")
    assert response.status_code == 200
 
 
# ---------------------------------------------------------------
# /predict  (form-based route used by the web UI)
# ---------------------------------------------------------------
def test_predict_spam(client):
    """Obvious spam email should be predicted as Spam"""
    mock_pipeline.predict.return_value = np.array([1])
    mock_pipeline.decision_function.return_value = np.array([2.0])
 
    response = client.post("/predict", data={
        "subject": "URGENT: You've Won $1,000,000!!!",
        "message": "Congratulations! Click here NOW to claim your prize!"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["prediction"] == "Spam"
    assert "Spam_probability" in data
    assert "Ham_probability" in data
 
 
def test_predict_ham(client):
    """Legitimate email should be predicted as Not Spam"""
    mock_pipeline.predict.return_value = np.array([0])
    mock_pipeline.decision_function.return_value = np.array([-2.0])
 
    response = client.post("/predict", data={
        "subject": "Meeting tomorrow at 3pm",
        "message": "Just confirming our project meeting in conference room B."
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["prediction"] == "Not Spam"
 
 
def test_predict_empty_message_returns_error(client):
    """Empty message should return an error"""
    response = client.post("/predict", data={
        "subject": "Hello",
        "message": ""
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
 
 
def test_predict_no_subject_still_works(client):
    """Missing subject should still work - subject is optional"""
    mock_pipeline.predict.return_value = np.array([0])
    mock_pipeline.decision_function.return_value = np.array([-1.0])
 
    response = client.post("/predict", data={
        "subject": "",
        "message": "Can we reschedule our meeting to next week?"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
 
 
# ---------------------------------------------------------------
# /predict_api  (JSON API route used by programmatic access)
# ---------------------------------------------------------------
def test_predict_api_spam(client):
    """API route should return Spam for obvious spam"""
    mock_pipeline.predict.return_value = np.array([1])
    mock_pipeline.decision_function.return_value = np.array([2.0])
 
    response = client.post("/predict_api", json={
        "subject": "Make $5000 per week working from home!",
        "message": "Amazing opportunity! No experience needed! Click here to start!"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["Prediction"] == "Spam"
    assert "Spam probability" in data
    assert "Ham probability" in data
 
 
def test_predict_api_ham(client):
    """API route should return Not Spam for legitimate email"""
    mock_pipeline.predict.return_value = np.array([0])
    mock_pipeline.decision_function.return_value = np.array([-2.0])
 
    response = client.post("/predict_api", json={
        "subject": "Weekend plans",
        "message": "Are we still on for dinner this Saturday at 7pm?"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["Prediction"] == "Not Spam"
 
 
def test_predict_api_empty_message_returns_error(client):
    """API route should return error when message is empty"""
    response = client.post("/predict_api", json={
        "subject": "Hello",
        "message": ""
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
 
 
def test_predict_api_probabilities_sum_to_100(client):
    """Spam and Ham probabilities should add up to ~100%"""
    mock_pipeline.predict.return_value = np.array([1])
    mock_pipeline.decision_function.return_value = np.array([1.0])
 
    response = client.post("/predict_api", json={
        "subject": "Free money",
        "message": "You have been selected for a cash prize!"
    })
    assert response.status_code == 200
    data = response.get_json()
    total = data["Spam probability"] + data["Ham probability"]
    assert abs(total - 100.0) < 0.01  # allow tiny floating point difference
 
 
def test_predict_api_no_subject(client):
    """API should work with missing subject"""
    mock_pipeline.predict.return_value = np.array([0])
    mock_pipeline.decision_function.return_value = np.array([-1.5])
 
    response = client.post("/predict_api", json={
        "subject": "",
        "message": "Please review the attached quarterly report."
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "Prediction" in data
 