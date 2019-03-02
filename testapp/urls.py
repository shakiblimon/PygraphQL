from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

from PygraphQL import schema

urlpatterns = [
    path('graphql',GraphQLView.as_view(graphiql=True , schema=schema)),
]