from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Action(models.TextChoices):
    CREATE = "CREATE", _("Criação")
    UPDATE = "UPDATE", _("Atualização")
    DELETE = "DELETE", _("Exclusão")
    STATUS_CHANGE = "STATUS_CHANGE", _("Mudança de Status")
    START_AUDIT = "START_AUDIT", _("Início de Conferência")
    FINISH_AUDIT = "FINISH_AUDIT", _("Fim de Conferência")
    ASSIGN = "ASSIGN", _("Atribuição")


class CavaleteHistory(models.Model):
    """Histórico de ações em Cavaletes."""

    cavalete = models.ForeignKey(
        "cavaletes.Cavalete",
        on_delete=models.SET_NULL,
        null=True,
        related_name="history",
        verbose_name=_("cavalete"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("usuário"),
    )
    action = models.CharField(_("ação"), max_length=20, choices=Action.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Snapshot dos dados relevantes no momento da ação
    description = models.TextField(_("descrição"), blank=True)

    class Meta:
        verbose_name = _("histórico de cavalete")
        verbose_name_plural = _("históricos de cavaletes")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.cavalete} - {self.action} by {self.user}"


class SlotHistory(models.Model):
    """Histórico de ações em Slots."""

    slot = models.ForeignKey(
        "cavaletes.Slot",
        on_delete=models.SET_NULL,
        null=True,
        related_name="history",
        verbose_name=_("slot"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("usuário"),
    )
    action = models.CharField(_("ação"), max_length=20, choices=Action.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Snapshot dos dados
    old_product_code = models.CharField(max_length=50, blank=True, null=True)
    new_product_code = models.CharField(max_length=50, blank=True, null=True)
    old_quantity = models.PositiveIntegerField(null=True)
    new_quantity = models.PositiveIntegerField(null=True)

    description = models.TextField(_("descrição"), blank=True)

    class Meta:
        verbose_name = _("histórico de slot")
        verbose_name_plural = _("históricos de slots")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.slot} - {self.action} by {self.user}"
