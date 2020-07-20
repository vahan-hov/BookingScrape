# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    hotel_name = scrapy.Field()
    location = scrapy.Field()
    imgs = scrapy.Field()

    score_category = scrapy.Field()
    score = scrapy.Field()
    # perks = scrapy.Field()

    description = scrapy.Field()
    host_info = scrapy.Field()
    surroundings_type = scrapy.Field()
    surroundings_info = scrapy.Field()

    facilities = scrapy.Field()
    house_rules = scrapy.Field()
    fine_print = scrapy.Field()
    faq = scrapy.Field()
