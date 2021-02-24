import scrapy
from scrapy import Request
from learnscrapy.items import SPA1Item

class SSR1(scrapy.Spider):
    name = 'spa1'

    def start_requests(self):
        urls = [
            f'https://spa1.scrape.center/api/movie/?limit=10&offset={a}' for a in range(0,100,10)
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.json()
        print('response:',response)
        for a in result['results']:
            item = SPA1Item()
            item['title'] = a['name'] + a['alias']
            item['fraction'] = a['score']
            item['country'] = '、'.join(a['regions'])
            item['time'] = a['minute']
            item['date'] = a['published_at']
            url = response.urljoin(f'/api/movie/{a["id"]}')
            yield Request(url=url,callback=self.parse_person,meta={'item':item})
        pass

    def parse_person(self,response):
        result = response.json()
        item = response.meta['item']
        item['director'] = result['directors'][0]['name']
        yield item