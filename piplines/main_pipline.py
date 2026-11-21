import asyncio
import argparse

from fetcher.fetcher import Fetcher
from utils.logger import logger_init
from parser.parser import Parser
from storage.scheduler import SchedulerStorage

logger = logger_init()


async def worker(queue, lock, fetcher):
    while True:
        pdp_url = await queue.get()
        try:
            if pdp_url is None:
                return

            pdp_html = await fetcher.fetch_pdp(pdp_url)
            if not pdp_html:
                logger.error("Pdp html is not collected")
                continue

            pdp_data = await asyncio.to_thread(Parser().parse_pdp, pdp_html, pdp_url)
            if not pdp_data:
                logger.error("Pdp data is not parsed")
                continue

            async with lock:
                await asyncio.to_thread(SchedulerStorage().set_pdp_storage, pdp_data)

        except Exception as e:
            logger.exception(e)
        finally:
            queue.task_done()


async def main():
    parser = argparse.ArgumentParser(description="Sitemap collection")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Sitemap URL to process",
    )
    args = parser.parse_args()

    async with Fetcher() as fetcher:
        queue = asyncio.Queue()
        lock = asyncio.Lock()

        sitemap_xml = await fetcher.fetch_sitemap(args.url)
        if sitemap_xml:
            pdp_urls = await asyncio.to_thread(Parser().parse_sitemap, sitemap_xml)
        else:
            logger.error("Sitemap is not collected")
            return

        for pdp_url in pdp_urls:
            await queue.put(pdp_url)

        workers = [asyncio.create_task(worker(queue, lock, fetcher)) for _ in range(5)]

        await queue.join()
        for _ in workers:
            await queue.put(None)
        await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
