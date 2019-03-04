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
Set your schema into **_settings.py_**
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
**{app_name} == Your django project app name.**

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

```.env
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )
```
interfaces = (**relay.Node**,)

### GraphQL & Django debuging middleware

You can debug your GraphQL queries in a similar way to django-debug-toolbar, but outputing in the results in 
GraphQL response as fields, instead of the graphical HTML interface.
Set it into **_settings.py_**
```.env
GRAPHENE = {
    'SCHEMA': 'PygraphQL.schema.schema',
    'MIDDLEWARE': [
        'grapehe_django.debug.DjangoDebugMiddleware'
    ]
}
```
### Screenshot
Create User

![create_user](https://user-images.githubusercontent.com/15167039/53692245-98e50980-3db6-11e9-9caf-262d1d8e45bf.png)


Generating Token For User

![generating_token](https://user-images.githubusercontent.com/15167039/53692273-eb262a80-3db6-11e9-8975-550ae3121665.png)


Verify Token

![verify_token](https://user-images.githubusercontent.com/15167039/53692282-17da4200-3db7-11e9-879b-97d7f85bbfbe.png)

Create Link

![create_link](https://user-images.githubusercontent.com/15167039/53711349-f4250380-3e6b-11e9-83b7-22efdeff4fee.png)


Query Link

![query](https://user-images.githubusercontent.com/15167039/53711408-2f273700-3e6c-11e9-8d4d-0a2eaf02ca63.png)

