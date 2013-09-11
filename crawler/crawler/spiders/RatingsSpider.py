# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import RatingItem
from scrapy.http import Request

import json
import re

class RatingssSpider(BaseSpider):

    name = "ratings"
    allowed_domains = ["tripadvisor.com.br"]
    json_data = open('/Users/icaro/Documents/UFBA/PF2/coding/bitte/crawler/crawler/urls.json')
    data = json.load(json_data)
    data = [url[u'url'] for url in data]
    json_data.close()
    start_urls = data

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        base = hxs.select('//h3[@class="reviews_header"]/text()').extract()
        items=[]
        if len(base)>0:
            total = 10
            final = base[0]
            m = re.search('(\d+)', final)
            total = m.group(0)
            current_url = response.url
            for i in range(0, int(total), 10):
                item = RatingItem()
                if i == 0:
                    url = current_url

                else:
                    url = current_url.replace('-Reviews-','-Reviews-or'+str(i)+'-')
                item["total"] = total
                item["url"] = url
                items.append(item)
        return items

