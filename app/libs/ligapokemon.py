from pathlib import Path
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from app.domain.schemas import CardLoad, EditionLoad


class LigaPokemon:
    """Class for webscraping data from Liga Pokemon website."""

    def __init__(self) -> None:
        """Initialize a LigaPokemon instance.

        :param self: The LigaPokemon instance
        """
        self.data = None
        self.URL_BASE = "https://www.ligapokemon.com.br"

    def _load_data(self, url: str) -> None:
        """Load data from a given URL.

        :param self: The LigaPokemon instance
        :param url: The URL to load data from
        :type url: str
        """
        if self.data:
            return

        data = None

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            data = page.content()
            browser.close()

        self.data = BeautifulSoup(data, "html.parser")

    def load_image(self, url: str, filename: str) -> None:
        """Load image data from a given URL.

        :param self: The LigaPokemon instance
        :param url: The URL to load image from
        :type url: str
        :param filename: The filename to save the image as
        :type filename: str
        """
        response = httpx.get(url)
        response.raise_for_status()

        with Path(filename).open("wb") as f:
            f.write(response.content)

    def get_edition(self) -> EditionLoad:
        """Fetch available editions from the league.

        :param self: The LigaPokemon instance
        :return: Dictionary of edition codes and names
        :rtype: dict[str, str]
        """
        params = {
            "code": self.data.select_one(".sigla-edition").text.strip(),
            "name": self.data.select_one(".name-edition").text.strip(),
            "year": self.data.select_one(".year-edition").text.strip(),
        }

        return EditionLoad.model_validate(params)

    def get_card(self, card_id: str, set_id: str, edition_slug: str) -> CardLoad:
        """Fetch data for a specific card in a league.

        :param self: The LigaPokemon instance
        :param card_id: ID of the card to fetch
        :type card_id: str
        :param set_id: ID of the set to fetch
        :type set_id: str
        :param edition_slug: Edition code of the card
        :type edition_slug: str
        :return: Card load schema
        :rtype: CardLoad
        """
        params = {"view": "cards/search", "card": f"{card_id}/{set_id}", "ed": edition_slug}
        url = f"{self.URL_BASE}/?{urlencode(params)}"

        self._load_data(url)

        params = {
            "card_id": card_id,
            "set_id": set_id,
            "edition_code": edition_slug,
            "name": self.data.select_one(".item-name").text.strip(),
            "rarity": self.data.select_one("#details-screen-rarity").text.strip(),
        }

        return CardLoad.model_validate(params)
