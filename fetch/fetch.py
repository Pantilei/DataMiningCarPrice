import asyncio
import aiohttp
import logging
import traceback

_logger = logging.Logger(__name__)


async def fetch(session, url):
    """Fetches given url and session object

    :param session: aiohttp object
    :type session: obj
    :param url: url to be feched
    :type url: str
    :return: Fetched html
    :rtype: str
    """
    try:
        async with session.get(url) as response:
            # return await response.text(encoding="utf-8")
            return await response.text()
    except Exception as ex:
        _logger.error(traceback.format_exc())
        return str(ex)


async def fetch_html(url):
    """Fetch the url

    :param url: Endpoint to fech
    :type url: str
    :return: Fetched html
    :rtype: str
    """
    try:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)

            return html
    except Exception as ex:
        _logger.error(traceback.format_exc())
        return str(ex)


async def fetch_all(urls):
    """Fetch list of urls

    :param urls: List of urls
    :type urls: list
    :return: List of htmls
    :rtype: list
    """
    try:
        htmls = await asyncio.gather(*[fetch_html(url) for url in urls])

        return htmls
    except Exception as ex:
        _logger.error(traceback.format_exc())
        return str(ex)


async def fetch_all_batch(urls, batch=50):
    """Fetch the urls in baches

    :param urls: list of urls to be feched
    :type urls: list
    :param batch: Number of urls to fech at the same time, defaults to 50
    :type batch: int, optional
    :return: list of fetches urls
    :rtype: list
    """
    try:
        all_htmls = []
        num_of_urls = len(urls)
        for j in range(0, num_of_urls+batch, batch):
            step = j+batch if j+batch < num_of_urls else num_of_urls+1
            all_htmls.extend(await fetch_all(urls[j:step]))

        return all_htmls
    except Exception as ex:
        _logger.error(traceback.format_exc())
        return str(ex)
