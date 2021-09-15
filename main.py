from infra.mongodb.mongo import get_mongo_connection
from service.scrape_companies import scrape_companies
from service.scrape_brands import scrape_brands
from service.scrape_pagination_limit import scrape_pagination_limit

if __name__ == '__main__':
    conn = get_mongo_connection()
    company_arr = []
    # # Scrape all companies from all six pages
    for page in range(6, 7):
        company_arr = company_arr + scrape_companies(conn, page)

    for company in company_arr:
        print(company['name'])
        limit = scrape_pagination_limit(company['link'])
        company['limit'] = limit
        for page in range(1, company['limit']):
            scrape_brands(conn, company['name'], company['link'], page)
