#!/usr/bin/env python

import tmdbsimple as tmdb
import requests
from scraper import *
from kafka import KafkaProducer
import json, sys


tmdb.API_KEY = '8689043e90cbfef442156fd038279ade'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def send_message(movie_dict, topic_name, key):
    json_str_dump = json.dumps(movie_dict)
    producer.send(topic_name, key=b'movie', value=json_str_dump.encode('ascii'))

def collect_movie_informations(movie_ids, limit_reviews_nbr=True, nbr_reviews=20):
    nbr_good_movies = 0
    # Create producer
    for movie_id in movie_ids:
        try:
            movie = tmdb.Movies(movie_id)
            response = movie.info()
            movie_url = 'http://akas.imdb.com/title/' + str(movie.imdb_id)
            rating_nbr_votes = get_movie_ratings(movie_url)
            if not(rating_nbr_votes['review_count'] < nbr_reviews):
                nbr_good_movies += 1
                reviews = get_movie_reviews(movie_url, limit_reviews_nbr, nbr_reviews)
                # TODO: add actors: scrap
                genres = [g['name'] for g in movie.genres]
                print(genres)
                movie_dict = { \
                        'id':  movie_id, \
                        'title': movie.title, \
                        'release_date': str(movie.release_date), \
                        'genres': genres, \
                        'adult': movie.adult, \
                        'popularity': str("%.2f" % movie.popularity), \
                        'rating': str(rating_nbr_votes['rating_value']), \
                        'nbr_votes': str(rating_nbr_votes['nbr_votes']), \
                        'budget': str(movie.budget), \
                        'revenue': str(movie.revenue), \
                        'duration': str(movie.runtime), \
                        'url': movie_url, \
                        'reviews': reviews \
                        }
                print('title = ' + movie.title + ', nbr review = ' + str(len(reviews)))
                send_message(movie_dict, 'movie_data', 'movie')
        except Exception as e:
            print(str(e))
            pass
    print(str(nbr_good_movies))

def get_movies_by_name(movie_names):
    for movie_name in movie_names:
        try:           
            search = tmdb.Search()
            response = search.movie(query=movie_name)
            for s in search.results:
                print(s['title'], s['id'], s['release_date'], s['popularity'])
        except Exception as e:
            #print(str(e))
            pass

movie_ids = [297762, 313369, 364, 324849, 11, 140607, 330459]
movie_names = ['Batman', 'La La Land', 'Wonder women', 'star wars']
#get_movies_by_name(movie_names)
collect_movie_informations(movie_ids, True)
