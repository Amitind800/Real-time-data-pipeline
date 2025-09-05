from kafka import KafkaProducer
import json, time
from faker import Faker

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    event = {
        "name": fake.name(),
        "email": fake.email(),
        "timestamp": time.time()
    }

    producer.send("user-topic", value=event)
    print("Produed:", event)
    time.sleep(1)