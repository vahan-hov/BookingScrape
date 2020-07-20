import pickle

import requests
from lxml import html

base_url = 'https://www.booking.com'


def open_page(url):
    response = requests.get(url)
    page = html.fromstring(response.content)
    return page


def get_each_city_hotels_links(page):
    xpathsub_cities = './/div/ul/li'
    xpath_main_ul = '//*[@id="bodyconstraint-inner"]/div[3]/div[2]/ul/li[1]/ul'

    city_links = []
    paragraphs = page.xpath(xpath_main_ul)[0].getchildren()
    for paragraph in paragraphs:
        cities = paragraph.xpath(xpathsub_cities)
        for city in cities:
            city_a = city.find('.//a')
            link = city_a.get('href')
            name = city_a.get('title')
            city_links.append([name, base_url + link])

    return city_links


def get_each_hotels_from_city_links(city_links):
    xpath_main_li = '//*[@id="bodyconstraint-inner"]/div[3]/div[2]/ul/li[2]/ul/li'
    xpath_sub_list = './/div/ul/'
    hotel_names_links = []

    for link in city_links[:5]:
        page_city_hotels = open_page(link)
        paragraphs = page_city_hotels.xpath(xpath_main_li)[0].xpath(xpath_sub_list)

        for paragraph in paragraphs:
            for hotel in paragraph.xpath('.//a'):
                hotel_link = hotel.get('href')
                hotel_name = hotel.get('title')
                hotel_names_links.append((hotel_name, hotel_link))

    return hotel_names_links


def save(file_name, data):
    with open(f'../../../Data/{file_name}', 'wb') as f:
        pickle.dump(data, f)


def read(file_name):
    with open(f'../../../Data/{file_name}', 'rb') as f:
        return pickle.load(f)


def get_hotel_name_links(cities):
    xpath_main_li = '//*[@id="bodyconstraint-inner"]/div[3]/div[2]/ul/li[2]/ul/li'
    xpath_sub_list = './/div/ul'

    hotel_names_links = []
    print(f'total len {len(cities)}')

    for i, (city, link) in enumerate(cities):
        print(f'current city hotel {city} {i}')
        page_city_hotels = open_page(link)

        try:
            paragraphs = page_city_hotels.xpath(xpath_main_li)[0].xpath(xpath_sub_list)
        except IndexError as e:
            print(f'skipped {city} as no hotels found')
            continue

        for paragraph in paragraphs:
            for hotel in paragraph.xpath('.//a'):
                hotel_link = hotel.get('href')
                hotel_name = hotel.get('title')

                if not hotel_name:
                    print(f'possible error? {hotel_name}')
                hotel_names_links.append((hotel_name, base_url + hotel_link))

    return hotel_names_links


def main():
    # url = 'https://www.booking.com/destination/country/de.en-gb.html?aid=356980&label=gog235jc-1DCAoouAI46AdIB1gDaDuIAQGYAQe4ARfIAQzYAQPoAQH4AQKIAgGoAgO4Ap2mrPgFwAIB0gIkODMwMmNhOTAtNGU0Yy00MWY2LWFkZWMtNzZkZGY3ZjcyN2Y52AIE4AIB&lang=en-gb&soz=1&lang_click=top;cdl=de;lang_changed=1'
    # page = open_page(url)
    # cities = get_each_city_hotels_links(page=page)

    cities_file_name = 'each_city_hotels_links.pickle'
    # save(file_name=cities_file_name, data=cities)
    cities = read(file_name=cities_file_name)

    # hotel_names = get_hotel_name_links(cities)
    hotels_file_name = 'hotel_names_links.pickle'
    # save(file_name=hotels_file_name, data=hotel_names)
    hotel_names = read(file_name=hotels_file_name)
