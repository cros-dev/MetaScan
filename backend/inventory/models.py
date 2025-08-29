from django.db import models
from django.conf import settings
from core.constants import ACTION_CHOICES

class SlotHistory(models.Model):
    slot = models.ForeignKey('cavaletes.Slot', on_delete=models.CASCADE, related_name='histories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    product_code = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    action = models.CharField(max_length=20, default='auditing')

    class Meta:
        verbose_name = 'Histórico de Slot'
        verbose_name_plural = 'Históricos de Slots'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.slot} - {self.action} - {self.timestamp}"

class CavaleteHistory(models.Model):
    cavalete = models.ForeignKey('cavaletes.Cavalete', on_delete=models.SET_NULL, null=True, related_name='cavalete_histories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    previous_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Histórico de Cavalete'
        verbose_name_plural = 'Históricos de Cavaletes'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.cavalete} - {self.action} - {self.timestamp}"
