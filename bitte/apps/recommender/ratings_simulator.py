# -*- coding:utf-8 -*-

__author__ = 'icaro'

from bitte.apps.recommender.models import *

class RatingSimulator:

    def simule(self):

        for it in range(0,100):
            value = rating(0,5)
            rating = Rating()
            rating.context = 1
            rating.item = 1
            rating.user = 1
            rating.value = value
            rating.save()
