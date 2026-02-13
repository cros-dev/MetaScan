from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Cavalete(models.Model):
    """
    Representa um cavalete físico que contém slots de produtos.
    Pode ser atribuído a um conferente (User).
    """

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", _("Disponível")
        IN_PROGRESS = "IN_PROGRESS", _("Em conferência")
        COMPLETED = "COMPLETED", _("Concluído")
        BLOCKED = "BLOCKED", _("Bloqueado")

    code = models.CharField(_("código"), max_length=50, unique=True, db_index=True)
    name = models.CharField(_("nome/descrição"), max_length=100, blank=True)

    # Usuário responsável pela conferência atual
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_cavaletes",
        verbose_name=_("conferente responsável"),
    )

    status = models.CharField(
        _("status"),
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("cavalete")
        verbose_name_plural = _("cavaletes")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.get_status_display()}"


class Slot(models.Model):
    """
    Posição específica dentro de um cavalete (ex: Lado A, Posição 1).
    Armazena o produto e a quantidade conferida.
    """

    class Side(models.TextChoices):
        SIDE_A = "A", _("Lado A")
        SIDE_B = "B", _("Lado B")

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", _("Aguardando")
        AUDITING = "AUDITING", _("Em conferência")
        COMPLETED = "COMPLETED", _("Conferido")

    cavalete = models.ForeignKey(
        Cavalete,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name=_("cavalete"),
    )

    side = models.CharField(_("lado"), max_length=1, choices=Side.choices)
    number = models.PositiveIntegerField(_("número da posição"))

    product_code = models.CharField(
        _("código do produto"), max_length=50, blank=True, null=True
    )
    product_description = models.CharField(
        _("descrição do produto"), max_length=255, blank=True, null=True
    )

    quantity = models.PositiveIntegerField(_("quantidade"), default=0)

    status = models.CharField(
        _("status"),
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("slot")
        verbose_name_plural = _("slots")
        ordering = ["cavalete", "side", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["cavalete", "side", "number"], name="unique_slot_position"
            )
        ]

    def __str__(self):
        return f"{self.cavalete.code} - {self.side}{self.number}"
