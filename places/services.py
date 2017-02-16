from places.models import Place
from plantus.tasks import task_to_water_pot


def create_place(data):
    """
    Create a place with parameters
    """
    name = data.get('name', '')
    ip_address = data.get('ip_address', '0.0.0.0')
    port = data.get('port', 0)
    users = data.get('users', None)

    place = Place(name=name, ip_address=ip_address, port=port)
    place.save()

    if users:
        place.users.set(users)

    return place


def update_place(place, data):
    """
    Update a place with parameters
    """
    place.name = data.get('name', place.name)
    place.ip_address = data.get('ip_address', place.ip_address)
    place.port = data.get('port', place.port)
    users = data.get('users', None)

    if users:
        place.users.set(users)

    place.save()

    return place


def service_to_water_all_pots(place):
    time = 5
    for pot in place.pots.all():
        task_to_water_pot.delay(pot.id, time)
