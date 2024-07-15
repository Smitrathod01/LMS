from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# we are using because django provides default login by username and password and if we want to do with email and password then use it in views
class EmailBackEnd(ModelBackend):
    def authenticate(self,  username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
