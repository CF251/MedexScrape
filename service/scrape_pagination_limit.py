import time
import urllib.request
from bs4 import BeautifulSoup
import re


def scrape_pagination_limit(url):
    while True:
        try:
            response = urllib.request.urlopen(url)
            break
        except Exception as exp:
            print("Got Exception in getting pagination, Retrying in 60 Seconds", exp.__class__.__name__)
            time.sleep(60)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.findAll("a", {"class": "page-link"})
    if len(rows) == 0:
        return int(2)
    else:
        page = rows[len(rows) - 2].text
        return int(page) + 1
