# Python Kafka examples


## Using kafka-python library


### Setting Kafka on single node

```
wget -c http://mirror.fibergrid.in/apache/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz
tar zxf kafka_2.11-0.9.0.1.tgz
cd kafka_2.11-0.9.0.1/
```

In first terminal, start Zookeeper:


```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

In second terminal, start Apache Kafka:

```
bin/kafka-server-start.sh config/server.properties
```

Keep these terminals aside, and start a new terminal. In this third terminal, we will create a queue to which we will post our messages. So, first we will create a queue ( also called a topic ):

```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic fast-messages
```
Now we are done setting up Kafka and a topic for our example.

### Setting up Kafka Python using PIP / Virtualenv

We will use Virtualenv to install the Kafka Python API, and use this virtualenv henceforth in all the examples:

```
virtualenv --system-site-packages env-kafka
source env-kafka/bin/activate
pip install kafka
```

### Simple Producer / Consumer

Here we SimpleProducer / SimpleConsumer to produce and consume messages using Python.

First produce some messages:
```
$ python simple/producer.py 
sending messages to topic: [fast-messages]
sending message: [async message-0]
sending message: [async message-1]
sending message: [async message-2]
sending message: [async message-3]
sending message: [async message-4]
sending message: [async message-5]
sending message: [async message-6]
sending message: [async message-7]
sending message: [async message-8]
sending message: [async message-9]
```

Now the consumer will read them:

```
$ python simple/consumer.py 
Created consumer for group: [my-group] and topic: [fast-messages]
Waiting for messages...
OffsetAndMessage(offset=3003226, message=Message(crc=-763031758, magic=0, attributes=0, timestamp=None, key=None, value='async message-0'))
OffsetAndMessage(offset=3003227, message=Message(crc=-1518190684, magic=0, attributes=0, timestamp=None, key=None, value='async message-1'))
OffsetAndMessage(offset=3003228, message=Message(crc=1015770654, magic=0, attributes=0, timestamp=None, key=None, value='async message-2'))
OffsetAndMessage(offset=3003229, message=Message(crc=1267490440, magic=0, attributes=0, timestamp=None, key=None, value='async message-3'))
OffsetAndMessage(offset=3003230, message=Message(crc=-706163925, magic=0, attributes=0, timestamp=None, key=None, value='async message-4'))
OffsetAndMessage(offset=3003231, message=Message(crc=-1561330755, magic=0, attributes=0, timestamp=None, key=None, value='async message-5'))
OffsetAndMessage(offset=3003232, message=Message(crc=1004972551, magic=0, attributes=0, timestamp=None, key=None, value='async message-6'))
OffsetAndMessage(offset=3003233, message=Message(crc=1289853585, magic=0, attributes=0, timestamp=None, key=None, value='async message-7'))
OffsetAndMessage(offset=3003234, message=Message(crc=-597784832, magic=0, attributes=0, timestamp=None, key=None, value='async message-8'))
OffsetAndMessage(offset=3003235, message=Message(crc=-1420183658, magic=0, attributes=0, timestamp=None, key=None, value='async message-9'))
OffsetAndMessage(offset=3003236, message=Message(crc=-763031758, magic=0, attributes=0, timestamp=None, key=None, value='async message-0'))
OffsetAndMessage(offset=3003237, message=Message(crc=-1518190684, magic=0, attributes=0, timestamp=None, key=None, value='async message-1'))
OffsetAndMessage(offset=3003238, message=Message(crc=1015770654, magic=0, attributes=0, timestamp=None, key=None, value='async message-2'))
OffsetAndMessage(offset=3003239, message=Message(crc=1267490440, magic=0, attributes=0, timestamp=None, key=None, value='async message-3'))
OffsetAndMessage(offset=3003240, message=Message(crc=-706163925, magic=0, attributes=0, timestamp=None, key=None, value='async message-4'))
OffsetAndMessage(offset=3003241, message=Message(crc=-1561330755, magic=0, attributes=0, timestamp=None, key=None, value='async message-5'))
OffsetAndMessage(offset=3003242, message=Message(crc=1004972551, magic=0, attributes=0, timestamp=None, key=None, value='async message-6'))
OffsetAndMessage(offset=3003243, message=Message(crc=1289853585, magic=0, attributes=0, timestamp=None, key=None, value='async message-7'))
OffsetAndMessage(offset=3003244, message=Message(crc=-597784832, magic=0, attributes=0, timestamp=None, key=None, value='async message-8'))
OffsetAndMessage(offset=3003245, message=Message(crc=-1420183658, magic=0, attributes=0, timestamp=None, key=None, value='async message-9'))
```

This API is deprecated now so we will next use KafkaProducer / KafkaConsumer API instead.

### Using non-deprecated API

Here we KafkaProduce / KafkaConsumer to produce and consume messages using Python.

First produce some messages:
```
$ python second/producer.py 
sending messages to group: [my-group] and topic: [fast-messages]
```

Now the consumer will read them:

```
$ python second/consumer.py 
Created consumer for group: [my-group] and topic: [fast-messages]
Waiting for messages...
ConsumerRecord(topic=u'fast-messages', partition=0, offset=3003247, timestamp=None, timestamp_type=None, key=None, value='Some message')
```

All seems well and good. However, if you look at Kafka logs, you might see following error:

```
[2016-07-19 17:18:41,197] ERROR Processor got uncaught exception. (kafka.network.Processor)
java.lang.ArrayIndexOutOfBoundsException: 18
	at org.apache.kafka.common.protocol.ApiKeys.forId(ApiKeys.java:68)
	at org.apache.kafka.common.requests.AbstractRequest.getRequest(AbstractRequest.java:39)
	at kafka.network.RequestChannel$Request.<init>(RequestChannel.scala:79)
	at kafka.network.Processor$$anonfun$run$11.apply(SocketServer.scala:426)
	at kafka.network.Processor$$anonfun$run$11.apply(SocketServer.scala:421)
	at scala.collection.Iterator$class.foreach(Iterator.scala:742)
	at scala.collection.AbstractIterator.foreach(Iterator.scala:1194)
	at scala.collection.IterableLike$class.foreach(IterableLike.scala:72)
	at scala.collection.AbstractIterable.foreach(Iterable.scala:54)
	at kafka.network.Processor.run(SocketServer.scala:421)
	at java.lang.Thread.run(Thread.java:745)
