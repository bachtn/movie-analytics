#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bs

url = 'http://akas.imdb.com/title/tt0000001' + '/reviews'
r = requests.get(url)
soup = bs(r.content, "html.parser")


def review_filter(tag):
    return not(tag.has_attr('class')) and not(tag.has_attr('id')) \
            and tag.find("h2")

for review_container in soup.find_all('div', class_=False, id_=False):
    if (review_filter(review_container)):
        author_id = review_container.find("a").get("href").split('/')[2]
        title = review_container.find("h2").get_text()
        review_date = review_container.find_all("small")[-1].get_text()
        content = review_container.find_next_sibling().get_text()
        print(author_id)
        print(review_date)
        print(title)
        print(content)
