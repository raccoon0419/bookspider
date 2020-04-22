# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/b/?&node=116169071&tag=baiduiclickcn-23&ref=xg_DEP_18119_SY_51']
    redis_key = 'amazon'

    rules = (
        # 匹配大分类URL地址和小分类url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='leftNav']//ul[4]//div/li"),), follow=True),
        # 匹配图书的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/.."),),callback='parse_book_detail'),
        # 匹配翻页地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']"),),follow=True),
    )


    def parse_book_detail(self,response):
        item = {}
        item['book_title'] = response.xpath("//sapn[@id='productTitle']/text()").extract_first()
        item['book_publish_date'] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first()
        item['book_author'] = response.xpath("//div[@id=byline]/span/a/text()").extract()
        item['book_price'] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()").extract_first()
        item['book_press'] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
        print(item)
