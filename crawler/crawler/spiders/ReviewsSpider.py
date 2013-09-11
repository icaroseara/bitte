# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import ReviewItem
from scrapy.http import Request

import json

class ReviewsSpider(BaseSpider):

    name = "reviews"
    allowed_domains = ["tripadvisor.com.br"]
    json_data = open('/Users/icaro/Documents/UFBA/PF2/coding/bitte/crawler/crawler/reviews.json')
    data = json.load(json_data)
    data = [url[u'url'] for url in data]
    json_data.close()
    start_urls = data

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        atraction = hxs.select('//h1/text()').extract()
        rates = hxs.select("//div[@class='rating reviewItemInline']/span/img[@class='sprite-ratings']/@content").extract()
        dates = hxs.select("//span[@class='ratingDate']/text()").extract()
        users = hxs.select('//div[@class="username mo"]/span/text()').extract()
        items = []
        total = len(rates)
        for i in range(0,total):
            item = ReviewItem()
            item['rate']= rates[i]
            date = dates[i]
            date = date.encode('utf-8')
            item['date']= str(date).replace("Avaliou em ","")
            #atraction = atraction[0].encode('utf-8')
            item['atraction']= atraction[0]
            item['user']= users[i]
            items.append(item)
        return items




