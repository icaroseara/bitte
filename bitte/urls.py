from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.auth.views import login,logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bitte.apps.client.views.index', name='client_index'),
    url(r'^about/$', 'bitte.apps.client.views.about', name='client_about' ),
    #url(r'^crawl/$', 'bitte.apps.recommender.views.crawl'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='accounts_logout'),
    url(r'^profile/$', 'bitte.apps.accounts.views.profile', name='accounts_profile'),
    url(r'^recommendations/$', 'bitte.apps.accounts.views.current_context', name='accounts_context'),
    url(r'^signup/$', 'bitte.apps.accounts.views.signup'),
    url(r'^login/$', 'bitte.apps.accounts.views.login_custom', name='accounts_login'),
    url(r'^discover/$', 'bitte.apps.accounts.views.discover', name='accounts_discover'),
    url(r'^rate/$', 'bitte.apps.accounts.views.rate'),
    url(r'^crawl_items/$', 'bitte.apps.recommender.views.generate_items'),
    url(r'^crawl_user_ratings/$', 'bitte.apps.recommender.views.generate_user_ratings'),
    url(r'^evaluate/$', 'bitte.apps.recommender.views.evaluate'),

)
urlpatterns += patterns('',
               (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
              )
#(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
