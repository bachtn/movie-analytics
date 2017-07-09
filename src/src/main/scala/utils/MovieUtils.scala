package utils
import play.api.libs.json.{Format, JsError, JsSuccess, Json}
import org.joda.time.{DateTime, Period}
import utils.ReviewUtils._

import scala.util.parsing.json.JSON

/**
  * Created by bach on 06/07/17.
  */
object MovieUtils {
  case class Movie(
                  id: String,
                  title: String,
                  release_date: String, //TODO: change to Datetime
                  genres: Seq[String],
                  adult: String,
                  popularity: String,
                  rating: String,
                  nbr_votes: String,
                  budget: String,
                  revenue: String,
                  duration: String,
                  url: String,
                  reviews: Option[Seq[String]],
                  popularity_from_reviews: Option[String]
                  )

  implicit val movieFormat: Format[Movie] = Json.format[Movie]

  def StringToMovie(str: String): Option[Movie] = Json.parse(str).validate[Movie] match {
    case JsError(e) => println(e); None
    case JsSuccess(movie, _) => Some(movie)
  }

  def parseJSON(s: String): Map[String, Any] =
    JSON.parseFull(s).get.asInstanceOf[Map[String, Any]]

  def parseMovie(s : String): Option[Movie] =  {
    val json = parseJSON(s)
    Some(Movie(json("id").toString,
      json("title").toString,
      json("release_date").toString,
      Seq(json("genres").toString),
      json("adult").toString,
      json("popularity").toString,
      json("rating").toString,
      json("nbr_votes").toString,
      json("budget").toString,
      json("revenue").toString,
      json("duration").toString,
      json("url").toString,
      Some(Seq(json("reviews").toString)),
      Some(json("popularity_from_reviews").toString)))
  }
}
