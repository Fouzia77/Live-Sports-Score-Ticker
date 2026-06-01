# LEARNINGS.md

## Serialization Size Calculation and Reflection

The project uses JSON serialization for Kafka messages. A typical event contains fields such as eventId, matchId, sport, timestamp, eventType, and event data. The average serialized message size was approximately 180–250 bytes depending on field values.

JSON was selected because it is human-readable, easy to debug, and widely supported. However, JSON produces larger payloads than binary formats such as Avro or Protobuf. For production-scale systems handling millions of events per second, a compact binary format would reduce network bandwidth and storage requirements.

## Producer Acknowledgment Experiment

Two producer configurations were evaluated.

### acks=1

The producer receives acknowledgment as soon as the leader broker writes the record.

Advantages:

* Lower latency
* Higher throughput

Disadvantages:

* Possible message loss if the leader fails before replication

### acks=all

The producer waits until all in-sync replicas acknowledge the message.

Advantages:

* Strong durability guarantees
* Reduced risk of message loss

Disadvantages:

* Slightly increased latency

### Conclusion

For a live sports score platform, data integrity is important because losing score updates can create inconsistent match state. Therefore, acks=all was selected as the preferred configuration despite the additional latency.

## Consumer Group Scaling Experiment

### One Consumer Instance

A single consumer instance received all partitions of the match-events topic. All processing occurred within one application instance.

### Two Consumer Instances

Kafka triggered a rebalance and distributed partitions between the two consumers. Each consumer processed a subset of partitions.

### Five Consumer Instances

Each consumer was assigned exactly one partition. This represented the maximum useful parallelism for the topic.

### Six Consumer Instances

The sixth consumer remained idle because all available partitions were already assigned. Kafka cannot assign more active consumers than partitions within a single consumer group.

### Key Learning

The number of partitions determines the maximum parallelism available within a consumer group. Adding consumers beyond the partition count does not increase throughput because no additional partitions are available to assign.

## Overall Reflection

This project provided practical experience with Kafka topics, partitions, message keys, producer acknowledgments, consumer groups, offsets, and lag monitoring. Using matchId as the Kafka key ensured event ordering for each match while partitioning enabled scalability. The project demonstrated how modern real-time event-driven systems process and distribute live data streams efficiently.
