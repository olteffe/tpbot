import re
from bs4 import BeautifulSoup
import requests

import settings
from format import format_phone


def write_agency_html(page: int) -> None:
    """write in html file"""
    req = requests.get(settings.AGENCY_URL.format(page), headers=settings.HEADERS)
    src = req.text
    with open(f"temp/agency{page}.html", "w") as file:
        file.write(src)


def read_html_page(page: int):
    """read one page and return soup-object"""
    with open(f"temp/agency{page}.html", "r") as file:
        source = file.read()
    return BeautifulSoup(source, "lxml")


def get_page_count(page: int) -> int:
    """return total number of agency pages"""
    soup = read_html_page(page)
    return int(soup.find("span", class_="pagelinklast").get_text())


def scrappy_agency(page: int, agency_list: list) -> list:
    """collects the agency name from a single page"""
    soup = read_html_page(page)
    agency_raw = soup.find_all("div", class_="anryblimg2")
    for agency in agency_raw:
        if agency.find("b", text=re.compile("Телефон:")):
            name = agency.find("h2", style="padding-top:0px").get_text(strip=True)
            phone = format_phone(agency.find("b", text="Телефон:").parent.get_text(strip=True))
            for i in phone:  # each phone in the list refers to one agency
                agency_list.append({"name": name, "phone": i})
        else:
            continue
    return agency_list


def get_all_agency() -> list:
    """we take all the data and import it into the main file"""
    all_agency_list = []
    write_agency_html(1)
    agency_page_count = get_page_count(1)
    for pages in range(2, agency_page_count + 1):
        write_agency_html(pages)
    for agency in range(1, agency_page_count + 1):
        scrappy_agency(agency, all_agency_list)
    return all_agency_list


if __name__ == '__main__':
    print(get_all_agency())
