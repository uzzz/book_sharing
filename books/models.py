from django.db import models
from django.contrib.auth.models import User
from django_fsm.db.fields import FSMField, transition

class Book(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='free')

    @transition(source='free', target='requested', save=True)
    def request(self, requester):
        if requester == self.owner:
            raise BookRequestError('Unable to request own book')

        BookRequest(requester=requester, book=self).save()

    @transition(source='free', target='reading', save=True)
    def read(self):
        pass

    @transition(source='requested', target='given', save=True)
    def give(self, requester):
        book_request = BookRequest.objects.get(requester=requester,
            is_confirmed=False, book=self)
        book_request.is_confirmed = True
        book_request.save()

    @transition(source='given', target='free', save=True)
    def return_to_owner(self):
        book_request = BookRequest.objects.get(book=self, is_confirmed=True)
        book_request.delete()

    @transition(source='reading', target='free', save=True)
    def finish_reading(self):
        pass

    def requests(self):
        return BookRequest.objects.filter(book=self)

    def __unicode__(self):
        return self.title

class BookRequest(models.Model):
    # TODO: add requester + book unique indexa
    requester = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    requested = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

class BookRequestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
