# PygraphQL
A GraphQL & Django project for api intregation.
### Set Up / Installation
```shell
pip install django 
pip install graphene_django
pip install graphql_django
```
For **_JWT_** Authentication
```shell
pip install django-graphql-jwt
```
### Configuring Graphene Django

On the **{django_project_name}**/```settings.py```, add the following:
```python
INSTALLED_APPS = (
    # At the end of all the default packages
    'graphene_django',
)
```
### Schema Settings
Set your schema into ```settings.py```
```python
GRAPHENE = {
    'SCHEMA': '{django_project_name}.schema.schema',
}
```
**django_project_name == your django project name**
```python
import graphene
import {app_name}.schema
```
Query for getting the data from the server.
```python
class Query({app_name}.schema.Query, graphene.ObjectType):
    pass
```


# Create schema
```shell
schema = graphene.Schema(query=Query,mutation = Mutation)
```
**{app_name} == Your django project app name.**

### Authorization in Django
The concept of authentication and authorization is enabled by default in Django using sessions. Since most of the web apps today are stateless, 
we are going to use the [django-graphql-jwt](https://github.com/flavors/django-graphql-jwt) library to implement ```JWT Tokens``` in Graphene.

#### Configuring django-graphql-jwt
In the ```PygraphQL/settings.py``` file, add a new ```MIDDLEWARE```:

```python
MIDDLEWARE = [
    # After django.contrib.auth.middleware.AuthenticationMiddleware
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
]
```
In the same file, add the ```AUTHENTICATION_BACKENDS``` setting:
```python
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

### Creating your query
GraphQL query language is all about selecting fields on objects.

#### Using Relay on Links
Graphene has complete support for Relay and offers some utils to make integration from Python easy.Create 
**_schema_relay.py_** into project directory go over the essential changes:
```python
class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)

```
- Relay allows you to use ``` django-filter``` for filtering data. Here, you’ve defined a FilterSet, with the __url__ 
and __description__ fields.
- The data is exposed in Nodes, so you must create one for the links.
- Each node implements an interface with an unique ID (you’ll see the result of this in a bit).
- Uses the ```LinkNode``` with the ```relay_link``` field inside your new query.

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

