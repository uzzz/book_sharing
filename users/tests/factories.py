import factory
from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    first_name = 'John'
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
