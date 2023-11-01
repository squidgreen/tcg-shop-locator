import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

@dataclass
class SellerInfo:
    """Contains tcgplayer seller info"""
    shop: str
    hyperlink: str
    rating: float
    num_sales: int
    location: str

    def __repr__(self):
        return f"SellerInfo({self.shop},{self.hyperlink},{str(self.rating)},{str(self.num_sales)},{self.location})"
    
    def __str__(self):
        return f"{self.shop},{self.hyperlink},{str(self.rating)},{str(self.num_sales)},{self.location}"

def get_tcgplayer_pages() -> List[str]:
    """
    Requests pages from tcgplayer containing lists of shop data. Return each page's
    html.
    """
    page_contents = []
    last_page = 484
    headers = {
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Host': 'store.tcgplayer.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'user-agent': 'location-app'
    }
    payload = {
        'isDirect': 'False',
        'isGoldStar': 'False',
        'isCertified': 'False',
        'categoryId': '1',
        'page': '1'
    }
    url = 'https://store.tcgplayer.com/sellers'

    for page_num in range(1, last_page + 1):
        payload['page'] = str(page_num)
        r = requests.get(url=url, headers=headers, params=payload)
        # TODO maybe try to grab each page, and return what we were able to grab if we
        # do eventually fail
        if r.status_code == requests.codes.ok:
            page_contents.append(r.text)
            print(f"Grabbed page {page_num}")
        else:
            print(f"ERROR {r.status_code} returned from request: {r.url}")
            exit()
        time.sleep(3)

    return page_contents

def make_soup(page_texts: List[str]) -> List[BeautifulSoup]:
    """
    Convert each page to a BeautifulSoup object and extract only the seller data section
    for further parsing.
    """
    seller_sections = []
    for page in page_texts:
        soup = BeautifulSoup(page, 'lxml')
        seller_sections.extend(soup.find_all(class_='scContent'))

    return seller_sections

def get_seller_data(sellers_soup: List[BeautifulSoup]) -> List[SellerInfo]:
    parsed_data = []
    for seller_data in sellers_soup:
        parsed_data.append(parse_seller_data(seller_data))
    
    return parsed_data

def parse_seller_data(site_page: BeautifulSoup):
    """
    Given a BeautifulSoup object representing one block of seller data, parse seller
    name, location, rating, and shop hyperlink into a object with accessible fields.
    """
    shop_info_strs = []
    shop_link = site_page.find(class_='scTitle').a['href'].strip()
    for text in site_page.strings:
        if text.strip():    # if the string is non-empty
            shop_info_strs.append(text.strip())

    shop_name = shop_info_strs[0]
    if shop_info_strs[1].startswith('Rating: '):
        sales_data_split = shop_info_strs[1].split('%')
        rating = float(sales_data_split[0].removeprefix('Rating: '))
    
        # TODO, add check if there is no num_sales present - set to -1?
        try:
            num_sales = int(re.findall('\d+', sales_data_split[1])[0])
        except IndexError:
            num_sales = -1
    else:
        rating = float(-1)
    if shop_info_strs[2].startswith('Location: '):
        shop_location = shop_info_strs[2].removeprefix('Location: ')
    else:
        shop_location = "XX"
    new_item = SellerInfo(shop_name, shop_link, rating, num_sales, shop_location)

    return new_item

def write_seller_data(seller_info: List[SellerInfo]):
    timestamp = datetime.now().strftime("%a_%d_%b_%Y_%I_%M%p")
    filename = f"sellers_{timestamp}.txt"
    headers = "shop_name, hyperlink, rating, num_sales, location"
    with open(filename, 'a') as fp:
        fp.write(f"{headers}\n")
        seller_strs = [f"{str(seller)}\n" for seller in seller_info]
        fp.writelines(seller_strs)

if __name__ == '__main__':
    html_pages = get_tcgplayer_pages()
    html_soup = make_soup(html_pages)
    seller_data = get_seller_data(html_soup)
    write_seller_data(seller_data)
