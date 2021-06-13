from django.contrib.auth.models import AbstractUser
from django.db import models
from restapi.models import Interest, Company


class User(AbstractUser):
    class Meta:
        db_table = 'users_user'

    photo = models.URLField(blank=True)
    age = models.IntegerField(blank=True, null = True)
    gender = models.CharField(max_length=20, blank=True, null = True)
    recieve_emails = models.BooleanField(null = True)
    interests = models.ManyToManyField(Interest)
    company = models.ManyToManyField(Company)

    def __str__(self):
        return self.username