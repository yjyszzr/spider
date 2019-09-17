# -*- coding: utf-8 -*-
import scrapy


class Asian5Spider(scrapy.Spider):
    name = 'asian_5'
    allowed_domains = ['500.com']
    start_urls = ['http://live.500.com/']

    def parse(self, response):
        pass
