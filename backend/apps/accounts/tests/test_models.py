import pytest
from apps.accounts.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_admin(self):
        """Testa se ADMIN recebe permissões de staff e superuser."""
        user = User.objects.create_user(
            username="admin_user", password="password123", role=User.Role.ADMIN
        )
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_create_user_manager(self):
        """Testa se MANAGER recebe permissão de staff mas não de superuser."""
        user = User.objects.create_user(
            username="manager_user", password="password123", role=User.Role.MANAGER
        )
        assert user.is_staff is True
        assert user.is_superuser is False

    def test_create_user_auditor(self):
        """Testa se AUDITOR não recebe permissões administrativas."""
        user = User.objects.create_user(
            username="auditor_user", password="password123", role=User.Role.AUDITOR
        )
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_change_role_updates_permissions(self):
        """Testa se mudar o role atualiza as permissões."""
        user = User.objects.create_user(
            username="test_user", password="password123", role=User.Role.AUDITOR
        )
        assert user.is_staff is False

        user.role = User.Role.ADMIN
        user.save()
        assert user.is_staff is True
        assert user.is_superuser is True

        user.role = User.Role.MANAGER
        user.save()
        assert user.is_staff is True
        assert user.is_superuser is False
