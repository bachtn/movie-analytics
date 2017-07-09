#!/usr/bin/env python

from imdb import IMDb
from scraper import *


def collect_movie_informations(id_list, by_id=True):
    ia = IMDb()
    nbr_good_movies = 0
    #for movie_id in range(451279, 99999999):
    for movie_id in id_list:
        try:
            movie = ia.get_movie(str(movie_id)) if by_id else ia.search_movie(movie_id)
            title = movie['title']
            ia.update(movie, 'release dates')
            release_date = movie['release dates'][0]
            year = movie['year']
            #print(movie['runtime']) #????
            rating = movie['rating']
            nbr_votes = movie['votes']
            genre = movie['genres']
            country = movie['country']
            movie_url = ia.get_imdbURL(movie)
            reviews = get_movie_reviews(movie_url)
            nbr_good_movies += 1
            movie_object = { \
                    'title': title, \
                    'release_date': release_date, \
                    'movie_year': year, \
                    'rating': rating, \
                    'nbr_votes': nbr_votes, \
                    'genre': genre,  \
                    'country': country, \
                    'movie_url': movie_url, \
                    'reviews': reviews \
                    }
            """
            for person in ia.search_person('Mel Gibson'):
                print(person.personID, person['name'])
            """
        except Exception as e:
            #print(str(e))
            pass

collect_movie_informations(range(99))
