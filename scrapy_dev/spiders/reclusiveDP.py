#coding:utf-8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders.crawl import CrawlSpider, Rule

from scrapy_dev.items import ShopItem
from scrapy_dev.bufferQueue import enQueShop,deQueShop
from scrapy.linkextractors import LinkExtractor

class reclusiveSpider(CrawlSpider):
    name = "reclusive" 
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dianping.com/beijing"
    ]
    
    rules = (
             Rule(LinkExtractor(allow=r'/search/category/2/0',tags='a'),
                  callback = 'parse_region'),
             )
    
    def parse_region(self, response):
            
        sel = Selector(response)
        print response
        
        shops = sel.xpath('//div[@id=\"shop-all-list\"]/ul/li')
        shopList =[] 
        print "======================================================="
        print shops
        print "======================================================="
        
        with open('shop.txt','a') as f:
            f.truncate()
        
        for site in shops:        
            shop = ShopItem()
            shop['name'] = site.xpath('.//div[@class=\"tit\"]/a/h4/text()').extract() 
            shop['region_tag'] = site.xpath('.//div[@class=\"tag-addr\"]/a[2]/span[@class=\"tag\"]/text()').extract() 
            shop['address'] = site.xpath('.//div[@class=\"tag-addr\"]/span[@class=\"addr\"]/text()').extract() 
            shop['href'] = site.xpath('.//div[@class=\"tit\"]/a[./h4!=\"\"]/@href').extract() 
            
            shopList.append(shop)  
            enQueShop(shop)
            print "----------------------------",shop['name']
            with open('shop.txt','a') as f:
                f.write(str(shop))
#         with open('shop.txt','r') as f:
#             print f.read()
        print shopList
        return shopList

    