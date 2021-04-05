from bs4 import BeautifulSoup
import logging
import traceback

_logger = logging.Logger(__name__)


class ParseHTML():
    def __init__(self, html):
        self.html = html
        self.soup_html = BeautifulSoup(html, "html.parser")

    def get_number_of_pages(self):
        """Get number of pages of products

        :return: Number of pages
        :rtype: int
        """
        try:
            last_page_obj = self.soup_html.find(class_="is-last-page")
            href = last_page_obj.find("a")["href"]
            page = int(href.split("page=")[1])
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

        return page

    def get_product_urls(self):
        """Get url of products

        :return: Product endpoints
        :rtype: list
        """
        try:
            products = self.soup_html.find_all(
                class_="ads-list-photo-item-title")
            product_hrefs = [product.find("a")["href"] for product in products]

            return product_hrefs
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)
