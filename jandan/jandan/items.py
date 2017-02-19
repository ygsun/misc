# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def add_schema(url, loader_context):
    response = loader_context['response']
    if response:
        return response.urljoin(url)
    else:
        return 'http:' + url


class OoxxItem(scrapy.Item):
    author_name = scrapy.Field()
    pic_url = scrapy.Field()
    pub_date = scrapy.Field()
    result = scrapy.Field()


class OoxxItemLoader(ItemLoader):
    author_name_in = MapCompose(str.strip)
    author_name_out = TakeFirst()

    pic_url_in = MapCompose(add_schema)
    # pic_url_out = TakeFirst()

    pub_date_in = MapCompose(str.strip)
    pub_date_out = TakeFirst()
