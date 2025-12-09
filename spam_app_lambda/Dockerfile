# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.10

# Copy Lambda Web Adapter from public AWS image
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire application
COPY app.py ${LAMBDA_TASK_ROOT}/
#COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/
COPY templates/ ${LAMBDA_TASK_ROOT}/templates/
COPY static/ ${LAMBDA_TASK_ROOT}/static/
COPY models/ ${LAMBDA_TASK_ROOT}/models/

WORKDIR ${LAMBDA_TASK_ROOT}

# Set environment variables for the adapter
ENV PORT=8080
ENV AWS_LWA_INVOKE_MODE=buffered

# Override the Lambda entrypoint
ENTRYPOINT []

# Run Flask directly
#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]