import random
import string

from cryptography.fernet import Fernet
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', self.generate_random_word())
        extra_fields.setdefault('access_token', self.generate_random_word())
        extra_fields.setdefault('refresh_token', self.generate_random_word())
        extra_fields.setdefault('linkedin_id', self.generate_random_word())
        extra_fields.setdefault('full_name', self.generate_random_word())
        extra_fields.setdefault('picture', "http://127.0.0.1:8000/")
        extra_fields.setdefault('profile_link', "http://127.0.0.1:8000/")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    @staticmethod
    def generate_random_word():
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(10))


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False, blank=True, null=True)
    access_token = models.CharField(max_length=2000, unique=True)
    refresh_token = models.CharField(max_length=2000, unique=True, null=True)
    linkedin_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    picture = models.URLField(max_length=5000, null=True)
    profile_link = models.URLField(max_length=1000, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    ENCRYPTION_KEY = Fernet.generate_key()

    def encrypt(self, value):
        cipher_suite = Fernet(self.ENCRYPTION_KEY)
        encrypted_value = cipher_suite.encrypt(value.encode())
        return encrypted_value.decode()

    def decrypt(self, encrypted_value):
        cipher_suite = Fernet(self.ENCRYPTION_KEY)
        decrypted_value = cipher_suite.decrypt(encrypted_value.encode())
        return decrypted_value.decode()

    def save(self, *args, **kwargs):
        if self.access_token:
            self.access_token = self.encrypt(self.access_token)
        if self.refresh_token:
            self.refresh_token = self.encrypt(self.refresh_token)
        super().save(*args, **kwargs)

    def get_access_token(self):
        return self.decrypt(self.access_token)

    def get_refresh_token(self):
        return self.decrypt(self.refresh_token)

    def __str__(self):
        if self.is_superuser:
            return f'{self.id},{self.email}'
        return f'{self.id},{self.full_name}'
