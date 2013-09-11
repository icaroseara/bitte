from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
    name = models.CharField(blank =False,
                            null = False,
                            max_length = 50,
                            verbose_name = u'Category name')
    def __unicode__(self):
        return self.name

class State(models.Model):
    name = models.CharField(blank =False,
                            null = False,
                            max_length = 50,
                            verbose_name = u'State name')
    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(blank =False,
                            null = False,
                            max_length = 50,
                            verbose_name = u'City name')
    country = models.CharField(default = "BR", max_length = 2)

    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name + "-" + self.state.name


class Item(models.Model):
    name = models.CharField(blank = False,
                          null = False,
                          max_length = 80,
                          verbose_name = u'Item name')
    description = models.TextField(blank = True,
                          null = True,
                          verbose_name = u'Description')
    location = models.TextField(blank = True,
                          null = True,
                          verbose_name = u'Location')

    lat_position   = models.DecimalField (max_digits=8, decimal_places=6)
    long_position   = models.DecimalField (max_digits=8, decimal_places=6)


    category = models.ForeignKey(Category)
    city = models.ForeignKey(City)

   # def __unicode__(self):
    #    return self.name


class ItemPhoto(models.Model):
    photo = models.ImageField(upload_to='product_photo',blank=True)
    description = models.TextField(blank = True,
                          null = True,
                          max_length = 150,
                          verbose_name = u'Description')

    item = models.ForeignKey('Item', related_name='photos')

    def __unicode__(self):
        return self.photo.name

class Context(models.Model):

    # context atributes
    COMPANION_CHOICES = (
            ('F','Family'),
            ('G','Group'),
            ('M','Mit Anyone'),
            ('A','Alone'),
            )
    companion = models.CharField(max_length=1, choices = COMPANION_CHOICES,default='A')

    WEATHER_CHOICES = (
            ('VH','Very Hot'),
            ('H','Hot'),
            ('A','Average'),
            ('C','Cold'),
            ('VC','Very Cold'),
            )
    weather = models.CharField(max_length=2, choices = WEATHER_CHOICES,default='A')

    MOTIVATION_CHOICES = (
            ('E','Education'),
            ('F','Fun'),
            ('B','Business'),
            )
    motivation = models.CharField(max_length=1, choices = MOTIVATION_CHOICES,default='F')

    date = models.DateTimeField(default=datetime.now, blank=True)

    # time context
    def _get_day_of_week(self):
        data = self.date.date().weekday()
        if data in (1,6):
            return "weekend"
        else:
            return "business_day"
    day_of_week = property(_get_day_of_week)

    def _get_local_time(self):
        hora = self.date.hour
        if hora<18 and hora>=8:
            return "diurno"
        else:
            return "noturno"
    local_time = property(_get_local_time)

    def _get_season(self):
        date = self.date.date()

        from bitte.apps.recommender.helper import Helper
        #h = Helper()
        #h.logger("date",date)
        #h.logger("m",date.month)
        #h.logger("d",date.day)
        #h.logger("y",date.year)
        month = date.month * 100
        day = date.day

        md = month + day
        #h.logger("md",md)

        if ((md > 320) and (md < 621)):
            return "fall"
            #return "spring"
        elif ((md > 620) and (md < 923)):
            return "winter"
            #return "summer"
        elif ((md > 922) and (md < 1223)):
            return "spring"
            #return "fall"
        else:
            return "summer"
            #return "winter"
    season = property(_get_season)

    #location context
    lat_position   = models.DecimalField (max_digits=8, decimal_places=6,null = True)
    long_position   = models.DecimalField (max_digits=8, decimal_places=6,null = True)

    def __unicode__(self):
        #return self.companion +" "+ self.weather+" "+ self.motivation +" "+self._get_day_of_week+" "+ self._get_local_time+" "+ self._get_season
        return self.companion +"|"+self.weather +"|"+ self.motivation+"|"+self.day_of_week+"|"+self.local_time+"|"+self.season

class CurrentContext(models.Model):
    current = models.BooleanField(default =True)
    distance_max = models.IntegerField(default =30)
    context = models.ForeignKey(Context)
    user = models.ForeignKey(User)

class Rating(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    context = models.ForeignKey(Context)
    value = models.IntegerField(blank = True,
                               null = True,
                               verbose_name = u'Rating')

    #def __unicode__(self):
    #    #return "i="+self.item +"c= "+ self.context +" u= "+ self.user +" r ="+ self.value