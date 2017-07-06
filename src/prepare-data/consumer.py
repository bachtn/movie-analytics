#!/usr/bin/env python

from kafka import KafkaConsumer

consumer = KafkaConsumer('movie_data', group_id='kafka-streaming-example', bootstrap_servers=['localhost:9092'])

for message in consumer:
    consumer.commit()
    print(message)
