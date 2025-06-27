from logger import logger

import pyspark.sql.functions as psf

import configs
from spark_session import get_spark_sesstion


def calc_speed_mart():
    with get_spark_sesstion() as spark:
        logger.info("=== SparkSession ===")
        logger.info(spark)

        telemetry_df = spark.read.parquet(
            configs.TELEMETRY_FILE_PATH,
            header=True,
            inferSchema=True,
        )

        telemetry_df = telemetry_df.withColumn(
            "interval_15_min",
            psf.expr(
                "interval_60_min + INTERVAL 15 MINUTE * (minute(timestamp) DIV 15)"
            ),
        )

        speed_df = (
            telemetry_df.select("satellite_id", "interval_15_min", "metrics.speed_km_s")
            .groupBy("satellite_id", "interval_15_min")
            .agg(
                psf.avg("speed_km_s").alias("avg_speed"),
                psf.max("speed_km_s").alias("max_speed"),
                psf.min("speed_km_s").alias("min_speed"),
            )
        )

        speed_df = speed_df.withColumn(
            "interval",
            psf.concat(
                "interval_15_min",
                psf.lit(":"),
                psf.expr("interval_15_min + INTERVAL 15 minute"),
            ),
        )

        speed_df = speed_df.select(
            "satellite_id",
            "interval",
            "avg_speed",
            "max_speed",
            "min_speed",
        )
        speed_df.show(truncate=False)

        speed_df.write.mode("overwrite").parquet(configs.SPEED_FILE_PATH)
