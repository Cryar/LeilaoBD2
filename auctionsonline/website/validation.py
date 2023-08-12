from django.contrib.auth import authenticate
from .models import Users

def validate_login(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        print('Bem vindo')
        return True
    else:
        print('Invalido')
        return False

def validate_registration(username, password1, password2, email):
    user = Users.objects.filter(username=username)

    if user:
        print('User already exists')
        return False
    if password1 != password2:
        return False
    email = Users.objects.filter(email=email)
    if email:
        print('Email already exists')
        return False

    return True
