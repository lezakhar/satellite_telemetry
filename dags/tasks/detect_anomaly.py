import pyspark.sql.functions as psf

from airflow.decorators import task

from pyspark.sql import DataFrame, Window
from airflow.exceptions import AirflowSkipException

import configs

from logger import logger
from spark_session import get_spark_sesstion

from _typing import Anomaly


def _to_html(df: DataFrame) -> str:
    pdf = df.toPandas()

    html_table = pdf.to_html(
        index=False,
        classes="dataframe",
        border=0,
    )
    return f"<pre>{html_table}</pre>"


@task
def detect_anomaly() -> list[Anomaly]:
    anomalies: list = []

    with get_spark_sesstion() as spark:
        logger.info("=== SparkSession ===")
        logger.info(spark)

        ################################################################Temperature anomalies##########################################################
        temperature_df = spark.read.parquet(
            configs.TEMPERATURE_FILE_PATH,
            header=True,
            inferSchema=True,
        )

        temperature_anomaly_df_1 = temperature_df.filter(
            (psf.col("temperature_c") > 55)
        )
        window = Window.partitionBy("satellite_id").orderBy(
            psf.col("interval_60_min").desc()
        )
        temperature_anomaly_df_1 = temperature_anomaly_df_1.withColumn(
            "row_number", psf.row_number().over(window)
        )
        temperature_anomaly_df_1.show()
        temperature_anomaly_df_1 = temperature_anomaly_df_1.filter(
            psf.col("row_number") == 1
        )
        temperature_anomaly_df_1.show()

        if not temperature_anomaly_df_1.isEmpty():
            anomalies.append(
                Anomaly(
                    description="🚨the temperature has exceeded the threshold value🚨",
                    data=f"data: \n {_to_html(temperature_anomaly_df_1)}",
                )
            )

        temperature_anomaly_df_2 = temperature_df.filter(psf.abs(psf.col("grad")) > 6)
        temperature_anomaly_df_2 = temperature_anomaly_df_1.withColumn(
            "row_number",
            psf.row_number().over(window),
        )
        temperature_anomaly_df_2.show()
        temperature_anomaly_df_2 = temperature_anomaly_df_1.filter(
            psf.col("row_number") == 1
        )
        temperature_anomaly_df_2.show()

        if not temperature_anomaly_df_2.isEmpty():
            anomalies.append(
                Anomaly(
                    description="🚨rapid temperature change🚨",
                    data=f"data: \n {_to_html(temperature_anomaly_df_2)}",
                )
            )

        ################################################################Speed anomalies###############################################################
        speed_df = spark.read.parquet(
            configs.SPEED_FILE_PATH,
            header=True,
            inferSchema=True,
        )

        speed_anomaly_df = speed_df.filter(
            (psf.col("min_speed") < 7.4) | (psf.col("max_speed") > 8.0)
        )

        window = Window.partitionBy("satellite_id").orderBy(psf.col("interval").desc())
        speed_anomaly_df = speed_anomaly_df.withColumn(
            "row_number",
            psf.row_number().over(window),
        )
        speed_anomaly_df.show(truncate=False)
        speed_anomaly_df = speed_anomaly_df.filter(psf.col("row_number") == 1)
        speed_anomaly_df.show(truncate=False)

        if not speed_anomaly_df.isEmpty():
            anomalies.append(
                Anomaly(
                    description="🚨abnormal decline or accelaration detected🚨",
                    data=f"data: \n {_to_html(speed_anomaly_df)}",
                )
            )

        if not anomalies:
            raise AirflowSkipException("anomalies not detected")

    return anomalies
