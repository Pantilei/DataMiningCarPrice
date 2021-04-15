from bs4 import BeautifulSoup
from logging import Logger
from typing import Iterator
import traceback

_logger: Logger = Logger(__name__)


class ParseHTML():
    def __init__(self, html: str):
        self.html: str = html
        self.soup_html: BeautifulSoup = BeautifulSoup(html, "html.parser")
        self.soup_html.decode("UTF-8")

    def get_number_of_pages(self) -> int:
        """Get number of pages of products

        :return: Number of pages
        :rtype: int
        """
        try:
            last_page_obj: BeautifulSoup = self.soup_html.find(
                class_="is-last-page")
            href: str = last_page_obj.find("a")["href"]
            page: int = int(href.split("page=")[1])
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

        return page

    def get_product_urls(self) -> list[str]:
        """Get url of products

        :return: Product endpoints
        :rtype: list
        """
        try:
            products: Iterator[BeautifulSoup] = self.soup_html.find_all(
                class_="ads-list-photo-item-title")
            product_hrefs: list[str] = [product.find(
                "a")["href"] for product in products]

            return product_hrefs
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_data(self) -> dict[str, str]:
        """Extract data of product from html page

        :return: Dictionary of data
        :rtype: dict
        """
        try:
            data: dict = {}
            # Get features
            data.update(self.get_product_features())
            # Get price
            data.update(self.get_product_price())
            # Get region
            data.update(self.get_product_region())
            # Get product description
            data.update(self.get_product_description())

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_features(self) -> dict[str, str]:
        """Get product features

        :return: Feature dict
        :rtype: dict
        """
        try:
            data: dict = {}
            features: Iterator[BeautifulSoup] = self.soup_html.find_all(
                class_="m-value")
            for feature in features:
                data[feature.find(itemprop="name").string] = feature.find(
                    itemprop="value").string

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_price(self) -> dict[str, str]:
        """Get product price from html

        :return: Product price dict
        :rtype: dict
        """
        try:
            data: dict = {}
            price_container: list[BeautifulSoup] = self.soup_html.select(
                ".adPage__content__price-feature__prices__price.is-main")
            price: str = price_container[0].find(itemprop="price")["content"]
            currency: str = price_container[0].find(
                itemprop="priceCurrency")["content"]
            data["price"] = f"{price} {currency}"

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_region(self) -> dict[str, str]:
        """Get product region

        :return: Data dict
        :rtype: dict
        """
        try:
            data: dict = {}
            region_container: BeautifulSoup = self.soup_html.find(
                class_="adPage__content__region")
            address_country: str = region_container.find(
                itemprop="addressCountry")["content"]
            address_locality: str = region_container.find(
                itemprop="addressLocality")["content"]
            data["address_country"] = address_country
            data["address_locality"] = address_locality

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_description(self) -> dict[str, str]:
        """Get product description

        :return: Data dict
        :rtype: dict
        """
        try:
            data: dict = {}
            description: str = self.soup_html.find(
                itemprop="description").string
            data["description"] = description
            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)


# with open("test.html", "r", encoding='UTF-8') as f:
#     html = f.read()
#     html_obj = ParseHTML(html)
#     print(html_obj.get_product_data())
