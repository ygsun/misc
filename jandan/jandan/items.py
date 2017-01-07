# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose
from scrapy.utils.misc import arg_to_iter


class ChoiceOnePic(object):
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return arg_to_iter(value)


class AddScheme(object):
    def __call__(self, values, loader_context):
        response = loader_context.get('response')
        return [response.urljoin(url) for url in values]


class OoxxItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class OoxxItemLoader(ItemLoader):
    author_out = TakeFirst()
    image_urls_out = Compose(ChoiceOnePic(), AddScheme())
