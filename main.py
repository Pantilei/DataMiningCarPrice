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


def get_product_endpoints(html):  # Make this function generator
    page_html = ParseHTML(html)
    product_urls = page_html.get_product_urls()
    return product_urls


async def get_pages_content(num_of_pgs, batch=50):
    all_htmls = [f"{URL_CARS}?page={i}" for i in range(num_of_pgs+1)]
    all_pages_content = await fetch.fetch_all_batch(all_htmls)

    return all_pages_content


async def main():
    num_of_pgs = await get_number_of_pgs()
    pages_content = await get_pages_content(num_of_pgs)

    all_products = []
    i = 0
    for page_content in pages_content:
        print(i)
        product_endpoints = get_product_endpoints(page_content)
        print(len(product_endpoints))
        if len(product_endpoints) == 0:
            print(page_content)
            break
        all_products.extend(get_product_endpoints(
            page_content))
        i += 1
    print(len(all_products))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
