import scrapy

class SSR1(scrapy.Spider):
    name = 'ssr1'

    def start_requests(self):
        urls = [
            f'https://ssr1.scrape.center/page/{a}' for a in range(1,11)
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response, **kwargs):
        pass