import asyncio
import multiprocessing as mp

from automall_scraper import Automall
from cars24_scraper import CarScraper
from kavak_scraper import KavakScraper
from dubizzle_scraper import DubizzleScraper


async def run_kavak():
    async with KavakScraper(concurrency_api=25, concurrency_details=200) as scraper:
        await scraper.run_scraper()


async def run_automall():
    async with Automall() as automall:
        await automall.run_scraper()


async def run_cars24():
    async with CarScraper() as scraper:
        await scraper.run_scraper(max_pages=50)


async def run_dubizzle():
    async with DubizzleScraper() as scraper:
        await scraper.fetch_data()


def process_wrapper(coro_func):
    asyncio.run(coro_func())


def main():
    scrapers = [run_kavak, run_automall, run_cars24, run_dubizzle]

    with mp.Pool(processes=len(scrapers)) as pool:
        pool.map(process_wrapper, scrapers)


if __name__ == "__main__":
    main()
