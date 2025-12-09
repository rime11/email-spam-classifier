
from mangum import Mangum
from app import app

# Mangum works with both API Gateway AND Function URLs
handler = Mangum(app, lifespan="off")
def lambda_handler(event, context):
    return handler(event, context)

