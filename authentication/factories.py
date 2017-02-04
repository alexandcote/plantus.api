from factory import (
    DjangoModelFactory,
    Faker,
    Sequence,
    PostGenerationMethodCall
)

from authentication.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    is_superuser = False
    is_staff = False
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Sequence(lambda n: 'user%d@plantustest.com' % n)
    password = PostGenerationMethodCall('set_password', 'qwer1234')
