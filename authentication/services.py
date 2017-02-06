from authentication.models import User


def create_user(data):
    """
    Create a user with parameters and log the transaction
    """
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email', None)
    password = data.get('password', None)
    is_staff = data.get('is_staff', False)
    is_superuser = data.get('is_superuser', False)

    normalize_email = User.objects.normalize_email(email)
    user = User(email=normalize_email, first_name=first_name,
                last_name=last_name, is_staff=is_staff,
                is_superuser=is_superuser)

    user.set_password(password)
    user.save()

    return user


def update_user(user, data):
    """
    Update user with parameters and log the transaction
    """
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.is_staff = data.get('is_staff', user.is_staff)
    user.is_superuser = data.get('is_superuser', user.is_superuser)
    password = data.get('password', None)

    if password:
        user.set_password(password)

    user.save()

    return user
