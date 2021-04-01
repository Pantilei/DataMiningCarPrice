from bs4 import BeautifulSoup
import re


class ParseHTML():
    def __init__(self, html):
        self.html = html
        self.soup_html = BeautifulSoup(html, "html.parser")

    def get_number_of_pages(self):
        try:
            last_page_obj = self.soup_html.find(class_="is-last-page")
            href = last_page_obj.find("a")["href"]
            page = int(href.split("page=")[1])
            # page = re.search()
        except Exception as ex:
            return str(ex)

        return page
