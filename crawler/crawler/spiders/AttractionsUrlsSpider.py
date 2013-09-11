from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import UrlItem

class AttractionsUrlsSpider(BaseSpider):
    name = "attractionsurls"
    allowed_domains = ["tripadvisor.com.br"]
    start_urls = [
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-Salvador_State_of_Bahia.html#TtD",
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-oa30-Salvador_State_of_Bahia.html#TtD",
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-oa60-Salvador_State_of_Bahia.html#TtD",
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-oa70-Salvador_State_of_Bahia.html#TtD",
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-oa120-Salvador_State_of_Bahia.html#TtD",
        "http://www.tripadvisor.com.br/Attractions-g303272-Activities-oa150-Salvador_State_of_Bahia.html#TtD",
    ]
    def parse(self, response):
        items = []
        base_url = "http://www.tripadvisor.com.br"
        hxs = HtmlXPathSelector(response)
        urls =  hxs.select('//a[@class="property_title"]//@href').extract()
        #names = hxs.select('//a[@class="property_title"]/text()').extract()
        #photos = hxs.select('//a[@class="photo_link "]/img/@src').extract()


        for url in urls:
            item = UrlItem()
            item['url'] = base_url + url
            #item['name'] = names[i]
            #item['photo'] = photos[i].replace("photo-l","photo-s")
            items.append(item)

        return items
