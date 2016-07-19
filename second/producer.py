from kafka import KafkaClient
from kafka import SimpleProducer
from kafka import KafkaProducer
import sys

kafka = KafkaClient('127.0.0.1:9092')
producer = KafkaProducer()

group_name = "my-group"
topic_name = "fast-messages"
print "sending messages to group: [%s] and topic: [%s]" % (group_name, topic_name)

# send only one message
producer.send('fast-messages', value="Some message")
