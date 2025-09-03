from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()

class EmailBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            print(user)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            print("here")
            return user
        else:
            return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None