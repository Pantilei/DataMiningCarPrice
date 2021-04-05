import asyncio
from fetch import fetch
from parse.parse import ParseHTML

MAIN_URL = "https://999.md"
URL_CARS = f"{MAIN_URL}/ru/list/transport/cars"


async def get_number_of_pgs():
    main_html = await fetch.fetch_html(URL_CARS)
    main_html_obj = ParseHTML(main_html)
    num_of_pgs = main_html_obj.get_number_of_pages()

    return num_of_pgs


async def get_pages_content(num_of_pgs):
    all_htmls = [f"{URL_CARS}?page={i}" for i in range(num_of_pgs+1)]
    all_pages_content = await fetch.fetch_all_batch(all_htmls)

    return all_pages_content


def get_product_endpoints(html):  # Make this function generator
    page_html = ParseHTML(html)
    product_urls = page_html.get_product_urls()
    return product_urls


def get_all_product_endpoints(pages_content):
    all_product_endpoints = []
    for page_content in pages_content:
        product_endpoints = get_product_endpoints(page_content)
        all_product_endpoints.extend(product_endpoints)

    print(len(all_product_endpoints))
    return all_product_endpoints


async def save_product_endpoints(product_endpoints):
    # Send endpoints data to database
    pass


async def main():
    num_of_pgs = await get_number_of_pgs()
    pages_content = await get_pages_content(num_of_pgs)
    all_product_endpoints = get_all_product_endpoints(pages_content)
    await save_product_endpoints(all_product_endpoints)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
