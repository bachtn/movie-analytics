#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bs
import json

def get_review_page_urls(movie_url):
    """
    Given a movie_url, it returns a list of urls of all review pages.
    In fact, if a movie has more than 10 reviews, each 10 reviews are in a different page.
    """
    # TODO: when there is more than 10 review pages, you must click on the last page to get 20 review pages
    # ... or you can take the number of reviews and scrap until you reach the final page, bare in mind that
    # there is 10 reviews per page
    review_url = movie_url + '/reviews'
    soup = bs(requests.get(review_url).content, "html.parser")
    review_page_urls = []
    review_page_container = soup.find('div', {"id" : "tn15content"}).find_all('table')[1]
    for page_url in review_page_container.find_all("a"):
        review_page_urls.append(movie_url + '/' + page_url.get("href"))
    return set(review_page_urls)

def review_filter(tag):
    """
    Determines if the given tag is a tag of a review div.
    The review div filter has no class and no id, and has a tag h2.
    """
    return not(tag.has_attr('class')) and not(tag.has_attr('id')) and tag.find("h2")

def get_reviews_in_page(review_page_url):
    """
    Given an url of a review page, it iterates over all reviews
    and collects the data of each review, then returns a list
    of a dictionary object that represents a review
    """
    reviews = []
    soup = bs(requests.get(review_page_url).content, "html.parser")
    for review_container in soup.find_all('div'):
        if (review_filter(review_container)):
            author_id = review_container.find("a").get("href").split('/')[2]
            title = review_container.find("h2").get_text()
            review_date = review_container.find_all("small")[-1].get_text()
            content = review_container.find_next_sibling().get_text()
            review = {'author_id': author_id, 'title': title, 'review_date': review_date, 'content': content}
            reviews.append(review)
    return reviews

def get_movie_reviews(movie_url):
    """
    Gets the url of all review pages and than, for each page,
    it gets its reviews.
    Returns a list of all the reviews of the given movie.
    """
    review_page_urls = get_review_page_urls(movie_url)
    movie_reviews = []
    for review_page_url in review_page_urls:
        #print(review_page_url)
        movie_reviews.extend(get_reviews_in_page(review_page_url))
    return movie_reviews
        


"""
movie_url = 'http://akas.imdb.com/title/tt0000001'
review_list = get_movie_reviews(movie_url)
print("number of reviews = " + str(len(review_list)))
reviews_in_json = json.dumps(review_list)
with open('data.json', 'w') as outfile:
    json.dump(reviews_in_json, outfile)
"""

