from factory import DjangoModelFactory
from factory import Sequence
from factory import SubFactory

from places.factories import PlaceFactory
from plants.factories import PlantFactory
from pots.models import Pot


class PotsFactory(DjangoModelFactory):
    class Meta:
        model = Pot

    name = Sequence(lambda n: 'Pot #%d' % n)
    plant = SubFactory(PlantFactory)
    place = SubFactory(PlaceFactory)
