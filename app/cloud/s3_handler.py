import boto3
import os
from app.config.config_loader import load_config

config = load_config()

AWS_ACCESS_KEY = config["aws"]["access_key_id"]
AWS_SECRET_KEY = config["aws"]["secret_access_key"]
AWS_BUCKET = config["aws"]["bucket_name"]
AWS_REGION = config["aws"]["region"]


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )


def upload_raw_data_to_s3():
    s3 = get_s3_client()
    raw_path = config["paths"]["raw_data"]

    print("\n================ UPLOADING TO S3 ================\n")

    for file in os.listdir(raw_path):
        if file.endswith(".csv"):
            local_path = os.path.join(raw_path, file)
            s3_key = f"raw/{file}"
            s3.upload_file(local_path, AWS_BUCKET, s3_key)
            print(f"Uploaded: {file} → s3://{AWS_BUCKET}/{s3_key}")

    print("\nAll files uploaded to S3 successfully ✅")


def list_s3_files():
    s3 = get_s3_client()

    print("\n================ S3 BUCKET CONTENTS ================\n")

    response = s3.list_objects_v2(Bucket=AWS_BUCKET)

    if "Contents" in response:
        for obj in response["Contents"]:
            print(f"{obj['Key']} — {obj['Size']} bytes")
    else:
        print("Bucket is empty")