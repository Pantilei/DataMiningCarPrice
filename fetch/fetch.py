import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_html(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

        return html


async def fetch_all(urls):
    all_data = await asyncio.gather(*[get_html(url) for url in urls])
    htmls = [a.encode("utf-8") for a in all_data]

    return htmls


def start_evet_loop(urls):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_all(urls))
