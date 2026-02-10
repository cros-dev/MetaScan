"""Testes das permissões customizadas do app core."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class PermissionsTestCase(TestCase):
    """Testes para permissões customizadas."""

    def setUp(self):
        """Configuração inicial."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="testpass123"
        )

    def test_is_owner_or_read_only_with_owner_attr(self):
        """Testa IsOwnerOrReadOnly com objeto que tem atributo 'owner'."""

        class MockObject:
            def __init__(self, owner):
                self.owner = owner

        permission = IsOwnerOrReadOnly()
        obj = MockObject(self.owner)

        # GET permite para qualquer um
        request = type("Request", (), {"user": self.other_user, "method": "GET"})()
        self.assertTrue(permission.has_object_permission(request, None, obj))

        # PUT permite apenas para owner
        request_owner = type("Request", (), {"user": self.owner, "method": "PUT"})()
        request_other = type(
            "Request", (), {"user": self.other_user, "method": "PUT"}
        )()

        self.assertTrue(permission.has_object_permission(request_owner, None, obj))
        self.assertFalse(permission.has_object_permission(request_other, None, obj))

    def test_is_owner_or_read_only_with_user_attr(self):
        """Testa IsOwnerOrReadOnly com objeto que tem atributo 'user'."""

        class MockObject:
            def __init__(self, user):
                self.user = user

        permission = IsOwnerOrReadOnly()
        obj = MockObject(self.owner)

        # GET permite para qualquer um
        request = type("Request", (), {"user": self.other_user, "method": "GET"})()
        self.assertTrue(permission.has_object_permission(request, None, obj))

        # PUT permite apenas para user
        request_owner = type("Request", (), {"user": self.owner, "method": "PUT"})()
        request_other = type(
            "Request", (), {"user": self.other_user, "method": "PUT"}
        )()

        self.assertTrue(permission.has_object_permission(request_owner, None, obj))
        self.assertFalse(permission.has_object_permission(request_other, None, obj))

    def test_is_owner_or_read_only_without_owner_or_user(self):
        """Testa IsOwnerOrReadOnly com objeto sem atributo 'owner' ou 'user'."""

        class MockObject:
            pass

        permission = IsOwnerOrReadOnly()
        obj = MockObject()

        # GET permite
        request = type("Request", (), {"user": self.owner, "method": "GET"})()
        self.assertTrue(permission.has_object_permission(request, None, obj))

        # PUT não permite (objeto sem owner/user)
        request = type("Request", (), {"user": self.owner, "method": "PUT"})()
        self.assertFalse(permission.has_object_permission(request, None, obj))
