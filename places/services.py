from places.models import Place
from plantus.tasks import task_to_water_pot


def create_place(data):
    """
    Create a place with parameters
    """
    name = data.get('name', '')
    users = data.get('users', None)

    place = Place(name=name)
    place.save()

    if users:
        place.users.set(users)

    return place


def update_place(place, data):
    """
    Update a place with parameters
    """
    place.name = data.get('name', place.name)
    users = data.get('users', None)

    if users:
        place.users.set(users)

    place.save()

    return place


def service_to_water_all_pots(place):
    """ 
    Task to water pots in a place
    TODO: Add tests when the function is completed 
    """
    time = 5
    for pot in place.pots.all():
        task_to_water_pot.delay(pot.id, time)
