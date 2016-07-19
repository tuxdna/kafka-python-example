from kafka import SimpleConsumer, SimpleClient
from kafka import KafkaConsumer
from kafka import KafkaClient

group_name = "my-group"
topic_name = "fast-messages"

kafka = KafkaClient('127.0.0.1:9092')
consumer = KafkaConsumer(kafka, topic_name, group_id=group_name)

print "Created consumer for group: [%s] and topic: [%s]" % (group_name, topic_name)
print "Waiting for messages..."

for msg in consumer:
    print msg
