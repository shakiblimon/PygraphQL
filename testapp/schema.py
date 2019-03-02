import graphene
import graphql_jwt
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth import *

import testapp
from testapp.models import Category, Ingredient, Post, Link
from testapp.schema import CreateUser


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


# limiting Field Access
class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ['title', 'content']
        exclude_fields = ['published', 'owner']  # Adding excluded field into schema
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


'''
    Link model content
'''


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


'''
    create link 
'''


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


'''
    #####################################
'''
'''
        Create User 
'''


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Aguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

    class Mutation(graphene.ObjectType):
        create_link = CreateLink.Field()
        create_user = CreateUser.Field()

        token_auth = graphql_jwt.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()


#########################

class Query(object):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    ## Queryset Filtering On Lists

    all_posts = DjangoFilterConnectionField(PostNode)

    links = graphene.List(LinkType)

    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().Objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')

        return user
#####################################


    def resolve_link(self, info, **kwargs):
        return Link.objects.all()

    def resolve_all_posts(self, info):
        return Post.objects.filter(published=True)

    #   Userbased Filtering Onlist

    my_post = DjangoFilterConnectionField(PostNode)

    def resolve_ny_post(self, info):
        # context will referance to the Django request

        if not info.comtext.user.is_authenticated():
            return Post.objects.none()
        else:
            return Post.objects.filter(owner=info.comtext.user)
