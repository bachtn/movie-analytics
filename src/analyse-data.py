#!/usr/bin/env python

from kafka import KafkaConsumer, KafkaProducer
import json
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import unicodedata



def get_text_score(text):
    """
    TextBlob(post).sentiment return a tuple of form (polarity,
    subjectivity ) where polarity is a float within the range
    [-1.0, 1.0] and subjectivity is a float within the range
    [0.0, 1.0] where 0.0 is very objective and 1.0 is very
    subjective.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode('utf-8')
    text_score = 0
    for sentence in TextBlob(text).sentences:
        text_score += sentence.polarity if sentence.subjectivity == 0 \
                else sentence.polarity * sentence.subjectivity
    return "%.2f" % text_score

def get_movie_popularity(movie_score):
    if (movie_score > 1):
        return 5
    elif (movie_score > 0.5):
        return 2
    elif (movie_score < 0):
        return -2


def send_message(producer, movie_dict, topic_name, key):
    json_str_dump = json.dumps(movie_dict)
    producer.send(topic_name, key=b'movie', value=json_str_dump.encode('ascii'))

def sentiment_analysis(topic_name):
    consumer = KafkaConsumer(topic_name, group_id='kafka-streaming-example', bootstrap_servers=['localhost:9092'])
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    nbr_message = 0
    for message in consumer:
        nbr_message += 1
        consumer.commit()
        movie_dict = json.loads(message.value.decode('utf-8'))
        print("Received message " + str(nbr_message) + ", movie title = " + movie_dict['title'])
        reviews = movie_dict['reviews']
        updated_reviews = []
        movie_popularity = 0
        for i in range(len(reviews)):
            review = json.loads(reviews[i])
            title_score = get_text_score(review["title"])
            content_score = get_text_score(review["content"])
            movie_popularity += get_movie_popularity(title_score * 0.4 + content_score * 0.6)
            review.update({'title_score': title_score, 'content_score': content_score})
            updated_reviews.append(review)
        movie_dict.update({'reviews': updated_reviews, 'popularity_from_reviews': str(movie_popularity)})
        send_message(producer, movie_dict, 'movie_popularity', 'movie_sentiment')

sentiment_analysis('movie_data')
