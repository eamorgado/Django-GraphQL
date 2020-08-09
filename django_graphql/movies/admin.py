from django.contrib import admin
from .models import Actor, Movie

class Actors(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class Movies(admin.ModelAdmin):
    list_display = ('title','year',)

admin.site.register(Actor, Actors)
admin.site.register(Movie, Movies)

