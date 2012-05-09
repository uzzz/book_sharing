import factory
from books.models import Book
from users.tests.factories import UserFactory

class BookFactory(factory.Factory):
    FACTORY_FOR = Book

    title = factory.Sequence(lambda n: 'Book title {0}'.format(n))
    owner = factory.LazyAttribute(lambda a: UserFactory())
