from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from core.constants import CAVALETE_STATUS_CHOICES, CAVALETE_TYPE_CHOICES, SLOT_SIDE_CHOICES, SLOT_STATUS_CHOICES

class Cavalete(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20, choices=CAVALETE_TYPE_CHOICES, default='corredor')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='cavaletes'
    )
    status = models.CharField(max_length=20, choices=CAVALETE_STATUS_CHOICES, default='available')

    def save(self, *args, **kwargs):
        if not self.pk:
            last = Cavalete.objects.order_by('-id').first()
            next_num = 1
            if last and last.code and last.code.startswith('CAV'):
                try:
                    next_num = int(last.code[3:]) + 1
                except ValueError:
                    pass
            self.code = f'CAV{next_num:02d}'
            self.name = f'Cavalete {next_num:02d}'
        super().save(*args, **kwargs)

    def get_slot_count(self):
        if self.type == 'torre':
            return 12
        return 6

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cavalete'
        verbose_name_plural = 'Cavaletes'

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
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'

    def __str__(self):
        return f"{self.cavalete.name} - Side {self.side}{self.number}"
