import configs
import pyspark.sql.functions as psf
from utils.logger import logger
from utils.spark_session import get_spark_sesstion


def calc_altitude_mart():
    with get_spark_sesstion() as spark:
        logger.info("=== SparkSession ===")
        logger.info(spark)

        telemetry_df = spark.read.parquet(
            configs.TELEMETRY_FILE_PATH,
            header=True,
            inferSchema=True,
        )

        print("check")

        logger.info("=== Schema ===")
        telemetry_df.printSchema()
        logger.info(f"Количество партиций: {telemetry_df.rdd.getNumPartitions()}")
        logger.info("=== First 5 Rows ===")
        telemetry_df.show(5)

        altitude_df = telemetry_df.groupBy("satellite_id").agg(
            psf.avg("metrics.altitude_km").alias("mean_altitude"),
            psf.max("metrics.altitude_km").alias("max_altitude"),
            psf.min("metrics.altitude_km").alias("min_altitude"),
            psf.count("*").alias("records"),
        )
        altitude_df.show()

        altitude_df.write.mode("overwrite").parquet(configs.ALTITUDE_FILE_PATH)
