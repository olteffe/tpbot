import requests
import re
from bs4 import BeautifulSoup

import settings


def write_page_html():
    req = requests.get(settings.BASE_URL.format(settings.COLUMN_NAME[0], 1), headers=settings.HEADERS)  # temporary page=1
    src = req.text
    with open("index.html", "w") as file:
        file.write(src)


def scrappy_ad_info():
    with open("index.html", "r") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    link_list, ad_description_list, author_list = [], [], []
    raw_links = soup.find_all("a", class_="titleline")  # and raw_ad_name
    for link in raw_links:
        link_list.append(link.get("href"))
    for ad_description in raw_links:
        ad_description_list.append(re.sub(r'\s+', ' ', ad_description.get_text()).strip())
    raw_author = soup.find_all("td", class_="col-author")
    for author in raw_author:
        author_list.append(re.sub(r'\s+', ' ', author.get_text(",")).strip())
    all_ad_list = list(zip(link_list, ad_description_list, author_list))


def check_pagination() -> int:
    """return total number of pages"""
    with open("index.html", "r") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    soup_string = soup.find("div", class_="link_bar").get_text(separator=",", strip=True)
    temp_list = list(soup_string.split(","))
    if temp_list[-1] == 'следующая →':
        return int(temp_list[-2])
    elif int(temp_list[-1]) == 1:
        return 1


def scrappy_agency_number():
    pass


def save_in_db():
    pass


if __name__ == '__main__':
    write_page_html()
    scrappy_ad_info()
    # print(check_pagination())
    # list_links = []
    # scrappy_url_page()
    # print(list_links, len(list_links))
