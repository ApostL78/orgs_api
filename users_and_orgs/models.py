from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Model of user without username"""

    username = None
    email = models.EmailField("Email адрес", unique=True)
    phone = models.CharField("Номер телефона", max_length=12, blank=True, null=True)
    avatar = models.ImageField(
        "Аватар", upload_to="avatars/%Y/%m/%d", null=True, blank=True
    )
    organizations = models.ManyToManyField(
        "Organization", blank=True, related_name="employees"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Organization(models.Model):
    """Model of organisation"""

    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
