import scrapy
from scrapy import Request
from learnscrapy.items import SPA1Item
import time,random,base64
from hashlib import sha1

class SPA2Spider(scrapy.Spider):
    name = 'spa2'

    @staticmethod
    def sign(url):
        t = str(int(time.time()) - random.randint(1,20))
        s = ','.join([url,t])
        return base64.b64encode(','.join([sha1(s.encode()).hexdigest(),t]).encode()).decode()

    def start_requests(self):
        urls = [
            f'http://spa2.scrape.center/api/movie/?limit=10&offset={a}&token={self.sign("/api/movie")}' for a in range(0,100,10)
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
            s = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'
            detail = base64.b64encode((s + str(a["id"])).encode()).decode()

            yield Request(url=response.urljoin(f'/api/movie/{detail}/?token={self.sign("/api/movie/" + detail)}'),callback=self.parse_person,meta={'item':item})
        pass

    def parse_person(self,response):
        result = response.json()
        item = response.meta['item']
        item['director'] = result['directors'][0]['name']
        yield item