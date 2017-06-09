#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request


class PdfSearch(scrapy.Spider):
    name = 'pdf_search'

    custom_settings = {
        'HTTPERROR_ALLOW_ALL': True,
        'DEPTH_LIMIT': 50,
        'MAX_REQUESTS': 100000,
        'RETRY_HTTP_CODES': [],
    }

    def __init__(self, *args, **kwargs):
        super(PdfSearch, self).__init__(*args, **kwargs)
        self.start_urls = str(kwargs.get('input_url'))
        self.allowed_domains = [str(kwargs.get('allowed_domains'))]

    def start_requests(self):
        logging.getLogger('scrapy').propagate = False
        url = getattr(self, 'url', self.start_urls)
        yield scrapy.Request(url, dont_filter=True, callback=self.parse, errback=self.errback)

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.parse_pdf)

    def parse_pdf(self, response):
        for href in response.css('a[href$=".pdf"]::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.save_pdf)

    def save_pdf(self, response):
        f = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', f)
        with open(f, 'wb') as f:
            f.write(response.body)

    def errback(self, err):
        """Handles an error"""
        return {
            'url': err.request.url,
            'status': 'error_downloading_http_response',
            'message': str(err.value),
        }


def scrap(url, domain):
    try:
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/53.0'})
        data = {'input_url': url, 'allowed_domains': domain}
        process.crawl(PdfSearch(**data))
        process.start()
    except:
        pass
