import uuid

from places.models import Place


def create_place(data):
    """
    Create a place with parameters
    """
    name = data.get('name', '')
    identifier = data.get('identifier', uuid.uuid4())
    picture = data.get('picture', None)
    users = data.get('users', None)

    place = Place(name=name, identifier=identifier, picture=picture)
    place.save()

    if users:
        place.users.set(users)

    return place


def update_place(place, data):
    """
    Update a place with parameters
    """
    place.name = data.get('name', place.name)
    place.picture = data.get('picture', place.picture)
    users = data.get('users', None)

    if users:
        place.users.set(users)

    place.save()

    return place
