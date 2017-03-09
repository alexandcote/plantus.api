from places.models import Place


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
