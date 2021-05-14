import requests
import re
from bs4 import BeautifulSoup

import settings
import agency


def write_html_page(column: int, page: int):
    req = requests.get(settings.BASE_URL.format(settings.COLUMN_NAME[column], page), headers=settings.HEADERS)
    src = req.text
    with open(f"index{page}.html", "w") as file:
        file.write(src)


def read_html_page(page: int):
    """read one page and return soup-object"""
    with open(f"index{page}.html", "r") as file:
        source = file.read()
    return BeautifulSoup(source, "lxml")


def check_pagination() -> int:
    """return total amount of ad pages"""
    soup = read_html_page(1)
    soup_string = soup.find("div", class_="link_bar").get_text(separator=",", strip=True)
    temp_list = list(soup_string.split(","))
    if temp_list[-1] == 'следующая →':
        return int(temp_list[-2])
    elif int(temp_list[-1]) == 1:
        return 1


def scrappy_ad_link(page: int, link_list: list) -> list:
    soup = read_html_page(page)
    raw_links = soup.find_all("a", class_="titleline")
    for link in raw_links:
        link_list.append(link.get("href"))
    return link_list


def scrappy_ad_description(page: int, ad_description_list: list) -> list:
    soup = read_html_page(page)
    raw_description = soup.find_all("a", class_="titleline")
    for ad_description in raw_description:
        ad_description_list.append(re.sub(r'\s+', ' ', ad_description.get_text()).strip())
    return ad_description_list


def scrappy_ad_author(page: int, ad_author_list: list) -> list:
    soup = read_html_page(page)
    raw_author = soup.find_all("a", title=re.compile("найти все объявления автора"))
    for author in raw_author:
        ad_author_list.append(author.get_text())
    return ad_author_list


def scrappy_ad_phone(page: int, ad_phone_list: list) -> list:
    soup = read_html_page(page)
    raw_phone = soup.find_all("div", class_="phone", title="Телефон")
    for phone in raw_phone:
        ad_phone_list.append(phone.get_text())
    return ad_phone_list


def scrappy_ad_date(page: int, ad_date_list: list) -> list:
    soup = read_html_page(page)
    raw_date = soup.find_all("div", class_="tabdate", style="font-size:11px")
    for date in raw_date:
        ad_date_list.append(date.get_text())
    return ad_date_list


def get_all_ads() -> list:
    all_link_list, all_description_list, all_author_list, all_phone_list, all_date_list = [], [], [], [], []
    write_html_page(const_rubric, 1)
    amount_ad_page = check_pagination()
    for ad_page in range(2, amount_ad_page + 1):
        write_html_page(const_rubric, ad_page)
    for ad_link in range(1, amount_ad_page + 1):
        scrappy_ad_link(ad_link, all_link_list)
    for ad_description in range(1, amount_ad_page + 1):
        scrappy_ad_description(ad_description, all_description_list)
    for ad_author in range(1, amount_ad_page + 1):
        scrappy_ad_author(ad_author, all_author_list)
    for ad_phone in range(1, amount_ad_page + 1):
        scrappy_ad_phone(ad_phone, all_phone_list)
    for ad_date in range(1, amount_ad_page + 1):
        scrappy_ad_date(ad_date, all_date_list)
    return list(zip(all_link_list, all_description_list, all_author_list, all_phone_list, all_date_list))


def save_in_db():
    pass


if __name__ == '__main__':
    const_rubric = 0  # TODO Its temporarily. You will get it from telegram module
    # TODO get_all_ads() dont work correctly: some ad dont have all need data and zip() cut them

