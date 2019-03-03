import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from testapp.models import Link, Vote


class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']


class LinkNote(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)


class VoteNote(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces= (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNote)
    relay_links = DjangoFilterConnectionField(LinkNote, filterset_class=LinkFilter)


class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNote)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user

        link = Link(
            url=input.get('url'),description=input.get('description'),posted_by=user,
        )
        link.save()
        return RelayCreateLink(link=link)


class RelayMutation(graphene.ObjectType):
    relay_create_link = RelayCreateLink.Field()

