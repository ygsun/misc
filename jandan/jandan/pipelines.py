# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
import datetime
import random

from scrapy.exceptions import DropItem

from .spiders.models import *


class URLEmptyPipeline(object):
    def process_item(self, item, spider):
        if 'pic_url' not in item:
            raise DropItem('Missing url in {}'.format(item))
        else:
            return item


class URLFilterPipeline(object):
    @staticmethod
    def filter_by_url(url, pattern):
        if url:
            return re.search(pattern, url, flags=re.I)
        else:
            return False

    def process_item(self, item, spider):
        includes = spider.settings.get('URLFILTER_INCLUDE')
        for url in item['pic_url']:
            for pattern in includes:
                if self.filter_by_url(url, pattern):
                    return item

        raise DropItem('Failed validate the pattern of {}'.format(item['pic_url']))


class ConvertDateTimePipeline(object):
    @staticmethod
    def _convert_delta(offset, units):
        offset = random.choice((1, -1)) * int(offset)
        units = units.lower()
        if units == 'years' or units == 'year':
            obj = datetime.timedelta(weeks=offset * 12)
        elif units == 'weeks' or units == 'week':
            obj = datetime.timedelta(weeks=offset)
        elif units == 'days' or units == 'day':
            obj = datetime.timedelta(days=offset)
        elif units == 'hours' or units == 'hour':
            obj = datetime.timedelta(hours=offset)
        elif units == 'mins' or units == 'min':
            obj = datetime.timedelta(minutes=offset)
        elif units == 'seconds' or units == 'second':
            obj = datetime.timedelta(seconds=offset)
        else:
            obj = None

        return obj

    def extract_info(self, raw_datetime_desc):
        m = re.match(r'@(\d+)\s+(\w+)\s+ago', raw_datetime_desc)
        if m:
            offset, units = m.groups()
            t_delta = self._convert_delta(offset, units)
            if t_delta:
                new_datetime = datetime.datetime.now() + t_delta
                return new_datetime.replace(microsecond=0)

    def process_item(self, item, spider):
        pub_date = item['pub_date']
        date = self.extract_info(pub_date)
        if date is not None:
            item['pub_date'] = date
            return item
        else:
            raise DropItem('Invalid pub_date {}'.format(item['pub_date']))


class StoreDBPipeline(object):
    def process_item(self, item, spider):
        if 'result' not in item:
            raise DropItem('Downloading url {} failed.'.format(item['url']))
        else:
            for result in item['result']:
                catelog, _ = Catelog.get_or_create(name=spider.name)
                author, _ = Author.get_or_create(name=item['author_name'])
                Picture.get_or_create(author=author,
                                      catelog=catelog,
                                      url=result['url'],
                                      defaults=dict(
                                          pub_date=item['pub_date'],
                                          path=result['path'],
                                          # path=os.path.abspath(os.path.join(spider.settings.get('FILES_STORE'), result['path']))),
                                      ))
        return item

    def open_spider(self, spider):
        database_proxy.connect()

    def close_spider(self, spider):
        database_proxy.close()
