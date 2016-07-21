from pykafka import KafkaClient
import time
import uuid

client = KafkaClient(hosts="localhost:9092")
topic = client.topics[b"test"]

consumer = topic.get_balanced_consumer(
    consumer_group="test_group",
    auto_commit_enable=True,
    zookeeper_connect="localhost:2181")

display_interval = 5  # secs

print 'Consuming messagse from topic %r. Press Ctrl-C to interrupt.' % topic.name

display_iteration = 0
message_count = 0
partitions = set()  # Track which partitions got consumed by this consumer
start_time = time.time()

while True:
    message = consumer.consume()  # Read one message from Kafka
    identifier = uuid.UUID(message.value)  # Decode the message
    message_count += 1
    partitions.add(message.partition.id)
    now = time.time()
    if now - start_time > display_interval:
        print '%i) %i messages consumed at %.0f messages / second - from partitions %r' % (
            display_iteration,
            message_count,
            message_count / (now - start_time),
            sorted(partitions))
        display_iteration += 1
        message_count = 0
        partitions = set()
        start_time = time.time()
