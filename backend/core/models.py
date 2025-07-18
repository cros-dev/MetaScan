from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from django.core.validators import MinValueValidator

from metascan import settings

CAVALETE_STATUS_CHOICES = [
    ('available', 'Available'),
    ('assigned', 'Assigned'),
    ('inactive', 'Inactive'),
]

SLOT_SIDE_CHOICES = [
    ('A', 'Side A'),
    ('B', 'Side B'),
]
SLOT_STATUS_CHOICES = [
    ('available', 'Available'),
    ('auditing', 'Auditing'),
    ('pending', 'Pending'),
    ('completed', 'Completed'),
]

ACTION_CHOICES = [
    ('created', 'Created'),
    ('edited', 'Edited'),
    ('removed', 'Removed'),
    ('other', 'Other'),
]

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
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    sankhya_password = EncryptedCharField(max_length=128, null=True, blank=True) # type: ignore

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Cavalete(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='cavaletes'
    )
    status = models.CharField(max_length=20, choices=CAVALETE_STATUS_CHOICES, default='available')

    def save(self, *args, **kwargs):
        if not self.pk:
            last = Cavalete.objects.order_by('-id').first() # type: ignore
            next_num = 1
            if last and last.code and last.code.startswith('CAV'):
                try:
                    next_num = int(last.code[3:]) + 1
                except ValueError:
                    pass
            self.code = f'CAV{next_num:02d}'
            self.name = f'Cavalete {next_num:02d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Slot(models.Model):
    cavalete = models.ForeignKey(Cavalete, on_delete=models.CASCADE, related_name='slots')
    side = models.CharField(max_length=1, choices=SLOT_SIDE_CHOICES)
    number = models.IntegerField()
    product_code = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=30, choices=SLOT_STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('cavalete', 'side', 'number')

    def __str__(self):
        return f"{self.cavalete.name} - Side {self.side}{self.number}"

class SlotHistory(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='histories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    product_code = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    action = models.CharField(max_length=20, default='auditing')

class CavaleteHistory(models.Model):
    cavalete = models.ForeignKey(Cavalete, on_delete=models.SET_NULL, null=True, related_name='cavalete_histories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    previous_data = models.JSONField(null=True, blank=True)