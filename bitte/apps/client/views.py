# Create your views here.
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request):

    if request.user.is_authenticated():
        return render_to_response('client/index.html',{'user':request.user})
    else:
       return render_to_response('client/index.html')

def recommender(request):
	return render_to_response("client/recommender.html")


def about(request):
	return render_to_response("client/about.html")

