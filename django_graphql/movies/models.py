from django.db import models

#Model for Actor
class Actor(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


#Model for Movie
class Movie(models.Model):
    title = models.CharField(max_length=128)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField(default=1998)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)