```

The above error is a known issue and can be resolved using Kafka to version 0.10 or above. Read here for more details and why it happens:

 * https://mail-archives.apache.org/mod_mbox/kafka-users/201607.mbox/%3CCAK2DJU9H9VNJJQajSUD0E1i_89SnuoFC99vmVoAELndD=xqm8A@mail.gmail.com%3E 
 * https://issues.apache.org/jira/browse/KAFKA-3547



## Using pykafka library

```
pip install pykafka
```


```
$ python pk/producer.py
```

Consumer(s) - you can start multiple consumers in different terminals

```
$ python pk/consumer.py
```


## Replay messages

There are two ways to replay messages:

 * Using replay tool
 * Using the API
 
 
### Using replay tool

References:

 * https://community.hortonworks.com/questions/17840/kafka-system-tools-for-replay.html
 * https://cwiki.apache.org/confluence/display/KAFKA/System+Tools#SystemTools-ReplayLogProducer

First obtain a list of topics

```
$ bin/kafka-topics.sh  --list --zookeeper localhost:2181
__consumer_offsets
fast-messages
summary-markers
```

Next we use a Kafka Tool that can help us replay all the messages

Create a new topic

```
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic fast-messages2
Created topic "fast-messages2".
```

Describe properties of the two topics:

```
$ bin/kafka-topics.sh --describe --zookeeper localhost:2181  --topic fast-messages
Topic:fast-messages	PartitionCount:1	ReplicationFactor:1	Configs:
	Topic: fast-messages	Partition: 0	Leader: 0	Replicas: 0	Isr: 0

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181  --topic fast-messages2
Topic:fast-messages2	PartitionCount:1	ReplicationFactor:1	Configs:
	Topic: fast-messages2	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
```

Replay the messages onto new topic

```
$ bin/kafka-run-class.sh kafka.tools.ReplayLogProducer --sync --broker-list localhost:9092 --inputtopic fast-messages --outputtopic fast-messages2 --zookeeper localhost:2181
```

Altering an existing topic in Kafka. Lets change the number of partitions:

## Tips & Tricks

```
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
__consumer_offsets
fast-messages
fast-messages2
fast-messages3
summary-markers
test

$ bin/kafka-topics.sh --alter --topic test --partitions 6 --zookeeper localhost:2181
WARNING: If partitions are increased for a topic that has a key, the partition logic or ordering of the messages will be affected
Adding partitions succeeded!
```

### TODO: Replay using API

TBD

## References

 * Follow this tutorial to setup Kafka: https://www.mapr.com/blog/getting-started-sample-programs-apache-kafka-09
 * Kafka Official Documentation: https://kafka.apache.org/documentation.html
 * Python Kafka API: https://kafka-python.readthedocs.io/en/master/simple.html
 * Apache Kafka 0.8 Training Deck and Tutorial http://www.michael-noll.com/blog/2014/08/18/apache-kafka-training-deck-and-tutorial/
 
 
