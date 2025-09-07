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

jdbc_url = "jdbc:postgresql://postgres:5432/pipeline_db"
db_props = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}

query = json_df.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda batch_df, batch_id:
        batch_df.write
            .format("jdbc")
            .option("url", "jdbc:postgresql://postgres:5432/pipeline_db")
            .option("dbtable", "users")
            .option("user", "airflow")
            .option("password", "airflow")
            .option("driver", "org.postgresql.Driver")
            .mode("append")
            .save()
    ).start()

query.awaitTermination()
