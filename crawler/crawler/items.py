# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AttractionItem(Item):
    name = Field()
    description = Field()
    location = Field()
    long_position = Field()
    lat_position = Field()
    photo = Field()
class UrlItem(Item):
    url = Field()

class RatingItem(Item):
    url = Field()
    rate = Field()
    date = Field()
    #companion
    #weather
    #motivation
    total = Field()
class ReviewItem(Item):
    atraction = Field()
    rate = Field()
    date = Field()
    user = Field()
class Profile(Item):
    name = Field()
    email = Field()
    birthday = Field()
    gender = Field()
