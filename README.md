# PygraphQL
A GraphQL & Django project for api intregation.
### Set Up / Installation
```
pip install django 
pip install graphene_django
pip install graphql_django
```
### Configuring Graphene Django

On the **{django_project_name}/settings.py**, add the following:
```
INSTALLED_APPS = (
    # At the end of all the default packages
    'graphene_django',
)
```
### Schema Settings
```
GRAPHENE = {
    'SCHEMA': '{django_project_name}.schema.schema',
}
```
**django_project_name == your django project name**
```
import graphene
import {app_name}.schema

# Query for getting the data from the server.
class Query({app_name}.schema.Query, graphene.ObjectType):
    pass

# Create schema
schema = graphene.Schema(query=Query)
```
### Authorization in Django
There are several ways you may want to limit access to data when working with Graphene and Django: 
limiting which fields are accessible via GraphQL and limiting which objects a user can access.

Let’s use a simple example model:
```
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

```
owner = models.ForeignKey(**'auth.User'**, on_delete=models.CASCADE)

### Creating your query
**GraphQL query language is all about selecting fields on objects.**

#### Using Relay
>Graphene has complete support for Relay and offers some utils to make integration from Python easy.

**Example**
```.env
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )
```
interfaces = (**relay.Node**,)




