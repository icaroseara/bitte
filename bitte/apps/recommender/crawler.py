# -*- coding: utf-8-sig -*-
import urllib2
import urllib
from bs4 import BeautifulSoup

class Crawler:
    def crawl_tripadvisor(self):
        pass
    def crawl_touristeye(self):
        seeds = []
        seeds.append("http://www.touristeye.com/places?parent_id=2286&start=1&num=100&category_id=1&s=")
        root = "http://www.touristeye.com"
        
        urls = []
            
        # percorre a lista de urls
        for seed in seeds:
            # solicita a url e obtém o documento relacionado
            request = urllib2.Request(seed)
            response = urllib2.urlopen(request)
            document = response.read()
        
            # parse do documento
            if 'charset=utf-8' in document:
                soup = BeautifulSoup(unicode(document, 'utf-8', 'ignore'))
            else:
                soup = BeautifulSoup(unicode(document, 'ISO-8859-1', 'ignore'))
        
            # retorna uma lista com todos os links do documento
            links = soup.findAll('a', {'class': 'item-desc'})
        
            # percorre a lista de links no documento
            for link in links:
                try:
                    #print root + link['href']
                    urls.append(root + link['href'])
                except KeyError:
                    pass
        
        for url in urls:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            document = response.read()
        
            # parse do documento
            if 'charset=utf-8' in document:
                soup = BeautifulSoup(unicode(document, 'utf-8', 'ignore'))
            else:
                soup = BeautifulSoup(unicode(document, 'ISO-8859-1', 'ignore'))
        
            content = soup.find("div", {"id": "place"})
            #print url
            #print content
            #break
            
            # Item content
            name = content['data-title']
            description = ""
            location = content['data-street']
        
            lat_position = content['data-lat']
            long_position = content['data-lng']
        
            category = 1
            city = 1
            id_item = 1
            
            image = soup.findAll(attrs={"itemprop" : "photo"}) 
            image_url = ""
            try:
                image_url = image[0]['data-url']
            except: 
                pass            
                      
            print name +" | "+ location +" | "+ lat_position +" | "+ long_position +" | "+ image_url
            #break
    def crawl_mundi(self):
        pass
    def crawl_kekanto(self):
        pass
    def to_crawl(self, select):
        if select == "touristeye":
            self.crawl_touristeye()
        elif select == "mundi":
            self.crawl_mundi()
        elif select == "kekanto":
            self.crawl_kekanto()
        else:
            pass
    def do_post(self):
        from httplib2 import Http
        from urllib import urlencode
        http = Http()
        headers = {'Host': ' localhost:8000',
        'Origin' : 'http://localhost:8000',
        'Referer' : 'http://localhost:8000/admin/recommender/item/add/',
        'Cookie' : 'sessionid=11tpiz4n4u1p17fixrfbqlpbudrqttbl;csrftoken=thMqH8FNG16ml84tUqHFwUu66z4UzcE1'}
        body = dict(name="TT", description="A test comment",location ="loca",lat_position=32.777000,long_position=92.999000,category=1,city=1)
        #response, content = h.request("http://localhost:8000/admin/recommender/item/add/", "POST",headers=headers, urlencode(data))
        #print resp, content
        url = "http://localhost:8000/admin/recommender/item/add/"
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        print response, content
        
