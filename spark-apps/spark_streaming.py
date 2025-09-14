from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lower, trim, monotonically_increasing_id
from pyspark.sql.types import StructType, StringType, DoubleType

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

schema = StructType() \
    .add("name", StringType()) \
    .add("email", StringType()) \
    .add("timestamp", DoubleType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "user-topic") \
    .option("startingOffsets", "earliest") \
    .option("kafka.security.protocol", "PLAINTEXT") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# ✅ Clean + Deduplicate + Add user_id
transformed_df = json_df \
    .withColumn("email", trim(lower(col("email")))) \
    .withColumn("name", trim(col("name"))) \
    .withColumn("user_id", monotonically_increasing_id()) \
    .dropDuplicates(["email"])

# ✅ Write to Postgres with checkpointing
query = transformed_df.writeStream \
    .outputMode("append") \
    .option("checkpointLocation", "/opt/bitnami/spark/checkpoints/users") \
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
