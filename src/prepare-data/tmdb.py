#!/usr/bin/env python

import tmdbsimple as tmdb
tmdb.API_KEY = '8689043e90cbfef442156fd038279ade'

nbr_good_movie = 0
for movie_id in range (100000, 10000000):
    try:
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        #print(movie.title)
        #print(movie.release_date)
        #print(movie.popularity)
        #print(movie.budget)
        #print("runtime = " + str(movie.runtime))
        #print(movie.translations)
        #print(movie.credits)
        #print(movie.keywords()['keywords'])

        reviews = movie.reviews()
        if (len(reviews["results"])):
            nbr_good_movie += 1
            print(movie.title + " " + str(len(reviews["results"])))
            """
            for r in reviews["results"]:
                print("Author : " + r["author"])
                print("ReviewId: " + r["id"])
                print("Content: " + r["content"])
            """
            
        
    except Exception as e:
        #print(str(e))
        pass

print("number of good movies = " + str(nbr_good_movie))

