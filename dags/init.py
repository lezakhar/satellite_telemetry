import random
from datetime import datetime, timedelta
from io import BytesIO

import boto3
import configs
import pandas as pd
from botocore.exceptions import ClientError


def create_minio_bucket(bucket_name):
    s3_client = boto3.client(
        "s3",
        endpoint_url=configs.MINIO_ENDPOINT,
        aws_access_key_id=configs.MINIO_ACCESS_KEY,
        aws_secret_access_key=configs.MINIO_SECRET_KEY,
    )

    s3_resource = boto3.resource(
        "s3",
        endpoint_url=configs.MINIO_ENDPOINT,
        aws_access_key_id=configs.MINIO_ACCESS_KEY,
        aws_secret_access_key=configs.MINIO_SECRET_KEY,
    )

    try:
        s3_resource.meta.client.list_objects_v2(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "NoSuchBucket":
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully")


def to_minio(
    data: list[dict],
    bucket_name: str,
    object_name: str,
    endpoint_url: str = "http://localhost:9000",
    aws_access_key_id: str = "minioadmin",
    aws_secret_access_key: str = "minioadmin",
    content_type: str = "application/parquet",
):
    """
    Saves a list of dictionaries to MinIO in Parquet format using boto3.

    :param data: List of dictionaries to save
    :param bucket_name: Name of the MinIO bucket
    :param object_name: Name of the object (file) to save
    :param endpoint_url: MinIO server URL
    :param aws_access_key_id: MinIO access key
    :param aws_secret_access_key: MinIO secret key
    :param content_type: type of content
    """

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    df = pd.DataFrame(data)

    parquet_buffer = BytesIO()
    df.to_parquet(
        parquet_buffer,
        engine="pyarrow",
    )

    parquet_buffer.seek(0)

    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except s3_client.exceptions.ClientError:
        s3_client.create_bucket(Bucket=bucket_name)

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=parquet_buffer,
        ContentType=content_type,
    )

    print(
        f"File {object_name} with {len(data)} rows successfully inserted to bucket {bucket_name}"
    )


def generate_fake_telemetry(
    start_date: datetime,
    end_date: datetime,
):
    current_time = start_date
    while current_time < end_date:
        for sat_id in ["SAT-001", "SAT-002", "SAT-003"]:
            yield {
                "satellite_id": sat_id,
                "timestamp": current_time.isoformat() + "Z",
                "metrics": {
                    "altitude_km": 500 + random.gauss(50, 10),
                    "speed_km_s": 7.5 + random.gauss(0.2, 0.1),
                    "battery_voltage": 15 + random.gauss(1, 0.3),
                    "temperature_c": 25 + random.gauss(35, 3),
                    "solar_flux": 1400 + random.gauss(20, 5),
                },
                "status": "NOMINAL" if random.random() > 0.05 else "WARNING",
            }
        current_time += timedelta(seconds=10)


if __name__ == "__main__":
    for bucket_name in ("raw", "mart"):
        create_minio_bucket(bucket_name)

    data = list(
        generate_fake_telemetry(
            start_date=datetime(2025, 10, 1),
            end_date=datetime(2025, 10, 31),
        )
    )

    to_minio(
        data=data,
        bucket_name="raw",
        object_name="telemetry",
    )
