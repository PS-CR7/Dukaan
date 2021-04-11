from rest_framework.authtoken.models import Token
from .models import *

class UserService(object):
    """
    """
    @staticmethod
    def get_user(**kwargs):
        try:
            user = Account.objects.get(**kwargs)
            return user
        except Account.DoesNotExist:
            return None

    @staticmethod
    def create_user(**kwargs):
        mob={}
        mob['mobile']=kwargs['mobile']
        user = Account.objects.create(**mob)
        if kwargs.get("otp"):
            user.set_password(kwargs["otp"])
            user.save()
        return user

    @staticmethod
    def create_signup(data):
        mobile = data.get("mobile")
        if UserService.get_user(mobile=mobile):
            return {"status": 500,
                    "message": "User Already Exists."}
        user = UserService.create_user(**data)
        return {"token": UserService.access_token(user)}

    @staticmethod
    def access_token(user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    
