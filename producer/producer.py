from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import uuid
import random
import time
from datetime import datetime
from threading import Thread

# Wait for Kafka
producer = None

while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all"
        )
        print("Connected to Kafka Producer")

    except NoBrokersAvailable:
        print("Kafka not ready. Retrying in 5 seconds...")
        time.sleep(5)


matches = [
    ("match-1", "India", "Australia"),
    ("match-2", "Brazil", "Argentina"),
    ("match-3", "England", "France"),
    ("match-4", "Germany", "Spain"),
    ("match-5", "Japan", "Korea")
]


def simulate_match(match_id, team1, team2):

    while True:

        event_type = random.choice([
            "GOAL",
            "FOUL",
            "CORNER",
            "SHOT"
        ])

        event = {
            "eventId": str(uuid.uuid4()),
            "matchId": match_id,
            "sport": "Football",
            "timestamp": datetime.utcnow().isoformat(),
            "eventType": event_type,
            "data": {
                "team": random.choice([team1, team2]),
                "minute": random.randint(1, 90)
            }
        }

        producer.send(
            "match-events",
            key=match_id,
            value=event
        )

        if event_type == "GOAL":
            producer.send(
                "match-alerts",
                key=match_id,
                value=event
            )

        producer.flush()

        print(
            f"{match_id} | {event_type} | {event['data']['team']}"
        )

        time.sleep(random.randint(1, 4))


for match in matches:
    Thread(
        target=simulate_match,
        args=match,
        daemon=True
    ).start()

while True:
    time.sleep(60)