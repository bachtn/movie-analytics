#!/usr/bin/env python

from imdb import IMDb

# Create the object that will be used to access the IMDb's database.
ia = IMDb()

nbr_good_movies = 0
#for movie_id in range(451279, 99999999):
for movie_id in range(99):
    try:
        movie = ia.get_movie(str(movie_id))
        print("title = " + movie['title'] + " " + movie['rating'])
        ia.update(movie, 'release dates')
        #print(movie['release dates'][0])
        #print(movie['year'])
        #print(movie['runtime']) #????
        #print(movie['rating'])
        #print(movie['votes'])
        #print(movie['genres'])
        #print(movie['country'])
        print(ia.get_imdbURL(movie))
        nbr_good_movies += 1
        """
        for person in ia.search_person('Mel Gibson'):
            print(person.personID, person['name'])
        """
    except Exception as e:
        #print(str(e))
        pass

print(nbr_good_movies)
