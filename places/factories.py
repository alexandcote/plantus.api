import string

from factory import (
    DjangoModelFactory,
    Sequence
)
from factory import post_generation
from factory.fuzzy import FuzzyText
from places.models import Place


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = Place

    name = Sequence(lambda n: 'Villa #%d' % n)
    ip_address = '127.0.0.1'
    port = FuzzyText(length=4, chars=string.digits)

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)