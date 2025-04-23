# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PassesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url_pass = scrapy.Field()
    route_name = scrapy.Field()
    score = scrapy.Field()
    number_of_reviews = scrapy.Field()
    GPS = scrapy.Field()
    url_route = scrapy.Field()
    url_gif = scrapy.Field()
    elevation = scrapy.Field()
    elevation_gain = scrapy.Field()
    gradient = scrapy.Field()
    deadend = scrapy.Field()
    length= scrapy.Field()
    pass
