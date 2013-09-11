from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateField()

    GENDER_CHOICES = (
            ('M','Masculino'),
            ('F','Feminino'),
            )
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES,default='M')

    def _get_age_group(self):
        age = date.today() - self.birthday
        days_in_year = 365
        age = age.days/ days_in_year

        if (age <18):
            return "teenager"
        elif ((age >= 18) and (age < 29)):
            return "Young Adult"
        elif ((age >= 29) and (age < 49)):
            return "Adult"
        else:
            return "Older People"

    age_group = property(_get_age_group)