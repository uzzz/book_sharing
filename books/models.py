from django.db import models
from django.contrib.auth.models import User
from django_fsm.db.fields import FSMField, transition

class Book(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='free')

    def __unicode__(self):
        return self.title

class BookRequest(models.Model):
    # TODO: add requester + book unique index
    requester = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    requested = models.DateTimeField(auto_now_add=True)
