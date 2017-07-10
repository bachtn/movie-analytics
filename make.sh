## Not working YET

#launch zookeeper server
/home/bach/Downloads/kafka_2.11-0.11.0.0/bin/zookeeper-server-start.sh config/zookeeper.properties & 
# launch kafka server
/home/bach/Downloads/kafka_2.11-0.11.0.0/bin/kafka-server-start.sh config/server.properties &

cd src
# collect movie data
./collect-data.py &
# analyse movie reviews
./analyse-data.py &
# save data to HDFS
cd hdfs_utils
sbt run &
# launch zeppelin notebook
sudo /home/bach/Downloads/zeppelin-0.7.2-bin-all/bin/zeppelin.sh start &
# go to localhost:8080 in your web browser

