# CLI_JOURNAL.md

## Command 1

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Output:

```text
__consumer_offsets
match-alerts
match-events
score-updates
```

Explanation:
This command lists all Kafka topics currently available in the cluster.

---

## Command 2

```bash
kafka-topics --describe --topic match-events --bootstrap-server localhost:9092
```

Output:

```text
Topic: match-events
PartitionCount: 5
ReplicationFactor: 1
```

Explanation:
This command displays partition and replication information for the match-events topic.

---

## Command 3

```bash
kafka-topics --describe --topic score-updates --bootstrap-server localhost:9092
```

Output:

```text
Topic: score-updates
PartitionCount: 5
ReplicationFactor: 1
```

Explanation:
This command verifies that the score-updates topic contains five partitions.

---

## Command 4

```bash
kafka-topics --describe --topic match-alerts --bootstrap-server localhost:9092
```

Output:

```text
Topic: match-alerts
PartitionCount: 1
ReplicationFactor: 1
```

Explanation:
This command confirms that match-alerts uses a single partition to preserve ordering.

---

## Command 5

```bash
kafka-console-consumer --topic match-events --bootstrap-server localhost:9092 --from-beginning
```

Output:

```text
{"eventId": "8b51d29c-80da-48f3-ab5b-a1eafdc7d6f3", "matchId": "match-5", "sport
": "Football", "timestamp": "2026-06-01T04:06:37.882914", "eventType": "SHOT", "
data": {"team": "Japan", "minute": 13}}
{"eventId": "116903ad-f0d4-40ff-9ad0-dc26ee8d4227", "matchId": "match-3", "sport
": "Football", "timestamp": "2026-06-01T04:06:37.802179", "eventType": "GOAL", "
data": {"team": "France", "minute": 90}}
{"eventId": "17d2b14a-8c7c-4597-982a-dbd1b36eaf4a", "matchId": "match-4", "sport
": "Football", "timestamp": "2026-06-01T04:06:36.830711", "eventType": "SHOT", "
data": {"team": "Spain", "minute": 41}}

```

Explanation:
This command consumes events from the beginning of the topic and displays them in the terminal.

---

## Command 6

```bash
kafka-console-consumer --topic match-alerts --bootstrap-server localhost:9092 --from-beginning
```

Output:

```text
{"eventId": "b02b7670-0d59-4bd1-8ae1-ebbcffb4d479", "matchId": "match-5", "sport": "Football", "timestamp": "2026-06-01T04:02:10.159816", "eventType": "GOAL", "data": {"team": "Korea", "minute
": 4}}
{"eventId": "5c1202d4-ffc8-405e-b019-f4953107dd1b", "matchId": "match-2", "sport": "Football", "timestamp": "2026-06-01T04:02:30.187108", "eventType": "GOAL", "data": {"team": "Argentina", "mi
nute": 8}}
{"eventId": "df354a74-c987-43d5-b911-a60add37415c", "matchId": "match-1", "sport": "Football", "timestamp": "2026-06-01T04:02:34.193154", "eventType": "GOAL", "data": {"team": "India", "minute
": 77}}

```

Explanation:
This command verifies that alert events are being published correctly.

---

## Command 7

```bash
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group scoreboard-service
```

Output:

```text
GROUP               TOPIC           PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG
scoreboard-service  match-events    2         175            177            2
scoreboard-service  match-events    3         182            184            2
scoreboard-service  match-events    0         1137           1142           5
scoreboard-service  match-events    0         473            474            1
scoreboard-service  match-events    4         0              0              0
```

Explanation:
This command displays consumer group offsets and lag information.

---

## Command 8

```bash
docker compose ps
```

Output:

```text
kafka          Up
zookeeper      Up
producer-app   Up
consumer-app   Up
```

Explanation:
This command verifies that all required services are running successfully.
