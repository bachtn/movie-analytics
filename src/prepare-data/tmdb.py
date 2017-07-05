#!/usr/bin/env python

import tmdbsimple as tmdb
import requests
tmdb.API_KEY = '8689043e90cbfef442156fd038279ade'

from scraper import *


def collect_movie_informations(movie_ids):
    nbr_good_movies = 0
    for movie_id in movie_ids:
        try:
            movie = tmdb.Movies(movie_id)
            response = movie.info()
            movie_url = 'http://akas.imdb.com/title/' + str(movie.imdb_id)
            print(movie_url)
            reviews = get_movie_reviews(movie_url)
            nbr_good_movies += 1
            movie_object = { \
                    'title': movie.title, \
                    'release_date': movie.release_date, \
                    'popularity': movie.popularity, \
                    'budget': movie.budget, \
                    'movie_url': movie_url, \
                    'reviews': reviews \
                    }
            print('title = ' + movie.title + ', nbr review = ' + str(len(reviews)))
        except Exception as e:
            #print(str(e))
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
collect_movie_informations(movie_ids)
