from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# import User model


User = get_user_model()
def create_user(username, email, password):
    """
    Create a new user with the given username, email, and password.
    """
    user = User.objects.create_user(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def set_password(user, password):
    """
    Set the password for a user.
    """
    user.set_password(password)
    user.save()
    return user
