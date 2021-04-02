import asyncio
from fetch import fetch
from parse.parse import ParseHTML

MAIN_URL = "https://999.md"
URL_CARS = f"{MAIN_URL}/ru/list/transport/cars"


async def get_number_of_p():
    main_html = await fetch.fetch_html(URL_CARS)
    main_html_obj = ParseHTML(main_html)
    num_of_pgs = main_html_obj.get_number_of_pages()

    return num_of_pgs


def get_products(html):  # Make this function generator
    page_html = ParseHTML(html)
    product_urls = page_html.get_product_urls()
    return product_urls


async def main():
    num_of_pgs = await get_number_of_p()

    pages_content_tasks = [asyncio.create_task(fetch.fetch_html(
        f"{URL_CARS}?page={i}")) for i in range(1, num_of_pgs)]
    results = await asyncio.gather(*pages_content_tasks)
    # print(results[0].encode("utf-8"))
    all_products = []
    for result in results:
        all_products.extend(get_products(result.encode("utf-8")))
    # products = get_products(results[0].encode("utf-8"))
    print(len(all_products))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
