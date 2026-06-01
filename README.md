# Live Sports Score Ticker with Apache Kafka

## Overview

This project implements a real-time sports score ticker using Apache Kafka. The system simulates live sports matches, publishes match events to Kafka topics, consumes those events, maintains in-memory match state, and exposes REST APIs for scoreboards, alerts, and consumer lag monitoring.

## Architecture

Components:

1. Kafka Broker

   * Stores and distributes event streams.

2. Zookeeper

   * Coordinates Kafka broker operations.

3. Producer Application

   * Simulates 5 concurrent sports matches.
   * Publishes events to Kafka topics.
   * Uses matchId as the Kafka message key.

4. Consumer Application

   * Consumes match events and alerts.
   * Maintains current match state.
   * Exposes REST APIs.

5. Frontend (Optional)

   * Can consume REST APIs to display live scores.

## Kafka Topics

### match-events (5 partitions)

This topic stores all match events.

Reasoning:

* Five partitions allow parallel processing.
* Events belonging to the same match use matchId as the key.
* Kafka guarantees ordering within a partition.

### score-updates (5 partitions)

Reserved for processed score updates.

Reasoning:

* Matches the parallelism of match-events.
* Supports future stream processing.

### match-alerts (1 partition)

Stores high-priority events such as goals.

Reasoning:

* Single partition guarantees global ordering.
* Alerts appear in the exact sequence they were produced.

## Running the Project

Prerequisites:

* Docker
* Docker Compose

Start the entire system:

```bash
docker compose up --build
```

Verify containers:

```bash
docker compose ps
```

## API Endpoints

### GET /scores

Returns current state of all matches.

Example:

```json
{
  "match-1": {
    "teams": ["Team A","Team B"],
    "score": [2,1],
    "status": "LIVE"
  }
}
```

### GET /alerts

Returns latest high-priority events.

### GET /lag

Returns consumer lag information.

## Kafka Verification

List topics:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Describe topic:

```bash
kafka-topics --describe --topic match-events --bootstrap-server localhost:9092
```

## Technologies Used

* Apache Kafka
* Python
* FastAPI
* Docker
* Docker Compose


