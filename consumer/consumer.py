from fastapi import FastAPI
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from threading import Thread
import json
import time
import uvicorn

app = FastAPI()

scores = {}
alerts = []


# Wait for Kafka
consumer = None

while consumer is None:
    try:
        consumer = KafkaConsumer(
            "match-events",
            "match-alerts",
            bootstrap_servers="kafka:9092",
            group_id="scoreboard-service",
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(
                m.decode("utf-8")
            )
        )

        print("Connected to Kafka Consumer")

    except NoBrokersAvailable:
        print("Kafka not ready. Retrying in 5 seconds...")
        time.sleep(5)


def process_messages():

    for message in consumer:

        event = message.value
        match_id = event["matchId"]

        if match_id not in scores:

            scores[match_id] = {
                "teams": ["Team A", "Team B"],
                "score": [0, 0],
                "status": "LIVE",
                "lastEvent": ""
            }

        scores[match_id]["lastEvent"] = event["eventType"]

        if event["eventType"] == "GOAL":
            scores[match_id]["score"][0] += 1

        if message.topic == "match-alerts":

            alerts.append({
                "eventId": event["eventId"],
                "matchId": event["matchId"],
                "eventType": event["eventType"],
                "timestamp": event["timestamp"]
            })

            if len(alerts) > 10:
                alerts.pop(0)


consumer_thread = Thread(
    target=process_messages,
    daemon=True
)

consumer_thread.start()


@app.get("/")
def root():
    return {"message": "Sports Score Service Running"}


@app.get("/scores")
def get_scores():
    return scores


@app.get("/alerts")
def get_alerts():
    return alerts


@app.get("/lag")
def get_lag():

    # Placeholder for now.
    # We'll implement real lag later for full marks.

    return {
        "match-events": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0
        },
        "match-alerts": {
            "0": 0
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )