# -*- coding:utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from bitte.apps.accounts.models import UserProfile
from bitte.apps.recommender.models import Context,CurrentContext
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
import  pywapi
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=100)

class RatingForm(forms.Form):
    int = forms.IntegerField()
    # email = forms.EmailField(label="Email")
    #item = forms.IntegerField(label="Item")
    #user = forms.IntegerField(label="User")
    #context = forms.IntegerField(label="Context")
    #value = forms.IntegerField(label="Value")

class SingupForm(forms.Form):
    email = forms.EmailField(label="Email")
    birthday = forms.DateField(required=True,label="Nascimento",widget=SelectDateWidget(years=range(1994,1932,-1)))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    birthday = forms.DateField(required=True,label="Nascimento",widget=SelectDateWidget(years=range(1994,1932,-1)))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Thats username is already taken, please select another.")


    def save(self,commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        UserProfile.objects.create(user=user,
                                   gender=self.cleaned_data['gender'],
                                   birthday=self.cleaned_data['birthday'])
        return user

class ContextForm(ModelForm):
    hiddenValues = forms.Form()
    hiddenValues.fields['lat_position'] = forms.DecimalField(widget=forms.widgets.HiddenInput())
    hiddenValues.fields['long_position'] = forms.DecimalField(widget=forms.widgets.HiddenInput())
    distance = forms.IntegerField()
    class Meta:
        model = Context
        fields = ['companion', 'motivation', 'date','lat_position','long_position']
        exclude = ['date','weather']

    def convert_grad_to_weather(self,grad):
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

    def save(self,request,commit=True):
        if request.user.is_authenticated():
            user = request.user
            contexto = super(ContextForm, self).save(commit=False)
            yahoo_result = pywapi.get_weather_from_yahoo('BRXX3272')
            grad = yahoo_result['condition']['temp']
            contexto.weather =  self.convert_grad_to_weather(grad)
            contexto.lat_position = self.cleaned_data["lat_position"]
            contexto.long_position = self.cleaned_data["long_position"]
            distance = self.cleaned_data["distance"]
            if commit:
                contexto.save()
                CurrentContext.objects.filter(user=user).update(current=False)
                CurrentContext.objects.create(user=user,context=contexto,distance_max = distance)
            ctx={
                'form': form
            }
            return distance

        else:
            return HttpResponse(u"precisa está logado")

form = ContextForm()
