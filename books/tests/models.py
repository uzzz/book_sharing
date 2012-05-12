from django.test import TestCase

from books.models import *
from books.tests.factories import BookFactory
from users.tests.factories import UserFactory

class BookModelTests(TestCase):
    def setUp(self):
        pass

    def test_requests(self):
        user = UserFactory.create()
        book = BookFactory.create()
        request = BookRequest(book=book, requester=user)
        request.save()
        self.assertEqual(list(book.requests()), [request])
