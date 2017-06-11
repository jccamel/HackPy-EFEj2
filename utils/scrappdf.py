#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request


class PdfSearch(scrapy.Spider):

    name = 'FileScrap'

    custom_settings = {
        'HTTPERROR_ALLOW_ALL': True,
        'DEPTH_LIMIT': 50,
        'MAX_REQUESTS': 100000,
        'RETRY_HTTP_CODES': [],
    }

    def start_requests(self):
        logging.getLogger('scrapy').propagate = False
        requests = []
        urlfile = '/home/camelo/PycharmProjects/HackPy-EFEj2/projecte/' + nameproject + '/url.txt'
        for url in open(urlfile):
            requests.append(scrapy.Request(url=url, callback=self.parse))
        return requests

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.parse_file)

    def parse_file(self, response):
        for href in response.css('a[href$=".pdf"]::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.save)
        for href in response.css('a[href$=".jpg"]::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.save)
        for href in response.css('a[href$=".png"]::attr(href)').extract():
            yield Request(url=response.urljoin(href), callback=self.save)
        for href in response.css('img').xpath('@src').extract():
            yield Request(url=response.urljoin(href), callback=self.save)

    def save(self, response):
        import os
        f = ''
        path_download_foto = '/home/camelo/PycharmProjects/HackPy-EFEj2/photo_downloaded/'
        path_download_pdf = '/home/camelo/PycharmProjects/HackPy-EFEj2/pdf_downloaded/'
        name_file = response.url.split('/')[-1]
        if name_file.endswith('.jpg') or name_file.endswith('.png'):
            f = path_download_foto + name_file
        elif name_file.endswith('.pdf'):
            f = path_download_pdf + name_file
        if not os.path.isfile(f) or f == '':
            self.logger.info('Saving File %s', f)
            with open(f, 'wb') as f:
                f.write(response.body)
        else:
            self.logger.info('File %s NOT SAVED!!', f)

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
