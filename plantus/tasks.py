from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from pots.models import Pot


@shared_task
def task_to_water_pot(pot_id, time):
    try:
        pot = Pot.objects.get(id=pot_id)
        print(pot, time)
    except ObjectDoesNotExist:
        print("Error pot with ({id}) does not exist".format(id=pot_id))
