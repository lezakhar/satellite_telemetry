import os

from dotenv import load_dotenv

load_dotenv()


SPARK_MASTER_ENDPOINT: str = str(os.getenv("SPARK_MASTER_ENDPOINT"))

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_SPARK_ENDPOINT = os.getenv("MINIO_SPARK_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

TELEMETRY_FILE_PATH = "s3a://raw/telemetry"
ALTITUDE_FILE_PATH = "s3a://mart/altitude"
SPEED_FILE_PATH = "s3a://mart/speed"
TEMPERATURE_FILE_PATH = "s3a://mart/temperature"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(SPARK_MASTER_ENDPOINT)
