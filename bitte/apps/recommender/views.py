from django.http import HttpResponse
from bitte.apps.recommender.models import *
import urllib2
import urllib
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urlparse import urlparse
from django.core.files import File
import json
from django.contrib.auth.models import User
from bitte.apps.accounts.models import UserProfile
import random
import calendar
from datetime import datetime, date
from django.contrib.auth.hashers import make_password
from django.utils.timezone import utc

from bitte.apps.recommender.experiment import Experimenter

def crawl(request):
    seeds = []

    seeds.append("http://www.touristeye.com/places?parent_id=2286&start=1&num=100&category_id=1&s=")
    root = "http://www.touristeye.com"

    urls = []

    for seed in seeds:
        request = urllib2.Request(seed)
        response = urllib2.urlopen(request)
        document = response.read()

        soup = BeautifulSoup(unicode(document, 'utf-8', 'ignore'))

        links = soup.findAll('a', {'class': 'item-desc'})

        for link in links:
            try:
                urls.append(root + link['href'])
            except KeyError:
                pass

    for url in urls:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        document = response.read()

        soup = BeautifulSoup(unicode(document, 'utf-8', 'ignore'))

        content = soup.find("div", {"id": "place"})

        name = content['data-title']
        description = ""
        location = content['data-street']

        lat_position = content['data-lat']
        long_position = content['data-lng']

        category = Category.objects.get(id=1)
        city = City.objects.get(id=1)

        image = soup.findAll(attrs={"itemprop": "photo"})
        image_url = ""
        try:
            image_url = image[0]['data-url']
            item = Item(name=name, location=location, lat_position=lat_position, long_position=long_position,
                        category=category, city=city)
            item.save()

            photo = ItemPhoto(item=item)

            name = urlparse(image_url).path.split('/')[-1]

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(image_url).read())
            img_temp.flush()

            photo.photo.save(name, File(img_temp))
            photo.save()
        except:
            pass

    return HttpResponse("Crawled")


def generate_items(self):
    json_file = open("/Users/icaro/Documents/UFBA/PF2/coding/bitte/crawler/crawler/atractions.json")
    data = json.load(json_file)

    category = Category.objects.get(id=1)
    city = City.objects.get(id=1)
    for i in data['items']['item']:
        name = i['name']
        lat_position = i['lat_position']
        long_position = i['long_position']
        location = ""
        if 'location' in i.keys():
            location = i['location']['value']
        photo_url = ""
        if 'photo' in i.keys():
            photo_url = i['photo']['value']

        try:
            item = Item.objects.get(name=name)
        except Item.DoesNotExist:
            item = Item.objects.create(name=name, location=location, long_position=long_position,
                                       lat_position=lat_position, category=category, city=city)
            item.save()

            if photo_url != "":
                photo = ItemPhoto(item=item)
                name = urlparse(str(photo_url)).path.split('/')[-1]
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urllib2.urlopen(photo_url).read())
                img_temp.flush()
                photo.photo.save(name, File(img_temp))
                photo.save()
        json_file.close()
    return HttpResponse("Crawled")

def get_table_temperature(month):
    table = {}
    table["Jan"] = [25,30]
    table["Feb"] = [26,31]
    table["Mar"] = [25,30]
    table["Apr"] = [25,30]
    table["May"] = [24,29]
    table["Jun"] = [23,28]
    table["Jul"] = [22,27]
    table["Aug"] = [23,27]
    table["Sep"] = [23,27]
    table["Oct"] = [24,29]
    table["Nov"] = [24,29]
    table["Dec"] = [25,30]
    min = table[month][0]
    max = table[month][0]
    grad = random.randint(min,max)
    return grad

def convert_grad_to_weather(grad):
        grad = int(grad)
        if grad <= 10:
            return 'VC'
        if ((grad > 10) and (grad <= 20)):
            return 'C'
        elif ((grad > 20) and (grad <= 25)):
            return 'A'
        elif((grad > 25) and (grad <= 30)):
            return 'H'
        else:
            return 'VH'

def evaluate(self):
    experiment = Experimenter()
    retorno = experiment.make_experiment()
    return HttpResponse(retorno)

def generate_user_ratings(self):
    json_file = open("/Users/icaro/Documents/UFBA/PF2/coding/bitte/crawler/crawler/rates.json")
    data = json.load(json_file)
    for i in data['items']['item']:
        username = i[u'user']
        try:
            username = unicode(username, 'latin-1').lower()
        except TypeError:
            username = username.lower()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            email = username+"@bitte.com.br"
            password = make_password(12345)
            user = User.objects.create(username=username,email=email,password=password)
            gender =  random.choice(['M','F'])
            year = random.randint(1933,1994)
            month = random.randint(1,12)
            day = random.randint(1,20)

            birthday = datetime(year,month,day)
            UserProfile.objects.create(user=user,
                                           gender=gender,
                                           birthday=birthday)
        date_review =""
        if 'date' in i.keys():
            date_review = i['date']
        if date_review != "":
            companion =  random.choice(['F','G','M','A'])
            motivation =  random.choice(['E','F','B'])
            date_review =  datetime.strptime(date_review, '%b %d %Y')

            date_tz = datetime.utcnow().replace(tzinfo=utc,month =date_review.month,
                                                         day = date_review.day,
                                                         year= date_review.year)
            date_review = date_tz

            month_name = calendar.month_name[date_review.month]
            grad = get_table_temperature(month_name[:3])
            weather = convert_grad_to_weather(grad)

            context = Context.objects.create(companion= companion,motivation=motivation,
                        date = date_review,weather=weather)

            distance_max = 20
            CurrentContext.objects.filter(user=user).update(current=False)
            CurrentContext.objects.create(user=user,context=context,distance_max = distance_max)
            item_name = i[u'atraction']
            #item_name = unicode(item_name, 'latin-1')
            """
            item = Item.objects.get(name=item_name)
            if item.count():
                value = i['rate']
                rating = Rating.objects.create(context = context,item = item,user = user,value=value)
                rating.save()
            """
        try:
            item = Item.objects.get(name=item_name)
            value = float(i['rate'])
            rating = Rating.objects.create(context = context,item = item,user = user,value=value)
            rating.save()
        except Item.DoesNotExist:
            pass
    json_file.close()
    return HttpResponse("Crawled")
