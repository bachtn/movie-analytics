# movie-analytics

# Requirements:
Install kafka, TextBlob, tmdbsimple, beautifulSoup4, requests, json, 

# How to use:
## 1 - Download Kafka
https://www.apache.org/dyn/closer.cgi?path=/kafka/0.11.0.0/kafka\_2.11-0.11.0.0.tgz

## 2 - Start the server (ZooKeeper)
> bin/zookeeper-server-start.sh config/zookeeper.properties

## 3 - Start the Kafka server
> bin/kafka-server-start.sh config/server.properties

## 4 - Create the needed topics ('movie\_data' and 'movie\_popularity')
> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic movie\_data
> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic movie\_popularity

## 5 - Test that the topics were created
> bin/kafka-topics.sh --list --zookeeper localhost:2181
* This command should display the list of tpics ('movie\_data' and 'movie\_popularity') in your case.

## 6 - Collect movie data:
> python collect-data.py

## 7 - Analyse movie reviews:
> python analyse-data.py

## 8 - Save data to hdfs
> cd hdfs\_utils
> sbt run

## 9 - Launch Zepplin notebook
* Download zepplin
> zeppelin-0.7.2-bin-all/bin/zeppelin.sh start 
* go to localhost:8080 in your web browser


## The steps 6 and 7 can be executed in the same time

# Files
## collect-data.py :
collects data about movies and publish it in a kafka stream topic called: 'movie\_data'

## reviewCollector.py :
Is used by 'collect-data.py' to collect the movie reviews

## imdbpy.py : (is no longer used in the project) 
Collects data with imdbpy api but because there is a connection problem, it was replaced with the tmdbsimple api.

## analyse-data.py :
Uses a consumer to listen to the Kafka topic 'movie\_data', and for each message (data for a single movie), analyse its reviews and assigns a score for each one. and than the results are published in a new topic called 'movie\_popularity'
