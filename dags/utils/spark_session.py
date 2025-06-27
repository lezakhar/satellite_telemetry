import configs
from pyspark.sql import SparkSession


def get_spark_sesstion() -> SparkSession:
    return (
        SparkSession.builder.appName("AirflowMinIOExample")
        .master(configs.SPARK_MASTER_ENDPOINT)
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.11.901",
        )
        .config("spark.hadoop.fs.s3a.access.key", configs.MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", configs.MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.endpoint", configs.MINIO_SPARK_ENDPOINT)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.driver.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true"
        )
        .config(
            "spark.executor.extraJavaOptions",
            "-Dcom.amazonaws.services.s3.enableV4=true",
        )
        .getOrCreate()
    )
