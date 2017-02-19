# -*- coding: utf-8 -*-
import logging
import scrapy

from ..items import OoxxItem, OoxxItemLoader
from scrapy.shell import inspect_response
from scrapy.settings import default_settings


class OoxxSpider(scrapy.Spider):
    name = 'wuliao'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/pic']

    def parse(self, response):
        # fetch current page's all li elements
        for item_selector in response.css('ol.commentlist > li[id^="comment-"]'):
            # fill the item data
            item = OoxxItemLoader(item=OoxxItem(),
                                  selector=item_selector,
                                  response=response)
            # author name field
            item.add_css('author_name', 'div.author > strong::text')

            # img url
            item.add_css('pic_url', 'div.text > p > a.view_img_link::attr(href)')

            # public date text description
            item.add_css('pub_date', 'div.author > small > a::text')

            yield item.load_item()

        # follow next page
        # CLOSESPIDER_PAGECOUNT=2
        next_page_selector = response.css('div.cp-pagenavi > a.previous-comment-page::attr(href)')
        if next_page_selector:
            # self.log(response.urljoin(next_page_selector.extract_first()), logging.INFO)
            yield scrapy.Request(response.urljoin(next_page_selector.extract_first()))
