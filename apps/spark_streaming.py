from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.hadoop.security.authentication", "none") \
    .config("spark.hadoop.security.authorization", "false") \
    .config("spark.kafka.security.protocol", "PLAINTEXT") \
    .getOrCreate()

schema = StructType() \
    .add("name", StringType()) \
    .add("email", StringType()) \
    .add("timestamp", DoubleType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "user-topic") \
    .option("kafka.security.protocol", "PLAINTEXT") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
