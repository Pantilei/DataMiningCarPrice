from bs4 import BeautifulSoup
import logging
import traceback

_logger = logging.Logger(__name__)


class ParseHTML():
    def __init__(self, html):
        self.html = html
        self.soup_html = BeautifulSoup(html, "html.parser")
        self.soup_html.decode("UTF-8")

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

    def get_product_data(self):
        """Extract data of product from html page

        :return: Dictionary of data
        :rtype: dict
        """
        try:
            data = {}
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

    def get_product_features(self):
        """Get product features

        :return: Feature dict
        :rtype: dict
        """
        try:
            data = {}
            features = self.soup_html.find_all(class_="m-value")
            for feature in features:
                data[feature.find(itemprop="name").string] = feature.find(
                    itemprop="value").string

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_price(self):
        """Get product price from html

        :return: Product price dict
        :rtype: dict
        """
        try:
            data = {}
            price_container = self.soup_html.select(
                ".adPage__content__price-feature__prices__price.is-main")
            price = price_container[0].find(itemprop="price")["content"]
            currency = price_container[0].find(
                itemprop="priceCurrency")["content"]
            data["price"] = f"{price} {currency}"

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_region(self):
        """Get product region

        :return: Data dict
        :rtype: dict
        """
        try:
            data = {}
            region_container = self.soup_html.find(
                class_="adPage__content__region")
            address_country = region_container.find(
                itemprop="addressCountry")["content"]
            address_locality = region_container.find(
                itemprop="addressLocality")["content"]
            data["address_country"] = address_country
            data["address_locality"] = address_locality

            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)

    def get_product_description(self):
        """Get product description

        :return: Data dict
        :rtype: dict
        """
        try:
            data = {}
            description = self.soup_html.find(itemprop="description").string
            data["description"] = description
            return data
        except Exception as ex:
            _logger.error(traceback.format_exc())
            return str(ex)


# with open("test.html", "r", encoding='UTF-8') as f:
#     html = f.read()
#     html_obj = ParseHTML(html)
#     print(html_obj.get_product_data())
