from logger import logger

import pyspark.sql.functions as psf
from pyspark.sql import Window

import configs
from spark_session import get_spark_sesstion


def calc_temperature_mart():
    with get_spark_sesstion() as spark:
        logger.info("=== SparkSession ===")
        logger.info(spark)

        telemetry_df = spark.read.parquet(
            configs.TELEMETRY_FILE_PATH,
            header=True,
            inferSchema=True,
        )

        telemetry_df = telemetry_df.withColumn(
            "interval_60_min",
            psf.date_trunc(
                "hour",
                psf.col("timestamp"),
            ),
        )

        window = Window.partitionBy("satellite_id", "interval_60_min").orderBy(
            "timestamp"
        )
        temperature_df = telemetry_df.withColumn(
            "row_number", psf.row_number().over(window)
        )
        temperature_df.show()

        temperature_df = temperature_df.select(
            "satellite_id", "interval_60_min", "metrics.temperature_c"
        ).filter(psf.col("row_number") == 1)
        temperature_df.show()

        window = Window.partitionBy("satellite_id").orderBy("interval_60_min")
        temperature_df = temperature_df.withColumn(
            "grad",
            psf.round(
                psf.col("temperature_c") - psf.lag("temperature_c").over(window), 2
            ),
        )
        temperature_df.show()

        temperature_df.write.mode("overwrite").parquet(configs.TEMPERATURE_FILE_PATH)
