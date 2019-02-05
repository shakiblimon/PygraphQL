from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from testapp.models import Category, Ingredient, Post


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node,)


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node,)

#limiting Field Access

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        only_fields = ('title', 'content')
        exclude_fields = ('published', 'owner') #   Adding excluded field into schema
        interfaces = (relay.node)


class Query(object):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    ## Queryset Filtering On Lists

    all_posts = DjangoFilterConnectionField(PostNode)
    def resolve_all_posts(self,info):
        return Post.objects.filter(published=True)
