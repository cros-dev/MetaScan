import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

@pytest.mark.django_db
class SlotViewSetTestCase(TestCase):
    def setUp(self):
        # Usa Django apps para acessar modelos de outros apps
        Cavalete = apps.get_model('cavaletes', 'Cavalete')
        Slot = apps.get_model('cavaletes', 'Slot')
        
        # Cria usuário de teste
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='manager'
        )
        
        # Cria cavalete de teste
        self.cavalete = Cavalete.objects.create(
            name='Cavalete Teste',
            code='CAV99'
        )
        
        # Cria slot de teste
        self.slot = Slot.objects.create(
            cavalete=self.cavalete,
            side='A',
            number=1,
            status='available'
        )
