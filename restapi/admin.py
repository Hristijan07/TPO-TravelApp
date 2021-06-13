from django.contrib import admin
from .models import Destination, Trip, Interest, Suggestion, Like_Dislike, Transport, Company

# Register your models here.

admin.site.register(Destination)
admin.site.register(Trip)
admin.site.register(Interest)
admin.site.register(Suggestion)
admin.site.register(Like_Dislike)
admin.site.register(Transport)
admin.site.register(Company)
