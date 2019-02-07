import http

from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.rest_framework.tests.test_mutation import MyModelSerializer

from testapp.models import Post


class AwsomeModelMutation(SerializerMutation):
    class Meta:
        serializer_class = MyModelSerializer
        model_operations = ['create','update']
        lookup_field = 'id'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        if 'id' is input:
            instance = Post.objects.filter(id=input['id'], owner = info.context.user).first()
            if instance:
                return { 'instance': instance, 'data': input, 'patial':True}
            else:
                raise  http.Http404