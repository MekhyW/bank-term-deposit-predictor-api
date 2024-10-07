## Bank Marketing ML Project

This project implements a machine learning model to predict term deposit subscriptions for a bank marketing campaign. It can be run as a server using FastAPI or deployed as a serverless function on AWS Lambda.

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/bank-marketing-ml-project.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following environment variables:
     ```
     AWS_ACCESS_KEY_ID="your-access-key-id"
     AWS_SECRET_ACCESS_KEY="your-secret-access-key"
     AWS_REGION="your-region"
     AWS_ACCOUNT_ID="your-account-id"
     AWS_LAMBDA_ROLE_ARN="your-lambda-role-arn"
     ```

### Running as a Server

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

2. The server will run on `http://127.0.0.1:8000`.

### API Endpoints

- GET `/` - Root endpoint to check if the server is running.
- POST `/predict` - Endpoint to predict term deposit subscriptions.
For the /predict endpoint, use the following example request body:

```
{
  "age": 42,
  "job": "entrepreneur",
  "marital": "married",
  "education": "primary",
  "balance": 558,
  "housing": "yes",
  "duration": 186,
  "campaign": 2
}
```

### Deploying as a Serverless Function on AWS Lambda

1. Build the Docker image:
   ```
   docker build -t bank-marketing-ml-project .
   ```

2. Push the image to AWS ECR:
   ```
   aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
   docker tag bank-marketing-ml-project:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/bank-marketing-ml-project:latest
   docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/bank-marketing-ml-project:latest
   ```

3. Deploy the container image to AWS Lambda:
   ```
   aws lambda create-function --function-name bank-marketing-ml-project --package-type Image --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/bank-marketing-ml-project:latest --role $AWS_LAMBDA_ROLE_ARN
   ```

4. Test the Lambda function:
   ```
   aws lambda invoke --function-name bank-marketing-ml-project --payload '{"age": 42, "job": "entrepreneur", "marital": "married", "education": "primary", "balance": 558, "housing": "yes", "duration": 186, "campaign": 2}' output.txt
   cat output.txt
   ```

## Project Structure

- src/: Contains the main application code
- utils/: Contains scripts for AWS deployment
- models/: Stores the trained model and encoder
- data/: Stores the input and processed data
- notebooks/: Contains notebooks for data exploration and model training

## Authentication

By default, the /predict endpoint requires authentication. A simple token-based authentication system is implemented using SQLite. You need to add valid tokens to the tokens.db database before making predictions.
