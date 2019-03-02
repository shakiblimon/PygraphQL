from django.db import models

# Create your models here.
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

'''
    GraphQL Authentication JWT
'''
class Link(models.Model):
    url = models.URLField()
    descriptions = models.TextField(blank=True)

'''
#####################################
'''

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Model for Authorized django auth
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# django form implemetation

class Pet(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return  self.name

# class PetForm(models.Model):
#
#     class Meta:
#         models = Pet
#         fields = ('name')
#
# class PetType(DjangoObjectType):
#     class Meta:
#         models = Pet
#
# class PetMutation(DjangoModelFormMutation):
#     class Meta:
#         form_calss = PetForm
#         input_fields = 'data'
#         return_fields_name = 'my_pet'