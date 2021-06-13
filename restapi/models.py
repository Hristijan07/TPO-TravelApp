from django.db import models
# from users.models import User
from django.conf import settings


# Create your models here.

# Interest
class Interest(models.Model):
    class Meta:
        db_table = 'interest'

    interest_id = models.AutoField(primary_key=True)
    interest = models.CharField(max_length=100)
    pass

# Company
class Company(models.Model):
    class Meta:
        db_table = 'company'

    company_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=30)
    pass


# Trip
class Trip(models.Model):
    class Meta:
        db_table = 'trip'
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip_id = models.AutoField(primary_key=True)
    pass


# Destination
class Destination(models.Model):
    class Meta:
        db_table = 'destination'

    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    destination_id = models.AutoField(primary_key=True)
    postal_code = models.IntegerField()
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    n = models.FloatField()
    e = models.FloatField()
    ## n,e are longitude and latitude used for the maps
    """Budget da e MoneyField"""
    budget = models.IntegerField()
    pass


# Suggestion
class Suggestion(models.Model):
    class Meta:
        db_table = 'suggestion'

    destination_id = models.ForeignKey(Destination, on_delete=models.CASCADE)
    suggestion_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


# Like_Dislike
"""Da nema primary key"""
"""Kako one to one relationship???"""


class Like_Dislike(models.Model):
    class Meta:
        db_table = 'like/dislike'

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    suggestion_id = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    liked = models.BooleanField()


# Transport
class Transport(models.Model):
    class Meta:
        db_table = 'transport'

    transport_id = models.IntegerField(primary_key=True)
    transport_type = models.CharField(max_length=15)
    """Ticket da e MoneyField"""
    ticket = models.IntegerField()
