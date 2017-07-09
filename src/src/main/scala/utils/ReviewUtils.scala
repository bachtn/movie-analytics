package utils
import play.api.libs.json.{Format, JsError, JsSuccess, Json}
import org.joda.time.DateTime

import scala.util.parsing.json.JSON

/**
  * Created by bach on 06/07/17.
  */
object ReviewUtils {
  case class Review(
                   author_id: Option[String],
                   title: Option[String],
                   review_date: Option[String],
                   content: Option[String],
                   title_score: Option[String],
                   content_score: Option[String]
                   )

  implicit val reviewFormat: Format[Review] = Json.format[Review]

  def StringToReview(str: String): Option[Review] = Json.parse(str).validate[Review] match {
    case JsError(e) => println(e); None
    case JsSuccess(review, _) => Some(review)
  }

  def parseJSON(s: String): Map[String, Any] = {
    print(s)
    JSON.parseFull(s).get.asInstanceOf[Map[String, Any]]
  }

  def parseReview(s : String) : Review =  {
    print("*****************************")
    val json = parseJSON(s)
    print("*****************************")
    Review(Some(json("author_id").toString),
      Some(json("title").toString),
      Some(json("review_date").toString),
      Some(json("content").toString),
      Some(json("title_score").toString),
      Some(json("content_score").toString))
  }
}
