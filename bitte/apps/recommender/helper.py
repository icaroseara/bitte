__author__ = 'icaro'
import random
from bitte.apps.recommender.models import *
from xml.etree import ElementTree
import json
import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class Helper:
    def logger(self, title, msg):
        f = open('log.log','a')
        f.write(title+':'+str(msg)+'\n')
        f.close()

    def generate_ratings(self):
        for i in range(0,10000):
            value = random.randint(1,5)
            user = User.objects.order_by('?')[0]
            item = Item.objects.order_by('?')[0]
            context = Context.objects.order_by('?')[0]

            rating = Rating.objects.create(context = context,item = item,user = user)
            rating.value = value
            rating.save()

