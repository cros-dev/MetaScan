from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Usuário customizado do MetaScan.

    Campos:
        username: Identificador único (matrícula ou nome de usuário).
        email: Opcional, usado para recuperação de senha/admin.
        role: Papel do usuário no sistema (admin, gestor, conferente).
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Administrador")
        MANAGER = "MANAGER", _("Gestor")
        AUDITOR = "AUDITOR", _("Conferente")

    role = models.CharField(
        _("papel"),
        max_length=20,
        choices=Role.choices,
        default=Role.AUDITOR,
        help_text=_("Define as permissões do usuário no sistema."),
    )

    class Meta:
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        """Sobrescreve save para definir permissões baseadas no role."""
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.Role.MANAGER:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)
