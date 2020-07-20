import logging

import scrapy
from lxml import html
from ..items import BookingScrapeItem
from .scrape_city_hotel_links import read

hotel_names_links = read('hotel_names_links.pickle')
links = [link for name, link in hotel_names_links]


# TODO sql, add hotel links
class MySpiderSplash(scrapy.Spider):
    name = "BookingSpider"
    start_urls = links[:1000]

    def __init__(self, *args, **kwargs):
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        xpath_hotel_name_text = '//*[@id="hp_hotel_name"]/text()'
        xpath_location = '//*[@id="showMap2"]/span/text()'
        xpath_imgs = '//a[@data-id]/@href'
        xpath_score_category = '//*[@id="js--hp-gallery-scorecard"]/a/div/div[2]/div[1]/text()'
        xpath_score = '//*[@id="js--hp-gallery-scorecard"]/a/div/div[1]/text()'
        # xpath_perks = '//*[@id="hotel_main_content"]/div[3]/div[1]/div'
        # xpath_sub_perks = './/div[2]/text()'
        xpath_description = '//*[@id="summary"]'
        xpath_host_info = '//*[@id="host-info"]'
        xpath_surroundings_type = '//h2[@class="hp-poi__section-heading loc_block_header_fix"]'
        xpath_surroundings_info = '//div[contains(@class, "hp-poi-content-container hp-poi-content-container--column clearfix  ")]'
        xpath_facilities = '//*[@class="facilitiesChecklist"]'
        xpath_house_rules = '//div[contains(@class, "descriptionsContainer")]'
        xpath_fine_print = '//*[@id="hp_important_info_box"]'
        xpath_faq = '//*[@id="c-lp-faq"]/div/div[2]'

        page = html.fromstring(response.body)
        try:
            hotel_name = response.xpath(xpath_hotel_name_text).getall()[1]
            location = response.xpath(xpath_location).get()
            imgs = response.xpath(xpath_imgs).getall()
        except:
            hotel_name = ''
            location = ''
            imgs = ['']

        score_category = self.get_element(page, xpath_score_category)
        score = self.get_element(page, xpath_score)

        # perks = self.get_perks(page, xpath_perks, xpath_sub_perks)

        description = self.get_element_textcontent(page, xpath_description)
        host_info = self.get_element_textcontent(page, xpath_host_info)
        surroundings_type = self.get_element_textcontent(page, xpath_surroundings_type)
        surroundings_info = self.get_element_textcontent(page, xpath_surroundings_info)

        # TODO sometimes skips the first 2 divs
        facilities = self.get_element_textcontent(page, xpath_facilities)

        house_rules = self.get_element_textcontent(page, xpath_house_rules)
        fine_print = self.get_element_textcontent(page, xpath_fine_print)

        # TODO reviews are hard to ackquire, they won't show until
        #  click and after click only 10 are shown at a time

        faq = self.get_element_textcontent(page, xpath_faq)

        print(f'Done hotel {hotel_name}')

        yield BookingScrapeItem(hotel_name=hotel_name,
                                location=location,
                                imgs=imgs,
                                score_category=score_category,
                                score=score,
                                # perks=perks,
                                description=description,
                                host_info=host_info,
                                surroundings_type=surroundings_type,
                                surroundings_info=surroundings_info,
                                facilities=facilities,
                                house_rules=house_rules,
                                fine_print=fine_print,
                                faq=faq)

    #
    # # TODO change perks
    # @staticmethod
    # def get_perks(page, xpath_perks, xpath_sub_perks):
    #     perks = ''
    #     for perk_element in page.xpath(xpath_perks):
    #         perk = perk_element.xpath(xpath_sub_perks)[0]
    #         perks += perk
    #     return perks

    @staticmethod
    def get_element_textcontent(page, xpath):
        try:
            return page.xpath(xpath)[0].text_content()
        except:
            return ''

    @staticmethod
    def get_element(page, xpath):
        try:
            return page.xpath(xpath)[0]
        except:
            return ''
