from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import Group




from authentification.managers import UserManager


from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    PATIENT = 'patient'
    MEDECIN = 'medecin'
    INFIRMIER = 'infirmier'
    PHARMACIEN = 'pharmacien'
    LABORANTIN = 'laborantin'
    RADIOLOGUE = 'radiologue'
    USER = 'user'

    ROLE_CHOICES = [
        ( PATIENT, 'Patient'),
        (MEDECIN, 'Medecin'),
        (INFIRMIER, 'Infirmier'),
        (PHARMACIEN, 'Pharmacien'),
        (LABORANTIN, 'Laborantin'),
        ( RADIOLOGUE, 'Radiologue'),
        (ADMIN, 'Admin'),
        (USER , 'User'),
    ]
    AUTH_PROVIDERS = {
        'email': 'email',
        'google': 'google',
        'github': 'github',
        'linkedin': 'linkedin'
    }
    id = models.BigAutoField(primary_key=True, editable=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    email = models.EmailField(max_length=255, verbose_name=_("Email"), unique=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"
    def assign_role(self, role_name):
        # Make sure the role name is valid
        if role_name in dict(self.ROLE_CHOICES).keys():
            self.role = role_name
            self.save()
        else:
            raise ValueError("Invalid role name")