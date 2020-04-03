import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")

opts = options.Options()
opts.headless = True
browser = webdriver.Chrome(options=opts)
browser.implicitly_wait(6)


def get_item(item_url):
    logging.info(item_url)
    item_browser = webdriver.Chrome(options=opts)
    item_browser.implicitly_wait(6)
    item_browser.get(item_url)
    root = item_browser.find_element_by_tag_name("h2").text.replace("कृदन्त - ", "").strip()
    data_rows = item_browser.find_element_by_css_selector(".declension").find_elements_by_css_selector(".row")
    body_data = [root]
    headwords = [root]
    for row in data_rows:
        if row.text.strip().startswith("कृत"):
            continue
        body_data.append(row.text.replace("\n",  " = "))
        values = row.find_element_by_css_selector(".col-8").text.split(" - ")
        headwords.extend(values)
    item_browser.close()
    return (headwords, "\\n".join(body_data))


def get_entries_from_list(list_id):
    list_url = "http://sanskritabhyas.in/hi/Kridanta/List/%d" % (list_id)
    browser.get(list_url)
    item_elements = browser.find_elements_by_css_selector(".listWord")
    items = []
    for item_element in item_elements:
        item_url = item_element.get_attribute("href")
        item = get_item(item_url)
        items.append(item)
    # logging.debug(items)
    return items


def dump_dict(outfile_path):
    os.makedirs(name=os.path.dirname(outfile_path), exist_ok=True)
    with open(outfile_path, "w") as outfile:
        for list_id in range(1, 13):
            items = get_entries_from_list(list_id=list_id)
            for item in items:
                outfile.writelines(["|".join(item[0]), item[1]], "")


if __name__ == '__main__':
    # logging.debug(get_item("http://sanskritabhyas.in/hi/Kridanta/View/%E0%A4%AD%E0%A5%82"))
    dump_dict("/home/vvasuki/indic-dict/stardict-sanskrit-vyAkaraNa/kRdanta-sa/kRdanta-sa.babylon")