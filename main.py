import asyncio

import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

BASE_URL = "https://www.technodom.kz/p/noutbuk-16-asus-vivobook-s16-ci5-210h-16-512-ds3607va-rp105-294725"
HEADERS = {"User-Agent": UserAgent().random}


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            html = await response.text()
            soup = BS(html, 'html.parser')

            items =soup.find_all("h1", {"class": "Typography ProductInfoMobileSmall_title__6HplU Typography__XL"})
            for item in items:
                print(item.get_text(strip=True))


if __name__ == "__main__":
    asyncio.run(main())