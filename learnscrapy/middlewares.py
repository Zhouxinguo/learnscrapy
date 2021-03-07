# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
from scrapy import signals, Request
from scrapy.http import Response
import random


class LearnscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LearnscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Antispider7SpiderMiddleware(LearnscrapySpiderMiddleware):
    def __init__(self):
        super(Antispider7SpiderMiddleware, self).__init__()

    @property
    def proxy(self):
        return 'http://' + requests.get('http://192.168.19.128:5000/get').json()['proxy']

    def process_request(self, request: Request, spider):
        if len(spider.cookies) >= 20:
            request.headers.update({'authorization': f'jwt {random.choice(spider.cookies)}'})
            request.meta['proxy'] = self.proxy
        return None

    def process_response(self, request: Request, response: Response, spider):
        # 如果遇到了403，更换cookie或代理
        if response.status == 403:
            if request.meta['change_proxy'] == 0 and request.meta['change_cookie'] == 0:
                # 先换cookie
                print('cookie被ban，更换cookie')
                request.headers.update({'authorization': f'jwt {random.choice(spider.cookies)}'})
                request.meta['change_cookie'] = 1
            elif request.meta['change_proxy'] == 0 and request.meta['change_cookie'] == 1:
                print(f'重试：{response.url}')
                request.meta['proxy'] = self.proxy
                request.meta['change_proxy'] = 1
            elif request.meta['change_proxy'] == 1 and request.meta['change_cookie'] == 0:
                print('cookie被ban，更换cookie')
                request.meta['change_cookie'] = 1
                request.headers.update({'authorization': f'jwt {random.choice(spider.cookies)}'})
            else:
                request.headers.update({'authorization': f'jwt {random.choice(spider.cookies)}'})
                request.meta['proxy'] = self.proxy
                print('两个都换')
            return request
        else:
            return response
