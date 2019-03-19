from django.conf import settings
from django.db import models

# Create your models here.
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

'''
    GraphQL Authentication JWT
'''
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    link = models.ForeignKey('testapp.Link', related_name='votes', on_delete=models.CASCADE)

