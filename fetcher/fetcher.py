from curl_cffi.requests import AsyncSession
from utils.logger import logger_init
from config.headers import SITEMAP_HEADERS, PDP_HEADERS

logger = logger_init()


class Fetcher:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = AsyncSession(impersonate="chrome124")
        return self

    async def __aexit__(self, type, value, tb):
        if self.session:
            await self.session.close()

    async def fetch_sitemap(self, sitemap_url: str) -> str | None:
        try:
            response = await self.session.get(
                url=sitemap_url, headers=SITEMAP_HEADERS, timeout=10
            )
            if response.status_code == 200:
                logger.info("Sitemap fetched")
                return response.text

            logger.error(
                f"Sitemap fetch error: {response.url}\n"
                f"Status: {response.status_code}\n"
                f"Text: {response.text[:3000]}\n"
            )
            return None

        except Exception as e:
            logger.exception(e)
            return None

    async def fetch_pdp(self, pdp_url: str) -> str | None:
        try:
            response = await self.session.get(
                url=pdp_url, headers=PDP_HEADERS, timeout=10
            )
            if response.status_code == 200:
                logger.info("Pdp fetched")
                return response.text

            logger.error(
                f"Pdp fetch error: {response.url}\n"
                f"Status: {response.status_code}\n"
                f"Text: {response.text[:3000]}\n"
            )
            return None
        except Exception as e:
            logger.exception(e)
            return None
