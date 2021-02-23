import scrapy
from scrapy import Request
from learnscrapy.items import SSR1ScrapyItem

class SSR1(scrapy.Spider):
    name = 'ssr1'

    def start_requests(self):
        urls = [
            f'https://ssr1.scrape.center/page/{a}' for a in range(1,11)
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response, **kwargs):
        result = response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for a in result:
            item = SSR1ScrapyItem()
            item['title'] = a.xpath('.//h2[@class="m-b-sm"]/text()').extract_first()
            item['fraction'] = a.xpath('.//p[@class="score m-t-md m-b-n-sm"]/text()').extract_first()
            item['country'] = a.xpath('.//div[@class="m-v-sm info"][1]/span[1]/text()').extract_first()
            item['time'] = a.xpath('.//div[@class="m-v-sm info"][1]/span[3]/text()').extract_first()
            item['date'] = a.xpath('.//div[@class="m-v-sm info"][2]/span/text()').extract_first()
            url = a.xpath('.//a[@class="name"]/@href').extract_first()
            yield Request(url=response.urljoin(url),callback=self.parse_person,meta={'item':item})
        pass

    def parse_person(self,response):
        item = response.meta['item']
        item['director'] = response.xpath('.//div[@class="directors el-row"]//p/text()').extract_first()
        yield item