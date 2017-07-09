import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.streaming.kafka._
import kafka.serializer.StringDecoder
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import utils.MovieUtils._
import org.apache.spark.rdd.RDD

object SaveToHDFS {

  def main(arg: Array[String]): Unit = {

    val Array(topics : String, numThreads : String) = Array("movie_popularity,", "1")
    val sparkConf = new SparkConf().setAppName("movie-analytics").setMaster("local[*]")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint("checkpoint")

    val kafkaConf = Map(
      "metadata.broker.list" -> "localhost:6667",
      "zookeeper.connect" -> "localhost:2181",
      "group.id" -> "kafka-streaming-example"
    )

    val topicMap = topics.split(",").map((_, numThreads.toInt)).toMap
    val movies_str: DStream[String] = KafkaUtils.createStream[String, String, StringDecoder, StringDecoder](
        ssc, kafkaConf, topicMap, StorageLevel.MEMORY_ONLY
      ).map(_._2)
    val movies = movies_str.flatMap(parseMovie)
    movies.map(movie => (movie.title, movie.popularity)).print()
    movies.foreachRDD
    {
      rdd =>
        if (rdd.count > 0)
          rdd.repartition(1).saveAsTextFile("./HDFS/" + rdd.hashCode())
    }

    ssc.start()
    ssc.awaitTermination()
  }

}

