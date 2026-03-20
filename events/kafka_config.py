import json
import time
from confluent_kafka import Producer


CONF = {
    'bootstrap.servers': 'localhost:19092', 
    'client.id': 'aviator-game-engine'     
}
producer = Producer(CONF)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Event fired to {msg.topic()} [partition {msg.partition()}]")

def send_event(topic, key, event_data: dict):
    payload = json.dumps(event_data).encode('utf-8')
    producer.produce(
        topic=topic,
        key=str(key), 
        value=payload,
        callback=delivery_report
    )
    producer.flush()