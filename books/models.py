from django.db import models
from django.contrib.auth.models import User 

class Book(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title
