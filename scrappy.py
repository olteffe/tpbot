import requests
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
    link_list, ad_name_list, author_list = [], [], []
    raw_links = soup.find_all("a", class_="titleline")  # and raw_ad_name
    for link in raw_links:
        link_list.append(link.get("href"))
    # print(link_list)
    for ad_name in raw_links:
        ad_name_list.append(ad_name.get_text(separator=" "))
    # print(ad_name_list)
    raw_author = soup.find_all("td", class_="col-author")
    for author in raw_author:
        author_list.append(author.get_text(separator=", "))
    # print(author_list)
    all_ad_list = list(zip(link_list, ad_name_list, author_list))
    print(all_ad_list)
    # TODO remove \n


def check_pagination():
    pass


def scrappy_agency_number():
    pass


def save_in_db():
    pass


if __name__ == '__main__':
    write_page_html()
    scrappy_ad_info()
    # list_links = []
    # scrappy_url_page()
    # print(list_links, len(list_links))
