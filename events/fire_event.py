import json
import time
from confluent_kafka import Producer

# 1. Connection Settings
# We use localhost:19092 because that's the 'external' port we mapped in Docker
conf = {
    'bootstrap.servers': 'localhost:19092',
    'client.id': 'aviator-game-engine'
}

# 2. Initialize the Producer
producer = Producer(conf)

def delivery_report(err, msg):
    """ Callback called once message is delivered or failed. """
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Event fired to {msg.topic()} [partition {msg.partition()}]")

def fire_run_game(game_id, player_id, bet_amount):
    # This is your "Structure" - Redpanda will just see this as bytes
    event_data = {
        "event_type": "GAME_START",
        "game_id": game_id,
        "player": player_id,
        "bet": bet_amount,
        "timestamp": time.time(),
        "status": "in_progress"
    }

    # Convert dict to JSON string, then to bytes
    payload = json.dumps(event_data).encode('utf-8')

    # Send the event
    producer.produce(
        topic='run_game', 
        key=game_id, 
        value=payload, 
        callback=delivery_report
    )

    # 'flush' makes sure the message actually leaves the laptop and hits Redpanda
    producer.flush()

if __name__ == "__main__":
    print("🚀 Firing new game event...")
    fire_run_game("G-882", "munya_dev", 10.50)