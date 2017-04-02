from django.db.models import Avg

from plantus.celery import app
from pots.models import (
    Pot,
    TimeSerie,
    Operation)

NB_VALUE = 10


@app.task(bind=True)
def pots_analyser():
    """
    Task that analyse each pot of the database
    """
    # Todo Add some tests
    pots = Pot.objects.prefetch_related('plant').all()
    for pot in pots:
        pot_analyser.delay(pot)


@app.task
def pot_analyser(pot):
    """
    Task that analyse a pot and create operation
    """
    # Todo Add some tests
    time_series_average = TimeSerie.objects\
        .filter(pot=pot)\
        .values('pot_id')\
        .order_by('-date')[:NB_VALUE]\
        .aggregate(average_humidity=Avg('humidity'))

    if pot.plant.humidity_spec > time_series_average['average_humidity'] \
            and not Operation.objects.filter(
            pot=pot, action_id='water', completed_at__isnull=True).exists():
        Operation(action_id='water', pot=pot).save()
