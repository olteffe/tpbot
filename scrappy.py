import requests
import re
from bs4 import BeautifulSoup

import settings
from format import format_phone, format_date


def write_html_page(column: int, page: int):
    """write the html-doc file to the hard disk"""
    req = requests.get(settings.BASE_URL.format(settings.COLUMN_NAME[column], page), headers=settings.HEADERS)
    src = req.text
    with open(f"temp/index{page}.html", "w") as file:
        file.write(src)


def read_html_page(page: int):
    """read one page and return soup-object"""
    with open(f"temp/index{page}.html", "r") as file:
        source = file.read()
    return BeautifulSoup(source, "lxml")


def check_pagination() -> int:
    """Calculate the number of web pages and return it"""
    soup = read_html_page(1)
    soup_string = soup.find("div", class_="link_bar").get_text(separator=",", strip=True)
    temp_list = list(soup_string.split(","))
    if temp_list[-1] == 'следующая →':
        return int(temp_list[-2])
    elif int(temp_list[-1]) == 1:
        return 1


def scrappy_ad_link(page: int, link_list: list) -> list:
    """we get a list of links of single ads"""
    soup = read_html_page(page)
    raw_links = soup.find_all("a", class_="titleline")
    for link in raw_links:
        link_list.append(link.get("href"))
    return link_list


def get_ad_id(list_links: list) -> list:
    """Get a list of ad id"""
    return_list = []
    for ad_id in range(len(list_links)):
        return_list.append(re.sub("[^0-9]", "", list_links[ad_id]))
    return return_list


def parse_single_ad_info(single_id: str, page: int) -> dict:
    """get a single ad of a single web-page"""
    soup = read_html_page(page)
    raw_ad_unit = soup.find("tr", id=re.compile(single_id))
    description = raw_ad_unit.find("a", class_="titleline").get_text(strip=True)
    author = raw_ad_unit.find("a", title=re.compile("найти все объявления автора")).get_text()
    try:
        phone = format_phone(raw_ad_unit.find("div", class_="phone", title="Телефон").get_text())
    except AttributeError:
        phone = "Null"
    date = format_date(raw_ad_unit.find("div", class_="tabdate", style="font-size:11px").get_text(strip=True))
    link = raw_ad_unit.find("a", class_="titleline").get("href")
    return {"link": link, "author": author, "description": description, "phone": phone, "date": date}


def get_all_ads_in_page(page: int, dict_page_list: list) -> list:
    """Parsing all ads in single web page"""
    all_links_in_page = scrappy_ad_link(page, [])  # get all ad links in single page
    all_page_id = get_ad_id(all_links_in_page)  # convert links into ad id
    for ads in all_page_id:   # get all ads from single page
        dict_page_list.append(parse_single_ad_info(ads, page))
    return dict_page_list


def get_all_ads() -> list:
    """Parsing all ads in all web pages"""
    out_dict_list = []
    const_rubric = 0  # TODO Its temporarily. You will get it from telegram package
    write_html_page(const_rubric, 1)  # write first page for check_pagination()
    amount_of_page = check_pagination()  # check how many pages
    for page in range(2, amount_of_page + 1):  # save all the other pages
        write_html_page(const_rubric, page)
    for single_page in range(1, amount_of_page + 1):  # all info
        get_all_ads_in_page(single_page, out_dict_list)
    return out_dict_list


if __name__ == '__main__':
    print(get_all_ads())
