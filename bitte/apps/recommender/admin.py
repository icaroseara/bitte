from django.contrib import admin
from bitte.apps.recommender.models import Context,Rating,Item,Category,State,City,ItemPhoto

admin.site.register(Context)
admin.site.register(Rating)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(State)
admin.site.register(City)
admin.site.register(ItemPhoto)


