# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, render, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from bitte.apps.accounts.forms import RegisterForm, ContextForm, SingupForm, RatingForm
from django.http import HttpResponse
from bitte.apps.recommender.models import Item, CurrentContext, Context
from bitte.apps.accounts.forms import LoginForm
from django.contrib.auth import authenticate, login
from bitte.apps.recommender.recommend import UserBasedRecommender
from django.contrib.auth.models import User, check_password
from django.db.models import Count
from bitte.apps.accounts.models import UserProfile
from bitte.apps.recommender.models import *
import datetime
@login_required
def profile(request):
    ratings = Rating.objects.filter(user = request.user.get_profile().user_id )
    rec = []
    for r in ratings:
        it = Item.objects.filter(id=r.item_id)
        safe_str = it[0].name.encode('ascii', 'ignore')
        complete = (int(r.value*2),safe_str)
        rec.append(complete)
    ctx = {
        'profile': request.user.get_profile(),
        'user': request.user,
        'ratings': rec,
    }
    return render_to_response("accounts/profile.html", ctx, context_instance=RequestContext(request))

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]

        login(request, user)

        return redirect(reverse('accounts_profile'))
    ctx = {
        'form': form
    }
    return render_to_response('accounts/register.html', ctx, context_instance=RequestContext(request))


def discover(request, distance):
    if request.user.is_authenticated():
        user = request.user
        user_recommender = UserBasedRecommender()

        user_recommender.MAX_DISTANCE = distance
        user_recommender.USER_ID = user.id
        current_context = CurrentContext.objects.get(current=True, user=user)
        user_id = user.id
        #helper = Helper()
        #helper.logger("current context",str(current_context))
        list_recommentations = user_recommender.recommend(current_context)

        recommendation = list_recommentations

        return render_to_response('accounts/recommendation.html', {'recomendations': recommendation,'user':user,'context':current_context})
    else:
        return HttpResponse(u"precisa está logado")

def rate(request):

            item_id = request.POST['item_id']
            user_id = request.POST['user_id']
            context_id = request.POST['context_id']
            value = request.POST['value']

            p, created = Rating.objects.get_or_create(item_id=item_id,user_id=user_id,context_id=context_id,value=value)
            if created:
                return redirect(reverse('accounts_profile'))
            else:
                return HttpResponse(u"2")
def signup(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            gender = request.POST['gender']
            email = request.POST['email']
            password = request.POST['password']
            birthday_day = request.POST['birthday_day']
            birthday_month = request.POST['birthday_month']
            birthday_year = request.POST['birthday_year']
            birthday = datetime.date(int(birthday_year),int(birthday_month), int(birthday_day))

            user = User.objects.filter(username=str(username)).values('username')
            if not len(user):
                user = User.objects.create_user(username, email, password)
                UserProfile.objects.create(user=user,
                                           gender=gender,
                                           birthday=birthday)
                user_cache = authenticate(username=username, password=password)
                if user_cache:
                    login(request, user_cache)
                    return redirect(reverse('accounts_profile'))
                else:
                    return HttpResponse(u"1")
            else:
                return HttpResponse(u"2")
    return HttpResponse(u"3")

def login_custom(request):
    username = password = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(email=email).values('username')
            if len(user):
                user_cache = authenticate(username=user, password=password)
                if user_cache:
                    login(request, user_cache)
                    return redirect(reverse('accounts_context'))
                else:
                    erro = u"Email ou senha estão incorretos."
                    return render_to_response('client/index.html', {'erro': erro})
            else:
                erro = u"Email não cadastrado."
                return render_to_response('client/index.html', {'erro': erro})
    return render_to_response('client/index.html')


def current_context(request):
    form = ContextForm(request.POST or None)
    if form.is_valid():
        distance = form.save(request)
        return discover(request, distance)

    ctx = {
        'form': form
    }
    return render_to_response('accounts/current_context.html', ctx, context_instance=RequestContext(request))