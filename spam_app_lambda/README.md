# AWS Lambda Deployment Guide
[![Live Demo](https://img.shields.io/badge/Live%20Demo-AWS%20Lambda-orange)](https://ohw3i64ker6qr3sablgjbszvhi0rxntm.lambda-url.us-west-1.on.aws/)

This application runs on AWS Lambda using **Docker containers** and **the Lambda Web Adapter** providing a serverless and cost-effective alternative to traditional hosting. It uses the same Flask and Gunicorn setup used on Elastic Beanstalk, with no Lambda-specific code changes needed.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Key Components](#key-components)
- [Why Lambda with Docker](#why-lambda-with-docker)
- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
- [Configuration](#configuration)
- [Testing](#testing)
- [Updating the Application](#Updating_the_Application)
- [Useful Commands](#Useful_Commands)

### Architecture Overview 
```
User → API Gateway → Lambda → [Web Adapter] → Gunicorn:8080 → Flask → Response
```
**Request Flow:**
1. User sends a request to the API Gateway endpoint (e.g., `https://your-api-url.com/predict`)
2. API Gateway triggers Lambda with an event
3. Lambda Web Adapter extension intercepts the event
4. Adapter converts the Lambda event to an HTTP request
5. Request is forwarded to Gunicorn running on port 8080
6. Gunicorn passes it to Flask, which processes and returns a response
7. Response flows back: Flask → Gunicorn → Adapter → Lambda → API Gateway → User

### Key Components:
**Lambda Web Adapter**  
Intercepts Lambda events and converts them to standard HTTP requests enabling:

- No code changes from elastic beanstalk setup: Same Flask and Gunicorn 
- Use familiar WSGI (Web Server Gateway Interface) patterns without Lambda-specific handlers
- Serverless scaling Automatic scaling with pay-per-request pricing  

**Gunicorn**   
Production grade WSGI server that provides:
- Multiple workers for concurrent request handling, 
- Automatic crash recovery, and production-grade performance.
- Seurity strengthening   

### Why Gunicorn?

Flask's built-in development server is not production-ready, meaning it is:
- **Single-threaded**: can only handle one request at a time
- **No process management**: if it crashes, it stays crashed
- **Poor performance**: not optimized for production traffic
- **Security concerns**: missing production strengthening

### Why Lambda with Docker
AWS Lambda supports two deployment methods:
- ZIP file: Up to 50 MB compressed, 250 MB uncompressed
- Container image: Up to 10 GB

This project uses container deployment because machine learning dependencies (scikit-learn, numpy, pandas) exceed ZIP file size limits. Docker also provides:
- Better dependency management
- Reproducible builds
- Easier local testing
- Version control for the entire runtime environment

### Cost Comparison between Elastic Beanstalk and Lambda:  

| Service | Monthly Cost  | Scaling |
| :------- | :------ | :------- |
| Elastic Beanstalk | ~$54/month   |  Manual, always running  |
|| EC2 t2.micro~$8| 
|| Load Balancer: ~$15 |
|| Data transfer: ~$2-5|
|| Runs 24/7 even with no traffic |
| Lambda Docker |  First 1M requests/month: FREE | pay-per-request  |
||  $0.20 per 1M requests|
||  $0.0000166667 per GB-second |
|| Only pay when app is used|
________________  


Example calculation for a portfolio project:

- 1,000 requests/month
- 500 MB memory allocation
- Average 2-second execution time

**Cost:** Essentially $0 (well within free tier)
Compare this to Elastic Beanstalk's fixed $54/month regardless of usage.


## Prerequisites
Before deploying, ensure you have:

1. AWS CLI installed and configured:

```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, region, and output format
```
2. Docker installed locally
3. IAM Permissions: 
   - the AWS user needs **AWSLambda_FullAccess** (for Lambda function creation)
4. AWS Account ID, you find yours with:
```bash  
aws sts get-caller-identity --query Account --output text
#or just 
aws sts get-caller-identity
```

## Deployment Steps

### 1. Create Dockerfile:  
Create a file named `Dockerfile` in your project root (same directory as app.py) 

```dockerfile
# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.10

# Copy Lambda Web Adapter from public AWS image
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py ${LAMBDA_TASK_ROOT}/
COPY templates/ ${LAMBDA_TASK_ROOT}/templates/
COPY static/ ${LAMBDA_TASK_ROOT}/static/
COPY models/ ${LAMBDA_TASK_ROOT}/models/

WORKDIR ${LAMBDA_TASK_ROOT}

# Set environment variables for the adapter
ENV PORT=8080
ENV AWS_LWA_INVOKE_MODE=buffered

# Override the Lambda entrypoint
ENTRYPOINT []

# Run Gunicorn (production-ready WSGI server)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```
### 2. Create ECR Repository
AWS Elastic Container Registry (ECR) stores your Docker images:
```bash
aws ecr create-repository --repository-name spam-detector --region <YOUR_REGION>
#Replace <YOUR_REGION> with your actual AWS region
```
### 3. Build Docker Image locally
```bash 
docker build -t spam_detector_lambda .
```
### 4. Authenticate Docker to ECR
```bash
aws ecr get-login-password --region <YOUR_REGION> | \
  docker login --username AWS --password-stdin \
  <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION> .amazonaws.com
#Replace <YOUR_AWS_ACCOUNT_ID> and <YOUR_REGION>  with your actual AWS account ID and your region
```
### 5. Tag the Image for ECR
```bash 
docker tag spam_detector_lambda:latest <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/spam-detector:latest
```
### 6. Push to ECR
```bash 
docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION> .amazonaws.com spam-detector:latest
```
### 7. Verify the image is in ECR:
```bash 
aws ecr describe-images --repository-name spam-detector --region <YOUR_REGION> 
```
### 7. Create Lambda Function
In the AWS Lambda Console:
- Click Create function
- Select Container image
- Enter function name (spam_detector)
- Click Browse images and select your ECR image
- Under Architecture, choose arm64 (Graviton) because:  
      - Up to 20% lower cost  
      - Better cold start performance  
      - Compatible with all dependencies


### 8. Click **Create function**

## Configuration
After creating the Lambda function, configure these settings:  

**- General Configuration**:  
Navigate to **Configuration → General configuration → Edit**:
* **Timeout**: 30 seconds (allows time for ML model inference)
* **Memory**: 512 MB (default is usually sufficient)

**- Execution Role**:  
Lambda needs basic permissions to run and log:  
- Go to **Configuration → Permissions**  
- Verify the execution role has the policy: **AWSLambdaBasicExecutionRole**

This allows the function to write logs to CloudWatch for debugging.  

**- Function URL (Public Access)**:  
To make your API publicly accessible:
* Go to **Configuration → Function URL**
* Click **Create function URL**
* Configure:
   * Auth type: NONE (for public API)
   * Invoke mode: BUFFERED (required for Lambda Web Adapter)


**- Configure CORS policies (if needed):** a browser security feature that requires a server to grant permission when a web page from one domain requests resources from another
   * Allow origins: * (or specific domains)
   * Allow methods: POST, GET
   * Allow headers: Content-Type


**- Save and copy your function URL**


## Testing
Test your deployed function:
```bash
# Using curl
curl -X POST https://your-function-url.lambda-url.<YOUR_REGION>.on.aws/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won a prize"}'
```
Or visit the function URL in your browser to access the web interface.

### Updating the Application
Whenever you make changes to your code, redeploy with these steps:
```bash
# 1. Rebuild the Docker image
docker build -t spam_detector .

# 2. Re-tag for ECR
docker tag spam_detector:latest \
  <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/spam-detector:latest

# 3. Login to ECR (if needed)
aws ecr get-login-password --region <YOUR_REGION>| \
  docker login --username AWS --password-stdin \
  <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com

# 4. Push updated image
docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/spam-detector:latest
```
Lambda will automatically use the updated image for new invocations. No need to update the Lambda function configuration.


## Useful Commands
```bash
# View local Docker images
docker images

# View AWS configuration
aws configure list

# Check ECR repository contents
aws ecr describe-images --repository-name spam-detector --region us-west-1

# Delete ECR repository (when done)
aws ecr delete-repository --repository-name spam-detector --force --region us-west-1

# View Lambda function logs
aws logs tail /aws/lambda/spam_detector_lambda --follow

# Remove local Docker image
docker rmi spam_detector_lambda
```
License
MIT License - see [../LICENSE](../LICENSE)
