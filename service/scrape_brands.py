import re
import time
import urllib.request
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import json
from bson.json_util import dumps


def scrape_brands(conn, company_name, url, page):
    print(url + '?page=' + str(page))
    response = conn.companies.find_one({"name": company_name})
    company = json.loads(dumps(response))
    company_id = ObjectId(company["_id"]['$oid'])
    brands = []
    while True:
        try:
            response = urllib.request.urlopen(url + '?page=' + str(page))
            break
        except Exception as exp:
            print("Got Exception, Retrying in 60 Seconds", exp.__class__.__name__)
            time.sleep(60)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.findAll("div", {"class": "row"})

    for row in rows:
        cols = row.findAll("div", {"class": "col-xs-12 col-sm-6 col-lg-4"})
        for col in cols:
            contents = col.findAll("div", {"class": "row data-row"})
            for content in contents:
                med_type = content.find("span", {"class": "inline-dosage-form"}).text.strip()
                brand = content.find("div", {"class": "data-row-top"}).text.strip().replace(med_type, '')
                dose = content.find("div", {"class": "data-row-strength"}).text.strip()
                generic_name = content.find("div", {"class": "data-row-strength"}).find_next_sibling("div").text.strip()
                package_wrapper_div = content.find("div", {"class": "packages-wrapper"})
                package_pricing_div = package_wrapper_div.find("span", {
                    "class": "package-pricing"})

                if package_pricing_div is not None:
                    unit_price = package_pricing_div.text.strip()
                else:
                    unit_price = '0.0'

                regex = re.findall("\d+\.\d+", unit_price)
                if len(regex):
                    unit_price = float(regex[0])
                else:
                    unit_price = '0.0'
                obj = {
                    "name": brand,
                    "type": med_type,
                    "dose": dose,
                    "generic_name": generic_name,
                    "unit_price": unit_price,
                    "company_id": company_id
                }
                brands.append(obj)
    insert_brands(conn, brands)


def insert_brands(conn, brands):
    conn.brands.insert_many(brands)
