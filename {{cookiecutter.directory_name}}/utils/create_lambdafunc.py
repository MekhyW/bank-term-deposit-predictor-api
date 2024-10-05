import boto3
import os
from dotenv import load_dotenv

load_dotenv()

function_name = "bank_deposit_prediction"

lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

with open("{{cookiecutter.directory_name}}/predictor.zip", "rb") as f:
    zip_to_deploy = f.read()

lambda_response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime="python3.9",
    Role=lambda_role_arn,
    Handler="predict.lambda_handler",
    Code={"ZipFile": zip_to_deploy},
)

print("Function ARN:", lambda_response["FunctionArn"])