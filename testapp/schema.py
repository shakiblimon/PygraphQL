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
        filter_fields = ['title', 'content']
        exclude_fields = ['published', 'owner'] #   Adding excluded field into schema
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        try:
            post = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        if post.published or info.context.user == post.owner:
            return post
        return None


class Query(object):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    ## Queryset Filtering On Lists

    all_posts = DjangoFilterConnectionField(PostNode)

    def resolve_all_posts(self,info):
        return Post.objects.filter(published=True)

    #   Userbased Filtering Onlist

    my_post = DjangoFilterConnectionField(PostNode)

    def resolve_ny_post(self,info):
        #context will referance to the Django request

        if not info.comtext.user.is_authenticated():
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.comtext.user)