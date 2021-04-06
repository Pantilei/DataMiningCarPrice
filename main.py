import asyncio
from fetch import fetch
from parse.parse import ParseHTML

from typing import Coroutine, Iterator

MAIN_URL: str = "https://999.md"
URL_CARS: str = f"{MAIN_URL}/ru/list/transport/cars"


async def get_number_of_pgs() -> int:
    """Get number of available pages

    :return: Number of pages 
    :rtype: int
    """
    main_html: Coroutine[str] = await fetch.fetch_html(URL_CARS)
    main_html_obj: ParseHTML = ParseHTML(main_html)
    num_of_pgs: int = main_html_obj.get_number_of_pages()

    return num_of_pgs


async def get_pages_content(num_of_pgs: int) -> list[str]:
    """Get pages content 

    :param num_of_pgs: Number of pages
    :type num_of_pgs: int
    :return: List of pages content
    :rtype: list[str]
    """
    all_htmls: list[str] = [
        f"{URL_CARS}?page={i}" for i in range(num_of_pgs+1)]
    all_pages_content: Coroutine[list[str]] = await fetch.fetch_all_batch(all_htmls)

    return all_pages_content


# Make this function generator
def get_product_endpoints(html: str) -> list[str]:
    """Get product endpoints from HTML

    :param html: HTML document
    :type html: str
    :return: List of product endpoints
    :rtype: list[str]
    """
    page_html: ParseHTML = ParseHTML(html)
    product_urls: list[str] = page_html.get_product_urls()

    return product_urls


def get_all_product_endpoints(pages_content: Iterator) -> list[str]:
    """Get all product endpoints from list of htmls

    :param pages_content: HTML of pages
    :type pages_content: Iterator
    :return: List of product endpoints
    :rtype: list[str]
    """
    all_product_endpoints: list = []
    for page_content in pages_content:
        product_endpoints: list[str] = get_product_endpoints(page_content)
        all_product_endpoints.extend(product_endpoints)

    print(len(all_product_endpoints))
    return all_product_endpoints


async def save_product_endpoints(product_endpoints: list[str]):
    # Send endpoints data to database
    pass


async def main():
    """Main entrance to web parser program
    """
    num_of_pgs: Coroutine[int] = await get_number_of_pgs()
    pages_content: Coroutine[list[str]] = await get_pages_content(num_of_pgs)
    all_product_endpoints: list[str] = get_all_product_endpoints(pages_content)
    await save_product_endpoints(all_product_endpoints)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
