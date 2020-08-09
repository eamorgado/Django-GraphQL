from django.contrib import admin
from django.urls import path

from graphene_django.views import GraphQLView
from .schema import schema

#To allow post for users not authenticated => external apps => other types of auth
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/',csrf_exempt(GraphQLView.as_view(graphiql=True))), 
    #graphiql=True => enables testing (only during DEVELOPMENT)
]
