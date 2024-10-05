import pandas as pd
import pickle
import json
import boto3

s3 = boto3.client('s3')

def predict_deposit(input_csv_path, output_csv_path, model_path, encoder_path):
    df = pd.read_csv(input_csv_path)
    X = df.drop("deposit", axis=1)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(encoder_path, "rb") as f:
        one_hot_enc = pickle.load(f)
    X_transformed = one_hot_enc.transform(X)
    X_transformed = pd.DataFrame(X_transformed, columns=one_hot_enc.get_feature_names_out())
    y_pred = model.predict(X_transformed)
    df["y_pred"] = y_pred
    df["y_pred"] = df["y_pred"].map({1: "yes", 0: "no"})
    df.to_csv(output_csv_path, index=False)
    return df

def lambda_handler(event, context):
    input_bucket = event['input_bucket']
    input_key = event['input_key']
    output_bucket = event['output_bucket']
    output_key = event['output_key']
    model_bucket = event['model_bucket']
    input_csv_path = '/tmp/input.csv'
    s3.download_file(input_bucket, input_key, input_csv_path)
    model_path = '/tmp/model.pkl'
    encoder_path = '/tmp/ohe.pkl'
    s3.download_file(model_bucket, "models/model.pkl", model_path)
    s3.download_file(model_bucket, "models/ohe.pkl", encoder_path)
    output_csv_path = '/tmp/output.csv'
    predict_deposit(input_csv_path, output_csv_path, model_path, encoder_path)
    s3.upload_file(output_csv_path, output_bucket, output_key)
    return {
        'statusCode': 200,
        'body': json.dumps('Prediction completed successfully!')
    }