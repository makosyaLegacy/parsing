import asyncio
import json
import re

import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

BASE_URL = "https://www.technodom.kz/p/noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725"
REVIEWS_API_URL = "https://www.technodom.kz/_next/data/inpxdjJzMPDbMZ44-hcpJ/almaty/p/noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725/reviews.json?uri=noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725"
HEADERS = {"User-Agent": UserAgent().random}


async def main():

    product_data = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            html = await response.text()
            soup = BS(html, 'html.parser')

            name = soup.find("h1", class_=re.compile(r"ProductInfoMobileSmall_title"))
            price = soup.find("p", {"class": "Typography ProductPricesVariantB_accented__n2rtH Typography__Heading Typography__Heading_H1"})
            rating = soup.find("p", class_=re.compile(r"RatingAndReviewsCount_rating"))

            specs_data = {}
            specs = soup.find_all("div", class_=re.compile(r"Description_item"))
            for spec in specs:
                key = spec.find("p", class_=re.compile(r"Description_leftText"))
                value = spec.find("p", class_=re.compile(r"Description_rightText"))
                if key and value:
                    specs_data[key.get_text(strip=True)] = value.get_text(strip=True)

            product_data["name"] = name.get_text(strip=True) if name else None
            product_data["price"] = price.get_text(strip=True) if price else None
            product_data["rating"] = rating.get_text(strip=True) if rating else None
            product_data["specs"] = specs_data

        product_data["reviews"] = []

        async with session.get(REVIEWS_API_URL, headers=HEADERS) as api_response:
            if api_response.status == 200:
                json_data = await api_response.json()

                page_props = json_data.get("pageProps", json_data)
                initial_data = page_props.get("productReviewsInitialData", {})
                review_data = initial_data.get("reviewData", {})
                reviews_list = review_data.get("reviews", [])

                for review in reviews_list:
                    product_data["reviews"].append(review.get("text", "Без текста"))

    final_json = json.dumps(product_data, indent=4, ensure_ascii=False)
    print(final_json)

if __name__ == "__main__":
    asyncio.run(main())