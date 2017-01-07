# -*- coding: utf-8 -*-
import scrapy

from ..items import OoxxItem, OoxxItemLoader


class OoxxSpider(scrapy.Spider):
    name = "ooxx"
    allowed_domains = ["jandan.net"]
    start_urls = ['http://jandan.net/ooxx/page-1']

    def parse(self, response):
        # parse picture item
        for li_selector in response.css('ol.commentlist > li'):
            item_loader = OoxxItemLoader(OoxxItem(), selector=li_selector, response=response)

            # 查看作者名称
            item_loader.add_css('author', 'div.author > strong::text')

            # 查看原图URL
            item_loader.add_css('image_urls', 'div.text > p > a.view_img_link::attr(href)')

            # 缩略图URL
            item_loader.add_css('image_urls', 'div.text > p > img::attr(src)')

            yield item_loader.load_item()

            # parse next page
            next_page = response.css('div.cp-pagenavi > a.next-comment-page::attr(href)').extract_first()
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
