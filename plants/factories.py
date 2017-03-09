from factory import (
    DjangoModelFactory,
    Sequence
)
from factory.fuzzy import (
    FuzzyText,
    FuzzyDecimal
)

from plants.models import Plant


class PlantFactory(DjangoModelFactory):
    class Meta:
        model = Plant

    name = Sequence(lambda n: 'Plant #%d' % n)
    description = FuzzyText(length=100)
    humidity_spec = FuzzyDecimal(0, 100, 2)
    luminosity_spec = FuzzyDecimal(0, 100, 2)
    temperature_spec = FuzzyDecimal(0, 100, 2)
