# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import AttractionItem
from scrapy.http import Request

import json

class AttractionsUrlsSpider(BaseSpider):

    name = "attractions"
    allowed_domains = ["tripadvisor.com.br"]
    json_data = open('/Users/icaro/Documents/UFBA/PF2/coding/bitte/crawler/crawler/urls.json')
    data = json.load(json_data)
    data = [url[u'url'] for url in data]
    json_data.close()
    start_urls = data

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//h1/text()').extract()
        photo = hxs.select('//div[@class="photo "]/a/@href').extract()
        location =  hxs.select('//span[@class="street-address"]/text()').extract()
        complement = hxs.select('//span[@class="extended-address"]/text()').extract()
        latitude = hxs.select('//div[@class="js_floatContent"]/script').re(r'lat: \d*(.*)')
        longitude = hxs.select('//div[@class="js_floatContent"]/script').re(r'lng: \d*(.*)')
        item = AttractionItem()
        item['name'] = title[2]
        item['photo'] = photo
        item['location'] = location + complement
        if len(latitude)>0 and  len(longitude)>0:
            latitude = latitude[0].replace(',','')
            longitude = longitude[0].replace(',','')
            item['lat_position'] = latitude
            item['long_position'] = longitude
            return item


