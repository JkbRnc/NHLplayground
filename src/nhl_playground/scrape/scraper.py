import logging

import requests
import yaml
from requests import Response
from nhl_playground.scrape.scrape_utils import setup_logger
from typing import Any


class NHLScraper:
    """NHL scraper class using free api. Provides method for raw data scraping."""

    BASE_API_URL: str = "https://api-web.nhle.com"
    logger: logging.Logger
    ENDPOINTS: dict[str, str]

    def __init__(self, erase: bool = True) -> None:
        """Initialize scraper."""
        self._load_endpoints(path="src/nhl_playground/scrape/endpoints.yaml")
        self.logger = setup_logger("scraperLogger", "scraper.log", erase=erase)

    def _load_endpoints(self, path: str) -> None:
        self.ENDPOINTS = yaml.safe_load(open(path))

    def scrape_raw(
        self,
        endpoint: str,
        scrape_args: dict[str, str],
        overwrite_base: None | str = None,
    ) -> dict[str, Any]:
        """Scrapes data from NHL api and returns unprocessed raw data.

        Args:
            endpoint (str): Endpoint name for NHL api.
            scrape_args (dict[str, str]): Arguments for formatting url.
            overwrite_base (None | str): URL to overwrite base URL. Default None.

        Returns:
            dict: Dictionary containing the raw data. Is empty when an error occures.
        """
        self.logger.info(f"Scraping of {endpoint} data started")
        base_api_url = overwrite_base if overwrite_base else self.BASE_API_URL
        try:
            response: Response = requests.get(
                f"{base_api_url}{self.ENDPOINTS[endpoint].format(**scrape_args)}"
            )
            data: dict[str, Any] = response.json()
            self.logger.info("Scraping finished succesfully")
        except Exception:
            self.logger.warning("Error occured during scraping: {e}")
            data = {}
        return data
