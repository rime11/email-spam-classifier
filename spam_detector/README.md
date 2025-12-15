# Spam Detector Web Application

A Flask web application for real-time email spam classification using machine learning.

![Spam Detector Web Interface ](../assets/screenshot_flask_app.png)

**Note:** This application is currently deployed on AWS Lambda as a serverless API. See the `spam_app_lambda/` folder for deployment documentation. This Elastic Beanstalk setup achieved the same functionality but at significantly higher cost.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Run application](#run-application)
- [Testing](#testing)
- [AWS Elastic Beanstalk Deployment](#aws-elastic-beanstalk-deployment)
- [Troubleshooting](#troubleshooting)

## Overview
This application provides a web interface for classifying emails as spam or legitimate (ham) using a pre-trained LinearSVC model. Deployed on AWS Elastic Beanstalk, this documentation covers the EB deployment process.

**Note:** A cost-optimized serverless version using AWS Lambda is available in the spam_app_lambda/ folder. The Elastic Beanstalk setup documented here achieves the same functionality but at higher cost (~$54/month vs $0-2/month for Lambda).

## Features

- Real-time spam classification with 99.44% accuracy
- Confidence scores via decision function
- Clean, responsive web interface
- Input validation and error handling
- Pre-trained model included 
- Comprehensive test suite
- Example emails for testing

## Prerequisites

- Python 3.10 or higher
- AWS account (for deployment)
- AWS CLI configured with credentials (for deployment)
- Virtual environment tool (conda or venv recommended)

## Project Structure
```
spam_detector/
    ├── .ebextensions/                       #AWS EB configuration
    |    └── python.config
    ├──.elasticbeanstalk/                   # EB CLI settings (auto-generated)           
    ├── README.md                           # Deployment instructions  
    ├── app.py                              # Main Flask application
    ├── application.py                      # File that runs the Flask server  
    ├── requirements.txt                    # Flask dependencies  
    ├── models/
          └── spam_trained_model.joblib     # The trained model (4.4MB)
    ├── templates/
    |   ├──base.html             
    │   └── index.html                      # Main web interface
    └── static/
    |    ├── css/
    |        └── style.css
    └──tests\                               # App testing suite 
        ├──spmaDetectorTester.py
        └──results_dataframe.csv
```
**Note:** `application.py` is required by AWS Elastic Beanstalk.

## Dependencies
```
pandas==2.2.3
scikit-learn==1.6.1
joblib==1.4.2
numpy==2.2.4
flask
gunicorn # For the AWS Elastic beanstalk deployment
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/rime11/spam_detector.git
cd spam_detector
```
### 2. Set Up Environment

**Option A: Using Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate spam_detector_env
```
**Option B: Using pip**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Verify Installation
```bash
# Confirm model file exists
ls models/spam_trained_model.joblib
```
### Environment Setup

This project was developed using Conda. You can recreate the environment using either conda or pip method:

### Option 1: Using Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate spam_detector_env
```

### Option 2: Using pip
```bash
python -m venv venv
source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt
```

## Run application
```bash
python app.py
```

### 3. Verify Installation
```bash
# Confirm model file exists
ls models/spam_trained_model.joblib
```
## Running Locally
```bash
python app.py
```
Visit: `http://localhost:5000` or whatever you setup your port at in the app.py file

## API Endpoints

### POST `/predict`

Classify an email as spam or ham.

**Request Body:**
```json
{
  "subject": "Meeting tomorrow",
  "message": "Hi, are we still on for the meeting tomorrow at 2pm?"
}
```

**Response:**
```json
{
  "prediction": "ham",
  "Spam Probability": "40.25%",
  "Ham Probability": "59.75%"
}
```
## Testing

The project includes a comprehensive testing suite (`tests/test_spam_detector.py`) that validates the Flask API's performance across multiple scenarios including obvious spam, legitimate emails, phishing attempts, marketing content, edge cases, and error handling.

**Test Categories:**
- Obvious spam emails (prize scams, work-from-home schemes)
- Legitimate emails (meetings, personal communication)
- Phishing attempts (fake PayPal, IRS, Amazon notifications)
- Marketing emails (newsletters, promotional content)
- Edge cases (empty subjects, very long messages)
- Error handling (malformed requests, invalid JSON)

### Running Tests
```bash
# Terminal 1
python app.py

# Terminal 2
cd tests
python test_spam_detector.py
```
**Test Output:**
```
Total Tests: 20  
Successful: 19  
Failed Tests: 1  
Accuracy: 71.43% (10/14 correct classifications)  
```

**Results saved to:** `results_dataframe.csv` with the following columns:
- email subject	
- status	
- expected prediction	
- Prediction	
- correctly_predicted	
- Ham probability	
- Spam probability	
- confidence	
- response time	
- error	expected

## AWS Elastic Beanstalk Deployment
Understanding AWS EB Architecture
```
Application: spam-detector-app
├── Environment: spam-test-env (development/testing)
│   ├── EC2 instances
│   ├── Load balancer
│   └── Logs and monitoring
│
└── Environment: spam-detector-env (production)
    ├── EC2 instances
    ├── Load balancer
    └── Logs and monitoring
```
**Prerequisites:**
- AWS account
- AWS CLI configured with credentials

## Deployment Steps
### 1. Install EB CLI
```bash
pip install --upgrade awsebcli
```
### 2. Install AWS CLI (Optional but Recommended)
The AWS CLI enables broader AWS interactions for credential configuration and service management:
```bash 
pip install --upgrade awscli
```
### 3. Initialize Application
```bash
# Initialize EB application
eb init -p python-3.10 spam-detector-app --region <ENTER_YOUR_REGION>
```
### 4. Create Environment
```bash
# Create and deploy to new environment
eb create spam-detector-env
```
### 5. Deploy Application
```bash
# Deploy current version
eb deploy

# Open application in browser
eb open
```
### Updating After Changes
```bash
eb deploy
```
**Note:** This application has been deployed using two AWS architectures:


**AWS Console Reference**

![aws console](../assets/aws_interface.png)

## Troubleshooting
### Model file not found

**Issue:** Application cannot locate the trained model file.  

**Solution:** 

```bash
# Verify model exists
ls models/spam_trained_model.joblib

# If missing, re-clone the repository
git clone https://github.com/rime11/spam-detector.git
```  

### Port Already in Use
**Issue:** Cannot start Flask application due to port conflict. 

**Solution:** 
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```
### ModuleNotFoundError
**Issue:** ModuleNotFoundError when starting application.

**Solution:** 
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## EB Deployment Failures
**Issue:** Deployment fails or environment health is degraded.  

**Solutions:**  
* Check EB logs: **eb logs**  
* Verify application.py exists and is configured correctly  
* Ensure all dependencies are in requirements.txt  
* Confirm Python version matches EB platform (3.10)

## Cost Considerations
AWS Elastic Beanstalk deployment incurs the following approximate costs:

* EC2 instance: ~$40-50/month
* Load balancer: ~$15-20/month
* Total: ~$54/month

For a cost-effective alternative, see Lambda deployment in [the lambda deployment folder](/spam_app_lambda/) which runs for $0-2/month.

##  License

MIT License - see [../LICENSE](../LICENSE)

