# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import urllib

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']//dt") # 大分类列表
        for dt in dt_list:
            item = {}
            item['big_classify'] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em") # 小分类列表
            for em in em_list:
                item['s_href'] = em.xpath("./a/@href").extract_first()
                item['small_classify'] = em.xpath("./a/text()").extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = 'https:' + item['s_href']
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item':deepcopy(item)}
                    )

    def parse_book_list(self,response): # 解析列表页

        item = response.meta['item']
        print(item)
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            if li.xpath(".//div[@class='p-img']//img/@src") is not None:
                item['img_href'] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            else:
                item['img_href'] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item['book_title'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item["book_publish_data"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-date']/text()").extract_first().strip()
            item["book_sku"] = li.xpath("./div/@data-sku").extract_first()
            yield scrapy.Request(
                'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_sku']),
                callback=self.parse_book_price,
                meta={'item':deepcopy(item)}
            )
        # 列表页翻页
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item':item}
            )


    def parse_book_price(self,response):
        item = response.meta['item']
        item['book_price'] = json.loads(response.body.decode())[0]['op']
        yield item

