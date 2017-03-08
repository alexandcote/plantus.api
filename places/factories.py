from factory import (
    DjangoModelFactory,
    Sequence
)
from factory import post_generation

from places.models import Place


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = Place

    name = Sequence(lambda n: 'Villa #%d' % n)

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)
