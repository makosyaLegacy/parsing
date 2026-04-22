import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

BASE_URL = "https://www.technodom.kz/p/noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725"
REVIEWS_API_URL = "https://www.technodom.kz/_next/data/inpxdjJzMPDbMZ44-hcpJ/almaty/p/noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725/reviews.json?uri=noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725"
HEADERS = {"User-Agent": UserAgent().random}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            html = await response.text()
            soup = BS(html, 'html.parser')

            name = soup.find("h1", {"class": "Typography ProductInfoMobileSmall_title__6HplU Typography__XL"})
            price = soup.find("p", {"class": "Typography ProductPricesVariantB_accented__n2rtH Typography__Heading Typography__Heading_H1"})
            rating = soup.find("p", {"class": "Typography RatingAndReviewsCount_rating__evIGS Typography__Caption Typography__Caption_Bold"})

            specs_data = {}
            specs = soup.find_all("div", class_=re.compile(r"Description_item"))
            for spec in specs:
                key = spec.find("p", class_=re.compile(r"Description_leftText"))
                value = spec.find("p", class_=re.compile(r"Description_rightText"))
                if key and value:
                    specs_data[key.get_text(strip=True)] = value.get_text(strip=True)

            for key, value in specs_data.items():
                print(f"{key}: {value}")

            print(f"Название: {name.get_text(strip=True)}")
            print(f"Цена: {price.get_text(strip=True)}")
            print(f"Рейтинг: {rating.get_text(strip=True)}")

        async with session.get(REVIEWS_API_URL, headers=HEADERS) as api_response:
            if api_response.status == 200:
                json_data = await api_response.json()

                page_props = json_data.get("pageProps", json_data)
                initial_data = page_props.get("productReviewsInitialData", {})
                review_data = initial_data.get("reviewData", {})
                reviews_list = review_data.get("reviews", [])

                for i, review in enumerate(reviews_list, 1):
                    text = review.get("text", "Без текста")
                    print(f"{i}. {text}")





if __name__ == "__main__":
    asyncio.run(main())