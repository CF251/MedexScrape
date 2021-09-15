import time
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'https://medex.com.bd/companies?page='


def scrape_companies(conn, page):
    # print(BASE_URL + str(page))
    companies = []

    while True:
        try:
            response = urllib.request.urlopen(BASE_URL + str(page))
            break
        except Exception as exp:
            print("Got Exception, Retrying in 60 Seconds", exp.__class__.__name__)
            time.sleep(60)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.findAll("div", {"class": "row"})
    for row in rows:
        content = row.find("div", {"class": "col-xs-12 data-row-top"})
        if content is not None:
            anchor = content.find("a")
            link = anchor.get('href')
            if anchor.text not in companies:
                if '/brands' not in link:
                    link += '/brands'
                companies.append({
                    "name": anchor.text.strip(),
                    "link": link
                })

    # insert_companies(conn, companies)
    return companies[1:len(companies)]


def insert_companies(conn, companies):
    for company in companies:
        obj = {"name": company}
        conn.companies.insert_one(obj)
