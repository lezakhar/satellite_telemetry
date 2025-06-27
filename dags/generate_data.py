# Пример скрипта для генерации данных (можно запустить как DAG в Airflow)
import random

import pandas as pd
import boto3

from datetime import datetime, timedelta

from io import BytesIO


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
    Сохраняет список словарей в MinIO в формате Parquet с использованием boto3

    :param data: Список словарей для сохранения
    :param bucket_name: Имя бакета в MinIO
    :param object_name: Имя объекта (файла) для сохранения
    :param endpoint_url: URL MinIO сервера
    :param aws_access_key_id: Ключ доступа MinIO
    :param aws_secret_access_key: Секретный ключ MinIO
    """

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Преобразуем список словарей в DataFrame
    df = pd.DataFrame(data)

    # Конвертируем DataFrame в Parquet в памяти
    parquet_buffer = BytesIO()
    df.to_parquet(
        parquet_buffer,
        engine="pyarrow",
    )

    # Перемещаем указатель в начало буфера
    parquet_buffer.seek(0)

    # Проверяем, существует ли бакет, если нет - создаем
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except s3_client.exceptions.ClientError:
        s3_client.create_bucket(Bucket=bucket_name)

    # Загружаем данные в MinIO
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=parquet_buffer,
        ContentType=content_type,
    )

    print(
        f"Файл {object_name} размером {len(data)} строк успешно сохранен в бакете {bucket_name}"
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
    example = list(
        generate_fake_telemetry(
            start_date=datetime(2025, 10, 1),
            end_date=datetime(2025, 10, 31),
        )
    )

    to_minio(
        data=example,
        bucket_name="raw",
        object_name="telemetry",
    )
