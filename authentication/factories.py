from factory import (
    DjangoModelFactory,
    Faker,
    Sequence,
    PostGenerationMethodCall
)
from factory import post_generation

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

    @post_generation
    def places(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for place in extracted:
                self.places.add(place)


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True
