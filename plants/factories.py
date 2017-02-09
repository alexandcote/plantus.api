from factory import (
    DjangoModelFactory,
    Sequence
)
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyDecimal

from plants.models import Plant


class PlantFactory(DjangoModelFactory):
    class Meta:
        model = Plant

    name = Sequence(lambda n: 'Plant #%d' % n)
    description = FuzzyText(length=100)
    humidity_spec = FuzzyDecimal(0, 100)
    luminosity_spec = FuzzyInteger(0, 100)
    temperature_spec = FuzzyInteger(0, 100)
