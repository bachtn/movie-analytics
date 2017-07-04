#!/usr/bin/env python3

#div class reviews > div id tn15main > div id tn15content > 

import requests
from bs4 import BeautifulSoup as bs


def get_review_page_urls(movie_url):
    review_url = movie_url + '/reviews'
    soup = bs(requests.get(review_url).content, "html.parser")
    review_page_urls = []
    review_page_container = soup.find('div', {"id" : "tn15content"}).find_all('table')[1]
    for page_url in review_page_container.find_all("a"):
        review_page_urls.append(movie_url + '/' + page_url.get("href"))
    return set(review_page_urls)

def review_filter(tag):
    return not(tag.has_attr('class')) and not(tag.has_attr('id')) and tag.find("h2")

def get_reviews_in_page(review_page_url):
    reviews = []
    soup = bs(requests.get(review_page_url).content, "html.parser")
    for review_container in soup.find_all('div', class_=False, id_=False):
        if (review_filter(review_container)):
            author_id = review_container.find("a").get("href").split('/')[2]
            title = review_container.find("h2").get_text()
            review_date = review_container.find_all("small")[-1].get_text()
            content = review_container.find_next_sibling().get_text()
            review = {'author_id': author_id, 'title': title, 'review_date': review_date, 'content': content}
            reviews.append(review)
    return reviews

def get_movie_reviews(movie_url):
    review_page_urls = get_review_page_urls(movie_url)
    movie_reviews = []
    for review_page_url in review_page_urls:
        print(review_page_url)
        movie_reviews.extend(get_reviews_in_page(review_page_url))
    return movie_reviews
        

review_url = 'http://akas.imdb.com/title/tt0000001/reviews?start=0'

movie_url = 'http://akas.imdb.com/title/tt0000001'
print(len(get_movie_reviews(movie_url)))
