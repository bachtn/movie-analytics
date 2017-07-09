# movie-analytics
# Files
## collect-data.py :
collects data about movies and publish it in a kafka stream topic called: 'movie\_data'

## review-collector.py :
Is used by 'collect-data.py' to collect the movie reviews

## imdbpy.py : (is no longer used in the project) 
Collects data with imdbpy api but because there is a connection problem, it was replaced with the tmdbsimple api.

## analyse-data.py :
Uses a consumer to listen to the Kafka topic 'movie\_data', and for each message (data for a single movie), analyse its reviews and assigns a score for each one. and than the results are published in a new topic called 'movie\_popularity'
