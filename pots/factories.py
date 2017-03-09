from factory import (
    DjangoModelFactory,
    Sequence,
    SubFactory
)
from factory.fuzzy import FuzzyDecimal

from places.factories import PlaceFactory
from plants.factories import PlantFactory
from pots.models import (
    Pot,
    TimeSerie
)


class PotFactory(DjangoModelFactory):
    class Meta:
        model = Pot

    name = Sequence(lambda n: 'Pot #%d' % n)
    plant = SubFactory(PlantFactory)
    place = SubFactory(PlaceFactory)


class TimeSerieFactory(DjangoModelFactory):
    class Meta:
        model = TimeSerie

    pot = SubFactory(PotFactory)
    temperature = FuzzyDecimal(0, 100, 2)
    humidity = FuzzyDecimal(0, 100, 2)
    luminosity = FuzzyDecimal(0, 100, 2)
    water_level = FuzzyDecimal(0, 100, 2)

