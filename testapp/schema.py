from django.db.models import Q

import graphene
from graphene_django import DjangoObjectType

# class CategoryNode(DjangoObjectType):
#     class Meta:
#         model = Category
#         filter_fields = ['name', 'ingredients']
#         interfaces = (relay.Node,)
#
#
# class IngredientNode(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         # Allow for some more advanced filtering here
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith'],
#             'notes': ['exact', 'icontains'],
#             'category': ['exact'],
#             'category__name': ['exact'],
#         }
#         interfaces = (relay.Node,)
#
#
# # limiting Field Access
# class PostNode(DjangoObjectType):
#     class Meta:
#         model = Post
#         filter_fields = ['title', 'content']
#         exclude_fields = ['published', 'owner']  # Adding excluded field into schema
#         interfaces = (relay.Node,)
#
#     @classmethod
#     def get_node(cls, info, id):
#         try:
#             post = cls._meta.model.objects.get(id=id)
#         except cls._meta.model.DoesNotExist:
#             return None
#
#         if post.published or info.context.user == post.owner:
#             return post
#         return None
from graphql import GraphQLError

from testapp.models import Link, Vote
from users.schema import UserType

'''
    Link model Type
'''


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


'''
    Vote Model Type
'''


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


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


#
#          Create Link Query
# ----------------------------------------------
class Query(object):
    # category = relay.Node.Field(CategoryNode)
    # all_categories = DjangoFilterConnectionField(CategoryNode)
    #
    # ingredient = relay.Node.Field(IngredientNode)
    # all_ingredients = DjangoFilterConnectionField(IngredientNode)
    #
    # ## Queryset Filtering On Lists
    #
    # all_posts = DjangoFilterConnectionField(PostNode)

    links = graphene.List(
        LinkType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    def resolve_link(self, info, search=None, first=None, skip=None, **kwargs):
        qs=Link.objects.all()

        if search:
            filter = (
                    Q(url__icontains=search) |
                    Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip::]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

    #####################################
    #
    #
    #
    # def resolve_all_posts(self, info):
    #     return Post.objects.filter(published=True)
    #
    # #   Userbased Filtering Onlist
    #
    # my_post = DjangoFilterConnectionField(PostNode)
    #
    # def resolve_ny_post(self, info):
    #     # context will referance to the Django request
    #
    #     if not info.comtext.user.is_authenticated():
    #         return Post.objects.none()
    #     else:
    #         return Post.objects.filter(owner=info.comtext.user)

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()