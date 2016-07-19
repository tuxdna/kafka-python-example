from kafka import KafkaClient
from kafka import SimpleProducer
from kafka import KafkaProducer
import sys

kafka = KafkaClient('127.0.0.1:9092')
producer = SimpleProducer(kafka, async=True)

topic_name = "fast-messages"
print "sending messages to topic: [%s]" % (topic_name)

for i in range(10):
    msg = 'async message-%d' % (i)
    print "sending message: [%s]" % msg
    producer.send_messages('fast-messages', msg)
