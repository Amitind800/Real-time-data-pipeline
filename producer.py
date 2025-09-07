from kafka import KafkaProducer
import json,time, random, names


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v:json.dumps(v).encode('utf-8'))

while True:
    #event = {
    #    "name": random.choice(["Amit", "Ravi", "Sneha", "Priya"]),
    #    "email": f"user{random.randint(1,100)}@example.com",
    #    "timestamp": time.time()
    #}
    message = {
        "name": names.get_first_name(),
        "email": f"user{random.randint(1, 1000)}@example.com",
        "timestamp": time.time()
    }
    producer.send("user-topic", value=message)
    print("Sent:", message)
    time.sleep(2)