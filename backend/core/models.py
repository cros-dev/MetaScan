from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from .constants import ROLE_CHOICES

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    sankhya_password = EncryptedCharField(max_length=128, null=True, blank=True) # type: ignore
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='auditor')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def extract_names_from_email(self):
        """
        Extrai first_name e last_name do email no formato nome.sobrenome@metalaluminio.com.br
        """
        if self.email and '@metalaluminio.com.br' in self.email:
            # Remove o domínio
            email_part = self.email.replace('@metalaluminio.com.br', '')
            # Divide por ponto
            parts = email_part.split('.')
            if len(parts) >= 2:
                self.first_name = parts[0].title()
                self.last_name = parts[1].title()
            elif len(parts) == 1:
                self.first_name = parts[0].title()
                self.last_name = ''

    def save(self, *args, **kwargs):
        # Extrai nomes do email se não estiverem definidos
        if not self.first_name and not self.last_name and self.email:
            self.extract_names_from_email()
            
        if self.is_superuser:
            super().save(*args, **kwargs)
            return
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'manager':
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'