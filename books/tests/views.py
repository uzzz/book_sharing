from django.test import TestCase
from django.test.client import Client

from factories import BookFactory
from users.tests.factories import UserFactory
from books.models import Book
from core.tests.mixins import LoginMixin


class AllBooksListViewTests(TestCase, LoginMixin):
    def setUp(self):
        self.client = Client()
        self.book1 = BookFactory.create()
        self.book2 = BookFactory.create()

    def test_books_list(self):
        response = self.client.get('/books/all/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book2.title)

class MyBooksListViewTests(TestCase, LoginMixin):
    def setUp(self):
        self.client = Client()

    def test_books_list_not_logged(self):
        response = self.client.get('/books/my/')

        self.assertRedirects(response, '/accounts/login/?next=/books/my/')

    def test_books_list_logged(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create()

        book1 = BookFactory.create(owner=user1)
        book2 = BookFactory.create(owner=user1)
        book3 = BookFactory.create(owner=user2)

        with self.login(user1):
            response = self.client.get('/books/my/')

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, book1.title)
            self.assertContains(response, book2.title)
            self.assertNotContains(response, book3.title)

class MyBookEditViewTest(TestCase, LoginMixin):
    #total cut-n-paste from delete test
    #to do refactor test
    def setUp(self):
        self.client = Client()
        self.book = BookFactory.create()
        self.user = UserFactory.create()

    def test_edit_book_not_logged(self):
        response = self.client.post('/books/%d/edit/' % self.book.id)
        self.assertRedirects(response,
                '/accounts/login/?next=/books/%d/edit/' % self.book.id)
        self.assertEqual(self.book, Book.objects.get(pk=self.book.pk))

    def test_delete_not_my_book(self):
        with self.login(self.user):
            response = self.client.post('/books/%d/edit/' % self.book.id)

            self.assertEqual(response.status_code, 404)


class MyBookDeleteViewTest(TestCase, LoginMixin):
    def setUp(self):
        self.client = Client()
        self.book = BookFactory.create()
        self.user = UserFactory.create()

    def test_delete_book_not_logged(self):
        response = self.client.post('/books/%d/delete/' % self.book.id)

        self.assertRedirects(response,
                '/accounts/login/?next=/books/%d/delete/' % self.book.id)
        self.assertEqual(self.book, Book.objects.get(pk=self.book.pk))

    def test_delete_not_my_book(self):
        with self.login(self.user):
            response = self.client.post('/books/%d/delete/' % self.book.id)

            self.assertEqual(response.status_code, 404)

    def test_delete_my_book(self):
        self.book.owner = self.user
        self.book.save()

        with self.login(self.user):
            response = self.client.post('/books/%d/delete/' % self.book.id)

            self.assertRedirects(response, '/books/my/')
            self.assertEqual(Book.objects.filter(id=self.book.id).count(), 0)
