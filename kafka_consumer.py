from kafka import KafkaConsumer
import json

# Connect to Kafka
consumer = KafkaConsumer(
    "user-topic",                          # topic name
    bootstrap_servers=["localhost:9092"],  # same as producer
    auto_offset_reset="earliest",          # start from beginning if no offset
    enable_auto_commit=True,
    group_id="my-consumer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening for messages on 'user-topic'...")

for message in consumer:
    print("Consumed:", message.value)
