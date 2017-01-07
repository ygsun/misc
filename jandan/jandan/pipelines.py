# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from scrapy import Request

import hashlib


class JandanPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s/%s.jpg' % (request.meta['author'], image_guid)

    def get_media_requests(self, item, info):
        return [Request(x, meta={'author': item['author']}) for x in item.get(self.images_urls_field, [])]
