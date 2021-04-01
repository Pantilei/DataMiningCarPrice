from fetch import fetch
from parse.parse import ParseHTML

url = "https://999.md/ru/list/transport/cars"

html = fetch.start_evet_loop([url])[0]

html_obj = ParseHTML(html)
print(html_obj.get_number_of_pages())
