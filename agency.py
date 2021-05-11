from bs4 import BeautifulSoup
import requests

import settings


def write_agency_html(page: int):
    """write in html file"""
    req = requests.get(settings.AGENCY_URL.format(page), headers=settings.HEADERS)
    src = req.text
    with open(f"agency{page}.html", "w") as file:
        file.write(src)


def get_page_count(page: int) -> int:
    """return total number of agency pages"""
    with open(f"agency{page}.html", "r") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    return int(soup.find("span", class_="pagelinklast").get_text())


def scrappy_agency_name(page: int, agency_list: list) -> list:
    """collects the agency name from a single page"""
    with open(f"agency{page}.html", "r") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    agency_raw = soup.find_all("h2", style="padding-top:0px")
    for agency in agency_raw:
        agency_list.append(agency.get_text().strip())
    return agency_list


def scrappy_agency_phone(page: int, agency_phone_list: list) -> list:
    """collects agency phone numbers from a single page"""
    with open(f"agency{page}.html", "r") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    agency_phone_raw = soup.find_all("div", "span", class_="anrybls")
    for agency_phone in agency_phone_raw:
        if "Телефон:" in agency_phone.get_text().strip():
            agency_phone_list.append(agency_phone.get_text().strip())
    return agency_phone_list


def get_all_agency() -> list:
    """we take all the data and import it into the main file scrappy.py"""
    all_agency_list, all_phone_list = [], []
    write_agency_html(1)
    agency_page_count = get_page_count(1)
    for pages in range(2, agency_page_count + 1):
        write_agency_html(pages)
    for names in range(1, agency_page_count + 1):
        scrappy_agency_name(names, all_agency_list)
    for phones in range(1, agency_page_count + 1):
        scrappy_agency_phone(phones, all_phone_list)
    return list(zip(all_agency_list, all_phone_list))
